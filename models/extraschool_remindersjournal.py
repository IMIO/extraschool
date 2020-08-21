# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
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


class reminder_report_pdf_thread(threading.Thread):
    def __init__(self, cr, uid, reminder_ids, context=None):
        self.cr = cr
        self.uid = uid
        self.reminder_ids = reminder_ids
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        reminder = self.env['extraschool.reminder']
        report = self.env['report']
        report.get_pdf(reminder.browse(self.reminder_ids), 'extraschool.reminder_report_layout')


class extraschool_remindersjournal(models.Model):
    _name = 'extraschool.remindersjournal'
    _description = 'Reminders journal'
    _inherit = 'mail.thread'

    name = fields.Char('Name', required=True, track_visibility='onchange')
    activity_category_ids = fields.Many2many('extraschool.activitycategory', required=True, readonly=True,
                                             states={'hidden': [('readonly', False)], 'draft': [('readonly', False)]})
    transmission_date = fields.Date('Transmission date', default=datetime.date.today(), required=True, readonly=True,
                                    states={'hidden': [('readonly', False)], 'draft': [('readonly', False)]},
                                    track_visibility='onchange', help=_("This field is used for biller's date"))
    reminders_journal_item_ids = fields.One2many(comodel_name='extraschool.reminders_journal_item',
                                                 inverse_name='reminders_journal_id',
                                                 string='Reminder journal item')
    reminder_ids = fields.One2many(comodel_name='extraschool.reminder', inverse_name='reminders_journal_id',
                                   string='Reminders',
                                   track_visibility='onchange')
    biller_id = fields.Many2one(comodel_name='extraschool.biller', string='Biller', readonly=True,
                                states={'hidden': [('readonly', False)]})
    biller_ids = fields.One2many(comodel_name='extraschool.biller', inverse_name='reminder_journal_id',
                                 compute='_compute_concerned_billers')
    ready_to_print = fields.Boolean(String='Ready to print', default=False)
    date_from = fields.Date(string='Date from', readonly=True,
                            states={'hidden': [('readonly', False)], 'draft': [('readonly', False)]},
                            track_visibility='onchange')
    date_to = fields.Date(string='Date to', readonly=True,
                          states={'hidden': [('readonly', False)], 'draft': [('readonly', False)]},
                          track_visibility='onchange')
    state = fields.Selection([('hidden', 'Hidden'),
                              ('draft', 'Draft'),
                              ('validated', 'Validated')],
                             'validated', required=True, default='hidden', track_visibility='onchange'
                             )
    based_reminder_id = fields.Many2one(comodel_name='extraschool.remindersjournal',
                                        string='Choose the reminder to be based on',
                                        track_visibility='onchange')
    show_based_reminder = fields.Boolean('Clic here if it\'s not the first reminder', default=False,
                                         track_visibility='onchange')
    unsolved_reminder_ids = fields.One2many(comodel_name='extraschool.reminder', inverse_name='reminders_journal_id',
                                            string='Unsolved Reminders',
                                            compute="_compute_unsolved_reminder_method", track_visibility='onchange')

    @api.onchange('date_from', 'date_to', 'activity_category_ids')
    @api.multi
    def _compute_concerned_billers(self):
        """
        Compute billers concerned by reminders journal
        :return: None
        """
        for rec in self:
            if rec.date_from and rec.date_to:
                records = rec.env['extraschool.biller'].search(
                    [('invoices_date', '<=', rec.date_to),
                     ('invoices_date', '>=', rec.date_from),
                     ('fees', '=', False)]).filtered(
                    lambda r: r.activitycategoryid in rec.activity_category_ids)
                if rec.biller_id:
                    records += rec.biller_id
                rec.biller_ids = records

    @api.multi
    def _compute_unsolved_reminder_method(self):
        """
        Search unpaid reminders for display
        :return: None
        """
        for rec in self:
            rec.unsolved_reminder_ids = [reminder.id for reminder in self.env['extraschool.reminder'].search(
                [('reminders_journal_id', '=', rec.id)]) if reminder.balance_computed > 0]

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
            env = Environment(new_cr, uid, context)

            report = self.pool.get('report')
            for reminder in reminders:
                logging.info("generate pdf {}".format(reminder.id))
                env['report'].get_pdf(reminder, 'extraschool.reminder_report_layout')

            new_cr.commit()
            new_cr.close()
            return {}

    @api.multi
    def generate_pdf(self):
        self.ensure_one()
        cr, uid = self.env.cr, self.env.user.id

        self.env['ir.attachment'].search([('res_id', 'in', [i.id for i in self.reminder_ids]),
                                          ('res_model', '=', 'extraschool.reminder')]).unlink()

        self.env.invalidate_all()

        threaded_report = []
        chunk_size = 50
        for zz in range(0, len(self.reminder_ids) / chunk_size + 1):
            sub_reminders = self.reminder_ids[zz * chunk_size:(zz + 1) * chunk_size]
            if len(sub_reminders):
                thread = threading.Thread(target=self.generate_pdf_thread,
                                          args=(cr, uid, sub_reminders, self.env.context))
                threaded_report.append(thread)
                thread.start()

    @api.multi
    def _ensure_reminder_type_exists(self):
        # Get the next reminder_type
        reminder_type = self.env['extraschool.remindertype'].search(
            [('selected_type_id', '=', self.based_reminder_id.reminders_journal_item_ids.reminder_type_id.id)])
        if not reminder_type:
            raise Warning(_("There is no next reminder."))
        return reminder_type

    @api.multi
    def _create_fees_biller(self):
        self.biller_id = self.env['extraschool.biller'].create({'period_from': self.transmission_date,
                                                                'period_to': self.transmission_date,
                                                                'activitycategoryid': [(6, False,
                                                                                        self.activity_category_ids.ids)],
                                                                'invoices_date': self.transmission_date,
                                                                'fees': True
                                                                })

    @api.multi
    def _create_fees_if_needed(self, reminder_type, activity_category):
        if reminder_type.fees_type == 'fix':
            self._create_fees_biller()
            for reminder in self.reminder_ids:
                next_invoice_num = activity_category.get_next_comstruct('invoice', self.biller_id.get_from_year())
                fees_invoice = self.env["extraschool.invoice"].create(
                    {'name': _('invoice_%s') % (next_invoice_num['num'],),
                     'number': next_invoice_num['num'],
                     'parentid': reminder.parentid.id,
                     'biller_id': self.biller_id.id,
                     'activitycategoryid': [(6, False, self.activity_category_ids.ids)],
                     'structcom': next_invoice_num['com_struct'],
                     'last_reminder_id': reminder.id,
                     'reminder_fees': True,
                     'payment_term': datetime.date.today() + datetime.timedelta(days=reminder_type.payment_term_in_day)
                     })
                self.env['extraschool.invoicedprestations'].create({'invoiceid': fees_invoice.id,
                                                                    'description': reminder_type.fees_description if reminder_type.fees_description else 'Frais de rappel',
                                                                    'unit_price': reminder_type.fees_amount,
                                                                    'quantity': 1,
                                                                    'total_price': reminder_type.fees_amount,
                                                                    })
                reminder.write({'fees_amount': reminder_type.fees_amount,
                                'concerned_invoice_ids': [(4, [fees_invoice.id])]})

                logging.info("####Computing balance...")
                for invoice in self.biller_id.invoice_ids:
                    invoice._compute_balance()

    @api.multi
    def _create_reminders_journal_item(self, reminder_type, amount_dict):
        reminders_journal_amount = 0
        for amount in amount_dict:
            reminders_journal_amount += sum([i for i in amount_dict[amount]])

        return self.env['extraschool.reminders_journal_item'].create(
            {'name': "%s - %s" % (self.name, reminder_type.name),
             'reminder_type_id': reminder_type.id,
             'reminders_journal_id': self.id,
             'payment_term': datetime.datetime.strptime(self.transmission_date, "%Y-%m-%d") + datetime.timedelta(
                 days=reminder_type.payment_term_in_day),
             'amount': reminders_journal_amount,
             })

    @api.multi
    def _create_reminders(self, reminder_type, invoice_dict, amount_dict, activity_category):
        invoice_obj = self.env["extraschool.invoice"]
        reminders_journal_item_id = self._create_reminders_journal_item(reminder_type, amount_dict)
        count = 1
        for parent_id in invoice_dict:
            logging.info("### [{}/{}] reminder created...".format(count, len(invoice_dict)))
            count += 1

            reminder = self.env['extraschool.reminder'].create(
                {'reminders_journal_item_id': reminders_journal_item_id.id,
                 'reminders_journal_id': self.id,
                 'parentid': parent_id,
                 'school_implantation_id': invoice_obj.browse(invoice_dict[parent_id][0]).schoolimplantationid.id,
                 'structcom': activity_category.get_next_comstruct(
                     'reminder', invoice_obj.browse(invoice_dict[parent_id][0]).biller_id.get_from_year(), False)[
                     'com_struct'],
                 'amount': sum([invoice_obj.browse(invoice).balance for invoice in invoice_dict[parent_id]]),
                 'concerned_invoice_ids': [(6, 0, invoice_dict[parent_id])],
                 })

            self.env['extraschool.invoice'].browse(invoice_dict[parent_id]).write({'last_reminder_id': reminder.id})

    @api.multi
    def _next_reminder(self):
        """
        When reminders journal is based on another reminder, this function is called.
        :return: None
        """
        logging.info("Initiating Next Reminder method")
        reminder_type = self._ensure_reminder_type_exists()
        activity_category = self._ensure_activity_category()

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
        cr.execute(get_invoice_sql, (self.based_reminder_id.id, reminder_type.minimum_balance))
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
                self.env["extraschool.invoice"].search([('id', '=', invoice[0])]).write({'tag': 1})

        parent_to_del = []
        for parent in invoice_dict:
            sum_parent_balance = sum(
                self.env['extraschool.invoice'].search([('id', 'in', invoice_dict[parent])]).mapped('balance'))

            if sum_parent_balance <= reminder_type.minimum_general_balance:
                parent_to_del.append(parent)

        for parent in parent_to_del:
            invoice_dict.pop(parent, None)
            amount_dict.pop(parent, None)

        self._create_reminders(reminder_type, invoice_dict, amount_dict, activity_category)
        self._create_fees_if_needed(reminder_type, activity_category)

        return True

    @api.multi
    def _ensure_activity_category(self):
        activity_category = self.activity_category_ids[0]
        if len(self.activity_category_ids) > 1:
            activity_category = self.env['extraschool.organising_power'].search([])[0].dominant_activity_category_id
            if not activity_category:
                raise Warning(_('There is no dominant activity category !'))
        return activity_category

    @api.multi
    def _ensure_that_exists_reminder_type(self):
        organising_power = self.env['extraschool.organising_power'].search([])[0]
        activity_category = self.activity_category_ids[0]
        if len(self.activity_category_ids) > 1:
            activity_category = organising_power.dominant_activity_category_id
        if not activity_category.reminer_type_ids:
            raise Warning(_("These activity doesn't have any type of reminders : {}").format(activity_category.name))

    @api.multi
    def _ensure_that_dates_are_corrects(self):
        if self.date_from > self.date_to:
            raise Warning(_("Date to must be bigger than date from !!!"))

    @api.multi
    def _get_invoice_search_domain_date_range(self):
        invoice_search_domain_date_range = []
        if self.date_from and self.date_to:
            invoice_search_domain_date_range = [('biller_id.invoices_date', '>=', self.date_from),
                                                ('biller_id.invoices_date', '<=', self.date_to)]
        return invoice_search_domain_date_range

    @api.multi
    def _get_payterm(self, reminder_type):
        to_date = datetime.date.today() - datetime.timedelta(days=reminder_type.delay)
        invoice_search_domain = [('payment_term', '<=', to_date),
                                 ('last_reminder_id', '=', False)]
        if reminder_type.selected_type_id.id or reminder_type.select_reminder_type:
            invoice_search_domain = [('last_reminder_id.reminders_journal_item_id.reminder_type_id', '=',
                                      reminder_type.selected_type_id.id),
                                     ('last_reminder_id.reminders_journal_item_id.payment_term', '<=',
                                      to_date)]
        return invoice_search_domain

    @api.multi
    def _get_parent_id_under_limit(self, invoice_search_domain, reminder_type):
        invoice_ids = self.env['extraschool.invoice'].search(invoice_search_domain).sorted(
            key=lambda r: r.parentid.id)
        parent_id = invoice_ids.mapped('parentid')
        remove_parent = []
        # Get parent id where the total of invoices is under the limit (0.0 by default)
        for parent in parent_id:
            balance = sum([invoice.balance for invoice in invoice_ids.search([('parentid', '=', parent.id),
                                                                              ('tag', '=', None)])])
            if balance <= reminder_type.minimum_general_balance:
                remove_parent.append(parent.id)
        return remove_parent

    @api.multi
    def _get_invoice_search_domain(self, reminder_type):
        invoice_search_domain = [('balance', '>=', reminder_type.minimum_balance),
                                 ('tag', '=', None),
                                 ('biller_id.fees', '=', False)]
        invoice_search_domain += self._get_invoice_search_domain_date_range()
        invoice_search_domain += self._get_payterm(reminder_type)

        remove_parent = self._get_parent_id_under_limit(invoice_search_domain, reminder_type)
        invoice_search_domain += [('parentid', 'not in', tuple(remove_parent))]
        return invoice_search_domain

    @api.multi
    def _get_invoice_ids(self, reminder_type):
        return self.env['extraschool.invoice'].search(self._get_invoice_search_domain(reminder_type)).sorted(
            lambda r: r.parentid.id).filtered(
            lambda r: r.activitycategoryid in self.activity_category_ids)

    @api.multi
    def validate(self):
        self.ensure_one()
        if self.based_reminder_id:
            self._next_reminder()
        else:
            logging.info("Initiating Validate method")
            self._ensure_that_exists_reminder_type()
            self._ensure_that_dates_are_corrects()

            inv_obj = self.env['extraschool.invoice']
            inv_line_obj = self.env['extraschool.invoicedprestations']
            biller_id = -1

            for activity_category in self.activity_category_ids:
                for reminder_type in activity_category.reminer_type_ids.sorted(key=lambda r: r.sequence,
                                                                               reverse=True):
                    logging.info("##Check Reminder Type")

                    invoice_ids = self._get_invoice_ids(reminder_type)

                    # create reminders_journal_item_id
                    reminders_journal_item_id = self.env['extraschool.reminders_journal_item'].create(
                        {'name': "%s - %s" % (self.name, reminder_type.name),
                         'reminder_type_id': reminder_type.id,
                         'reminders_journal_id': self.id,
                         'payment_term': datetime.datetime.strptime(self.transmission_date,
                                                                    "%Y-%m-%d") + datetime.timedelta(
                             days=reminder_type.payment_term_in_day),
                         'amount': sum([invoice.balance for invoice in invoice_ids])})

                    reminder = False
                    parent_id = -1
                    total_amount = 0.0
                    amount = 0.0
                    concerned_invoice_ids = []
                    count = 1
                    for invoice in invoice_ids:
                        logging.info("##[{}/{}] invoices processed...".format(count, len(invoice_ids)))
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

                            reminder = self.env['extraschool.reminder'].create(
                                {'reminders_journal_item_id': reminders_journal_item_id.id,
                                 'reminders_journal_id': self.id,
                                 'parentid': parent_id,
                                 'school_implantation_id': invoice.schoolimplantationid.id,
                                 'structcom': activity_category.get_next_comstruct('reminder',
                                                                                   fields.Date.from_string(
                                                                                       self.transmission_date).year,
                                                                                   False)['com_struct']
                                 })
                            if reminder_type.fees_type == 'fix':
                                if biller_id == -1:
                                    self._create_fees_biller()
                                    biller_id = self.biller_id.id

                                next_invoice_num = activity_category.get_next_comstruct('invoice',
                                                                                        self.biller_id.get_from_year(),
                                                                                        False)
                                # create fees invoice
                                fees_invoice = inv_obj.create({'name': _('invoice_%s') % (next_invoice_num['num'],),
                                                               'number': next_invoice_num['num'],
                                                               'parentid': parent_id,
                                                               'biller_id': biller_id,
                                                               'activitycategoryid': [
                                                                   (6, False, self.activity_category_ids.ids)],
                                                               'structcom': next_invoice_num['com_struct'],
                                                               'last_reminder_id': reminder.id,
                                                               'reminder_fees': True,
                                                               'payment_term': datetime.date.today() + datetime.timedelta(
                                                                   days=reminder_type.payment_term_in_day),
                                                               })
                                concerned_invoice_ids.append(fees_invoice.id)
                                inv_line_obj.create({'invoiceid': fees_invoice.id,
                                                     'description': reminder_type.fees_description if reminder_type.fees_description else 'Frais de rappel',
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

                            reminder.write({'amount': amount,
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

                    if biller_id > 0:
                        self.biller_id.invoice_ids._compute_balance()

        # update invoice to exit from accounting
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

        self.env.cr.commit()
        self.generate_pdf()
        self.state = "validated"
        return True

    @api.multi
    def mail_reminders(self):
        return {'name': 'Reminders',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.reminder',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('reminders_journal_id.id', '=', self.id),
                           '|', ('remindersendmethod', '=', 'onlybymail'), ('remindersendmethod', '=', 'emailandmail')],
                'context': {"search_default_unsolve_reminders": 1}
                }

    @api.multi
    def email_reminders(self):
        return {'name': 'Reminders',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.reminder',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('reminders_journal_id.id', '=', self.id),
                           '|', ('remindersendmethod', '=', 'onlyemail'), ('remindersendmethod', '=', 'emailandmail')],
                'context': {"search_default_unsolve_reminders": 1}
                }

    @api.multi
    def all_reminders(self):
        return {'name': 'Reminders',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.reminder',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('reminders_journal_id.id', '=', self.id)],
                'context': {"search_default_unsolve_reminders": 1}
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
                'domain': [('res_id', 'in', [i.id for i in self.reminder_ids]),
                           ('res_model', '=', 'extraschool.reminder')],
                'context': {"search_default_actif": 1},

                }

    @api.multi
    def write(self, vals):
        if self.state == 'validated':
            raise Warning(_("You can't modify an existing reminder."))
        else:
            return super(extraschool_remindersjournal, self).write(vals)

    @api.multi
    def unlink(self):
        for reminder_journal_item in self.reminders_journal_item_ids:
            if reminder_journal_item.reminder_type_id.bailiff:
                reminder_ids = self.env['extraschool.reminder'].search([('reminders_journal_id', '=', self.id)])
                for reminder in reminder_ids:
                    self.env['extraschool.invoice'].search([('last_reminder_id', '=', reminder.id)]).write(
                        {'tag': None})

        return super(extraschool_remindersjournal, self).unlink()

    @api.model
    def create(self, vals):
        rec = super(extraschool_remindersjournal, self).create(vals)
        if rec.show_based_reminder:
            rec.activity_category_ids = rec.based_reminder_id.activity_category_ids
        rec['state'] = 'draft'
        return rec


class extraschool_remindersjournal_item(models.Model):
    _name = 'extraschool.reminders_journal_item'
    _description = 'Reminders journal item'

    name = fields.Char('Name', required=True)
    reminder_type_id = fields.Many2one('extraschool.remindertype', 'Reminder type', required=True)
    reminders_journal_id = fields.Many2one('extraschool.remindersjournal', 'Reminder journal', ondelete='cascade',
                                           required=True)
    payment_term = fields.Date('Payment term', required=True)
    amount = fields.Float('Amount', required=True)
