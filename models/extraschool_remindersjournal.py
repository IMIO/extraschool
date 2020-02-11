# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia & Jenny Pans - Imio (<http://www.imio.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, fields, _
import datetime
import threading
from openerp.api import Environment
from openerp.exceptions import except_orm, Warning, RedirectWarning
import logging
_logger = logging.getLogger(__name__)


class reminder_report_pdf_thread (threading.Thread):
   def __init__(self, cr, uid, reminder_ids, context=None):
      self.cr = cr
      self.uid = uid
      self.reminder_ids = reminder_ids
      self.context = context
      threading.Thread.__init__(self)

   def run(self):
       reminder = self.env['extraschool.reminder']
       report = self.env['report']
       report.get_pdf(reminder.browse(self.reminder_ids),'extraschool.reminder_report_layout')

class extraschool_remindersjournal(models.Model):
    _name = 'extraschool.remindersjournal'
    _description = 'Reminders journal'
    _inherit = 'mail.thread'

    name = fields.Char('Name', required=True, track_visibility='onchange')
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=True, readonly=True, states={'draft': [('readonly', False)]})
    transmission_date = fields.Date('Transmission date', default=datetime.date.today(), required=True, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    reminders_journal_item_ids = fields.One2many('extraschool.reminders_journal_item', 'reminders_journal_id','Reminder journal item')
    reminder_ids = fields.One2many('extraschool.reminder', 'reminders_journal_id','Reminders', track_visibility='onchange')
    biller_id = fields.Many2one('extraschool.biller', 'Biller', readonly=True, states={'draft': [('readonly', False)]})
    biller_ids = fields.One2many('extraschool.biller', 'reminder_journal_id')
    remindersjournal_biller_item_ids = fields.One2many('extraschool.reminders_journal_biller_item', 'reminders_journal_id','Reminders biller item')
    ready_to_print = fields.Boolean(String = 'Ready to print', default = False)
    date_from = fields.Date(string='Date from', readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    date_to = fields.Date(string='Date to', readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'),
                              ('validated', 'Validated')],
                             'validated', required=True, default='draft', track_visibility='onchange'
                             )
    based_reminder_id = fields.Many2one('extraschool.remindersjournal', 'Choose the reminder to be based on', track_visibility='onchange')
    show_based_reminder = fields.Boolean('Clic here if it\'s not the first reminder', default=False, track_visibility='onchange')
    unsolved_reminder_ids = fields.One2many('extraschool.reminder', 'reminders_journal_id', 'Unsolved Reminders', compute="_get_unsolved_reminder_method", track_visibility='onchange')

    @api.onchange('date_from', 'date_to')
    @api.multi
    def get_concerned_biller(self):
        if self.date_from and self.date_to:

            self.biller_ids = self.env['extraschool.biller'].search(
                [('invoices_date', '<=', self.date_to),
                 ('invoices_date', '>=', self.date_from),
                 ]).ids

    @api.one
    def _get_unsolved_reminder_method(self):
        unsolved_reminder_ids = []

        get_reminder_ids = self.env['extraschool.reminder'].search([('reminders_journal_id', '=', self.id)])

        for reminder in get_reminder_ids:
            invoice_ids = self.env['extraschool.reminder'].browse(reminder.id).concerned_invoice_ids
            balance = sum([self.env['extraschool.invoice'].browse(invoice.id).balance for invoice in invoice_ids])
            if balance > 0:
                unsolved_reminder_ids.append(reminder.id)
                reminder.write({'balance': balance})

        self.unsolved_reminder_ids = unsolved_reminder_ids

    @api.multi
    def write(self,vals):
        if self.state == 'validated':
            raise Warning(_("You can't modify an existing reminder."))
        else:
            return super(extraschool_remindersjournal, self).write(vals)

    @api.model
    def generate_pdf_thread(self, cr, uid, reminders, context=None):
        """
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: List of IDs selected
        @param context: A standard dictionary
        """
        with Environment.manage():

            # As this function is in a new thread, i need to open a new cursor, because the old one may be closed.
            new_cr = self.pool.cursor()
            env = Environment(new_cr, uid,context)

            report = self.pool.get('report')
            for reminder in reminders:
                logging.info("generate pdf {}".format(reminder.id))
                env['report'].get_pdf(reminder ,'extraschool.reminder_report_layout')

            new_cr.commit()
            new_cr.close()
            return {}

    @api.one
    def generate_pdf(self):
        cr,uid = self.env.cr, self.env.user.id

        self.env['ir.attachment'].search([('res_id', 'in',[i.id for i in self.reminder_ids]),
                                           ('res_model', '=', 'extraschool.reminder')]).unlink()

        self.env.invalidate_all()

        threaded_report = []
        chunk_size = 50
        for zz in range(0,len(self.reminder_ids)/chunk_size+1):
            sub_reminders = self.reminder_ids[zz*chunk_size:(zz+1)*chunk_size]
            if len(sub_reminders):
                thread = threading.Thread(target=self.generate_pdf_thread, args=(cr, uid, sub_reminders,self.env.context))
                threaded_report.append(thread)
                thread.start()

    # @api.multi
    # def delete(self):
    #     self.reminder_ids.unlink()
    #     self.reminders_journal_item_ids.unlink()

    # Called from remindersjournal.validate()
    @api.multi
    def next_reminder(self):
        logging.info("Initiating Next Reminder method")
        biller_is_made = False
        invoice_obj = self.env['extraschool.invoice']
        # Get the information of the reminder this one is based on.
        new_remindersjournal = self.env['extraschool.remindersjournal'].browse(self.based_reminder_id.id)

        # Get the next reminder_type
        reminder_type = self.env['extraschool.remindertype'].search(
            [('selected_type_id', '=', new_remindersjournal.reminders_journal_item_ids.reminder_type_id.id)])

        if not reminder_type:
            raise Warning(_("There is no next reminder."))

        # Return id[0], balance[1] and parentid[2] of all the invoices that were not paid for the last reminder.
        cr = self.env.cr
        get_invoice_sql = ("""  SELECT i.id, i.balance, p.id, i.schoolimplantationid
                                FROM extraschool_invoice AS i
                                INNER JOIN extraschool_parent AS p ON i.parentid = p .id
                                WHERE i.id IN (
                                                SELECT i.id
                                                FROM extraschool_reminder AS r
                                                INNER JOIN extraschool_reminder_invoice_rel AS ri
                                                ON r.id = ri.reminder_id
                                                INNER JOIN extraschool_invoice AS i
                                                ON ri.invoice_id = i.id
                                                INNER JOIN extraschool_parent AS p
                                                ON r.parentid = p.id
                                                WHERE r.reminders_journal_id = %s
                                                AND i.balance >= %s
                                                AND i.tag IS NULL
                                                )
                                ORDER BY p.id"""
                           )
        cr.execute(get_invoice_sql, (new_remindersjournal.id, reminder_type.minimum_balance))
        invoice_ids = cr.fetchall()

        logging.info("# {} invoices to process".format(len(invoice_ids)))

        # Build dictionnary of invoices sorted by parents.
        invoice_dict = {}
        amount_dict = {}

        logging.info("##Building dictionnary of invoices sorted by parents...")

        for invoice in invoice_ids:
            invoice_dict.setdefault(invoice[2], []).append(invoice[0])
            amount_dict.setdefault(invoice[2], []).append(invoice[1])
            if reminder_type.bailiff:
                invoice_obj.search([('id', '=', invoice[0])]).write({'tag': 1})

        parent_to_del = []
        for parent in invoice_dict:
            sum_parent_balance = sum(
                self.env['extraschool.invoice'].search([('id', 'in', invoice_dict[parent])]).mapped('balance'))

            if sum_parent_balance <= reminder_type.minimum_general_balance:
                parent_to_del.append(parent)

        for parent in parent_to_del:
            invoice_dict.pop(parent, None)
            amount_dict.pop(parent, None)

        reminders_journal_amount = 0
        for amount in amount_dict:
            reminders_journal_amount += sum([i for i in amount_dict[amount]])

        # Create a reminder journal
        reminders_journal_item_id = self.env['extraschool.reminders_journal_item'].create(
            {'name': "%s - %s" % (self.name, reminder_type.name),
             'reminder_type_id': reminder_type.id,
             'reminders_journal_id': self.id,
             'payment_term': datetime.datetime.strptime(self.transmission_date, "%Y-%m-%d") + datetime.timedelta(days=reminder_type.payment_term_in_day),
             'amount': reminders_journal_amount,
             })

        count = 1
        # For each parent create a reminder and add fees if needed.
        for key in invoice_dict:
            logging.info("### [{}/{}] reminder created...".format(count, len(invoice_dict)))
            count += 1

            reminder = self.env['extraschool.reminder'].create({'reminders_journal_item_id': reminders_journal_item_id.id,
                                                                'reminders_journal_id': self.id,
                                                                'parentid': key,
                                                                'school_implantation_id': invoice_obj.browse(invoice_dict[key][0]).schoolimplantationid.id,
                                                                'structcom': invoice_obj.browse(invoice_dict[key][0]).activitycategoryid.get_next_comstruct(
                                                                    'reminder', invoice_obj.browse(invoice_dict[key][0]).biller_id.get_from_year(), False, True)[
                                                                    'com_struct'],
                                                                'amount': sum([invoice_obj.browse(invoice).balance for invoice in invoice_dict[key]]),
                                                                'concerned_invoice_ids': [(6, 0, invoice_dict[key])],
                                                                })

            self.env['extraschool.invoice'].browse(invoice_dict[key]).write({'last_reminder_id': reminder.id})

            # If the reminder has fees, compute de total cost.
            if reminder_type.fees_type == 'fix':
                # Add fees in reminder.
                reminder.write({'fees_amount': reminder_type.fees_amount,})

                # Create Biller
                if not biller_is_made:
                    self.biller_id = self.env['extraschool.biller'].create({'period_from': self.transmission_date,
                                                                            'period_to': self.transmission_date,
                                                                            'activitycategoryid': [(6, False, self.activity_category_id.ids)],
                                                                            'invoices_date': self.transmission_date,
                                                                            })
                    biller_is_made = True

                next_invoice_num = self.activity_category_id.get_next_comstruct('invoice',
                                                                                self.biller_id.get_from_year(), False, True)
                fees_invoice = invoice_obj.create(
                    {'name': _('invoice_%s') % (next_invoice_num['num'],),
                     'number': next_invoice_num['num'],
                     'parentid': key,
                     'biller_id': self.biller_id.id,
                     'activitycategoryid': [(6, False, self.activity_category_id.ids)],
                     'structcom': next_invoice_num['com_struct'],
                     'last_reminder_id': reminder.id,
                     'reminder_fees': True,
                     'payment_term': datetime.date.today() + datetime.timedelta(days=reminder_type.payment_term_in_day),
                     })

                self.env['extraschool.invoicedprestations'].create({'invoiceid' : fees_invoice.id,
                                     'description' : reminder_type.fees_description if reminder_type.fees_description != False else 'Frais de rappel',
                                     'unit_price': reminder_type.fees_amount,
                                     'quantity': 1,
                                     'total_price': reminder_type.fees_amount,
                                     })

            logging.info("####Computing balance...")
            if biller_is_made:
                for invoice in self.biller_id.invoice_ids:
                    invoice._compute_balance()

        self.state = "validated"
        return True


    @api.multi
    def validate(self):
        self.ensure_one()
        if self.based_reminder_id:
            self.next_reminder()
        else:
            logging.info("Initiating Validate method")
            if len(self.activity_category_id.reminer_type_ids.ids) == 0 :
                return False

            invoice_search_domain_date_range = []
            #selection on date range
            if self.date_from:
                if self.date_from > self.date_to:
                    raise Warning(_("Date to must be bigger than date from !!!"))
                invoice_search_domain_date_range = [
                                                    ('biller_id.invoices_date', '>=',self.date_from),
                                                    ('biller_id.invoices_date', '<=', self.date_to)
                                                    ]


            inv_obj = self.env['extraschool.invoice']
            payment_obj = self.env['extraschool.payment']
            inv_line_obj = self.env['extraschool.invoicedprestations']
            biller_id = -1
            #browse activivity categ reminder type
            for reminder_type in self.activity_category_id.reminer_type_ids.sorted(key=lambda r: r.sequence, reverse=True):
                logging.info("##Check Reminder Type")
                #select invoices
                invoice_search_domain = [('activitycategoryid.id', '=',self.activity_category_id.id),
                                         ('balance', '>',0), # todo: See if this is needed.
                                         ('balance', '>=',reminder_type.minimum_balance),
                                         ('tag', '=', None),
                                         ]


                #add selection on date range
                invoice_search_domain += invoice_search_domain_date_range
                #compute pa
                to_date = datetime.date.today() - datetime.timedelta(days=reminder_type.delay)

                    #filter on payterm depend on reminder_type (no reminder_type = invoice_payment_term)
                if reminder_type.selected_type_id.id == False or reminder_type.select_reminder_type == False:
                    #payterm is taken from invoice
                    invoice_search_domain+= [('payment_term', '<=',to_date), # This is payment_term of the invoice because it's the first reminder
                                             ('last_reminder_id', '=', False)
                                             ]
                else:
                    #payterm is taken from reminder_journal
                    invoice_search_domain+= [('last_reminder_id.reminders_journal_item_id.reminder_type_id','=', reminder_type.selected_type_id.id),
                                             ('last_reminder_id.reminders_journal_item_id.payment_term', '<=',to_date)]

                invoice_ids = self.env['extraschool.invoice'].search(invoice_search_domain).sorted(key=lambda r: r.parentid.id)
                parent_id = invoice_ids.mapped('parentid')
                remove_parent = []

                # Get parent id where the total of invoices is under the limit (0.0 by default)
                for parent in parent_id:
                    if sum([invoice.balance for invoice in invoice_ids.search([('parentid', '=', parent.id),('tag', '=', None)])]) <= reminder_type.minimum_general_balance:
                        remove_parent.append(parent.id)

                invoice_search_domain += [('parentid', 'not in', tuple(remove_parent))]

                # New invoices
                invoice_ids = self.env['extraschool.invoice'].search(invoice_search_domain).sorted(key=lambda r: r.parentid.id)

                reminders_journal_item_id = self.env['extraschool.reminders_journal_item'].create({'name' : "%s - %s" % (self.name,reminder_type.name),
                                                                                                   'reminder_type_id' : reminder_type.id,
                                                                                                   'reminders_journal_id' : self.id,
                                                                                                   'payment_term' : datetime.datetime.strptime(self.transmission_date, "%Y-%m-%d") + datetime.timedelta(days=reminder_type.payment_term_in_day),
                                                                                                   'amount' : sum([invoice.balance for invoice in invoice_ids])})
                reminder = False
                parent_id = -1
                total_amount = 0.0
                amount = 0.0
                concerned_invoice_ids = []
                count = 1
                for invoice in invoice_ids:
                    logging.info("##[{}/{}] invoices processed...".format(count,len(invoice_ids)))
                    count += 1
                    if invoice.parentid.id != parent_id:
                        if parent_id > 0:
                            if amount > reminder_type.minimum_balance:
                                total_amount += amount
                                # This might be better if we flag invoice as huissier.
                                if reminder_type.out_of_accounting:
                                    amount = 0
                                reminder.write({'amount': amount,
                                                'concerned_invoice_ids': [(6, 0, concerned_invoice_ids)]})
                                inv_obj.browse(concerned_invoice_ids).write({'last_reminder_id': reminder.id})
                            else:
                                reminder.unlink()

                        amount = 0
                        parent_id = invoice.parentid.id
                        concerned_invoice_ids = []

                        # todo enlever le true pour manual et refaire la fonction
                        reminder = self.env['extraschool.reminder'].create({'reminders_journal_item_id': reminders_journal_item_id.id,
                                                                            'reminders_journal_id': self.id,
                                                                            'parentid': parent_id,
                                                                            'school_implantation_id': invoice.schoolimplantationid.id,
                                                                            'structcom': invoice.activitycategoryid.get_next_comstruct('reminder',fields.Date.from_string(self.transmission_date).year, False, True)['com_struct']
                                                                            })
                        if reminder_type.fees_type == 'fix':
                            if biller_id == -1:
                                self.biller_id = self.env['extraschool.biller'].create({'period_from' : self.transmission_date,
                                                                                        'period_to' : self.transmission_date,
                                                                                        'activitycategoryid': self.activity_category_id.id,
                                                                                        'invoices_date': self.transmission_date,
                                                                                        })
                                biller_id = self.biller_id.id

                            next_invoice_num = self.activity_category_id.get_next_comstruct('invoice',self.biller_id.get_from_year(), False, True)
                            fees_invoice = inv_obj.create({'name' : _('invoice_%s') % (next_invoice_num['num'],),
                                                           'number' : next_invoice_num['num'],
                                                           'parentid' : parent_id,
                                                           'biller_id' : biller_id,
                                                           'activitycategoryid': self.activity_category_id.id,
                                                           'structcom': next_invoice_num['com_struct'],
                                                           'last_reminder_id': reminder.id,
                                                           'reminder_fees': True,
                                                           'payment_term': datetime.date.today() + datetime.timedelta(days=reminder_type.payment_term_in_day),
                                                           })
                            concerned_invoice_ids.append(fees_invoice.id)
                            inv_line_obj.create({'invoiceid' : fees_invoice.id,
                                                 'description' : reminder_type.fees_description if reminder_type.fees_description != False else 'Frais de rappel',
                                                 'unit_price': reminder_type.fees_amount,
                                                 'quantity': 1,
                                                 'total_price': reminder_type.fees_amount,
                                                 })
                            total_amount += reminder_type.fees_amount

                    amount += invoice.balance
                    concerned_invoice_ids.append(invoice.id)

                if len(concerned_invoice_ids) > 0:
                    if amount > reminder_type.minimum_balance:
                        logging.info("###Creating Reminders...")
                        total_amount += amount
                        if reminder_type.out_of_accounting:
                            amount = 0

                        reminder.write({'amount' : amount,
                                        'concerned_invoice_ids': [(6, 0, concerned_invoice_ids)]})
                        inv_obj.browse(concerned_invoice_ids).write({'last_reminder_id': reminder.id})
                    else:
                        reminder.unlink()
                else:
                    logging.info("###Nothing has been done...")
                if total_amount > 0:
                    reminders_journal_item_id.amount = total_amount
                else:
                    reminders_journal_item_id.unlink()

                if biller_id > 0 :
                    self.biller_id.invoice_ids._compute_balance()

            #update invoice to exit from accounting
            get_invoice_exit_sql = """select r.id as reminder_id, i.id as invoice_id,i.balance
                                        from extraschool_reminder r
                                        left join extraschool_invoice i on i.last_reminder_id = r.id
                                        left join extraschool_reminders_journal_item ji on ji.id = r.reminders_journal_item_id
                                        left join extraschool_remindertype rt on rt.id = ji.reminder_type_id
                                        where r.reminders_journal_id = %s and rt.out_of_accounting = True
                                    """
            self.env.cr.execute(get_invoice_exit_sql, (self.id,))
            invoice_ids = self.env.cr.dictfetchall()
            logging.info("####Creating refund line")
            count = 1
            for invoice in invoice_ids:
                logging.info("##[{}/{}] refunds processed...".format(count, len(invoice_ids)))
                count += 1
                self.env['extraschool.refound_line'].create({'invoiceid': invoice['invoice_id'],
                                                             'date': datetime.date.today(),
                                                             'description': _("exit from accounting"),
                                                             'amount': invoice['balance'],
                                                             'reminder_id': invoice['reminder_id']
                                                             })

            #update biller summary
            get_biller_summary_sql = """select distinct(i.biller_id) as biller_id,sum(i.balance) as reminder_amount,
                                            case when sum(rl.amount) is null then 0 else sum(rl.amount) end as refound_amount
                                        from extraschool_reminder r
                                        left join extraschool_invoice i on i.last_reminder_id = r.id
                                        left join extraschool_refound_line rl on i.id = rl.invoiceid and rl.reminder_id = r.id
                                        where r.reminders_journal_id = %s
                                        group by i.biller_id
                                    """
            self.env.cr.execute(get_biller_summary_sql, (self.id,))
            biller_summary_ids = self.env.cr.dictfetchall()

            for biller_summary in biller_summary_ids:
                self.env['extraschool.reminders_journal_biller_item'].create({'name': "%s - %s" % (self.name,biller_summary['reminder_amount']),
                                                                              'reminders_journal_id': self.id,
                                                                              'biller_id': biller_summary['biller_id'],
                                                                              'reminder_amount': biller_summary['reminder_amount'],
                                                                              'exit_accounting_amount': biller_summary['refound_amount']})

            self.env.cr.commit()
            self.generate_pdf()
            self.state = "validated"
            return True



    @api.multi
    def mail_reminders(self):
        cr,uid = self.env.cr, self.env.user.id
        view_id = self.pool.get('ir.ui.view').search(cr,uid,[('model','=','extraschool.invoice'),
                                                             ('name','=','invoices.tree')])
        return {'name': 'Reminders',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.reminder',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('reminders_journal_id.id', '=',self.id),
                           '|',('remindersendmethod','=','onlybymail'),('remindersendmethod','=','emailandmail')]
                }

    @api.multi
    def email_reminders(self):
        cr,uid = self.env.cr, self.env.user.id
        view_id = self.pool.get('ir.ui.view').search(cr,uid,[('model','=','extraschool.invoice'),
                                                             ('name','=','invoices.tree')])
        return {'name': 'Reminders',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.reminder',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('reminders_journal_id.id', '=',self.id),
                           '|',('remindersendmethod','=','onlyemail'),('remindersendmethod','=','emailandmail')]
                }

    @api.multi
    def all_reminders(self):
        cr,uid = self.env.cr, self.env.user.id
        view_id = self.pool.get('ir.ui.view').search(cr,uid,[('model','=','extraschool.invoice'),
                                                             ('name','=','invoices.tree')])
        return {'name': 'Reminders',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.reminder',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('reminders_journal_id.id', '=',self.id)]
                }

    @api.multi
    def all_pdf(self):

        return {'name': 'Docs',
                'type': 'ir.actions.act_window',
                'res_model': 'ir.attachment',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('res_id', 'in',[i.id for i in self.reminder_ids]),
                           ('res_model', '=', 'extraschool.reminder')],
                'context': {"search_default_actif":1},

                }

    @api.multi
    def unlink(self):
        if self.reminders_journal_item_ids.reminder_type_id.bailiff:
            reminder_ids = self.env['extraschool.reminder'].search([('reminders_journal_id', '=', self.id)])
            for reminder in reminder_ids:
                self.env['extraschool.invoice'].search([('last_reminder_id', '=', reminder.id)]).write({'tag': None})

        return super(extraschool_remindersjournal, self).unlink()

class extraschool_remindersjournal_item(models.Model):
    _name = 'extraschool.reminders_journal_item'
    _description = 'Reminders journal item'

    name = fields.Char('Name', required=True)
    reminder_type_id = fields.Many2one('extraschool.remindertype', 'Reminder type', required=True)
    reminders_journal_id = fields.Many2one('extraschool.remindersjournal', 'Reminder journal',ondelete='cascade', required=True)
    payment_term = fields.Date('Payment term', required=True)
    amount = fields.Float('Amount', required=True)

class extraschool_reminders_journal_biller_item(models.Model):
    _name = 'extraschool.reminders_journal_biller_item'
    _description = 'Reminders journal biller item'

    name = fields.Char('Name', required=True)
    reminders_journal_id = fields.Many2one('extraschool.remindersjournal', 'Reminder journal',ondelete='cascade')
    biller_id = fields.Many2one('extraschool.biller', 'Biller', required=True)
    reminder_amount = fields.Float('Reminder amount', required=True)
    exit_accounting_amount = fields.Float('Exit accounting amount', required=True)




