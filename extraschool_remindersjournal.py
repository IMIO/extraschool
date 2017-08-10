# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014 
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot - Imio (<http://www.imio.be>).
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
from openerp.api import Environment
import cStringIO
import base64
import os
import lbutils
from pyPdf import PdfFileWriter, PdfFileReader
import datetime
import threading
from openerp.api import Environment
from openerp.exceptions import except_orm, Warning, RedirectWarning


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

    name = fields.Char('Name', required=True)
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=True, readonly=True, states={'draft': [('readonly', False)]})
    transmission_date = fields.Date('Transmission date', required=True, readonly=True, states={'draft': [('readonly', False)]})    
    reminders_journal_item_ids = fields.One2many('extraschool.reminders_journal_item', 'reminders_journal_id','Reminder journal item')   
    reminder_ids = fields.One2many('extraschool.reminder', 'reminders_journal_id','Reminders')                 
    biller_id = fields.Many2one('extraschool.biller', 'Biller', readonly=True, states={'draft': [('readonly', False)]})
    remindersjournal_biller_item_ids = fields.One2many('extraschool.reminders_journal_biller_item', 'reminders_journal_id','Reminders biller item')       
    ready_to_print = fields.Boolean(String = 'Ready to print', default = False)
    date_from = fields.Date(string='Date from', readonly=True, states={'draft': [('readonly', False)]})
    date_to = fields.Date(string='Date to', readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('validated', 'Validated')],
                              'validated', required=True, default='draft'
                              )

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
            
            #As this function is in a new thread, i need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            env = Environment(new_cr, uid,context)
         
            report = self.pool.get('report')
            for reminder in reminders:
                print "generate pdf %s" % (reminder.id)
                env['report'].get_pdf(reminder ,'extraschool.reminder_report_layout')
          
            new_cr.commit()
            new_cr.close()
            return {}
    
    @api.one
    def generate_pdf(self):    
        cr,uid = self.env.cr, self.env.user.id 
        threaded_report = []
        chunk_size = 50
        for zz in range(0,len(self.reminder_ids)/chunk_size+1):
            sub_reminders = self.reminder_ids[zz*chunk_size:(zz+1)*chunk_size]
            print "start thread for ids : %s" % (sub_reminders.ids)
            if len(sub_reminders):
                thread = threading.Thread(target=self.generate_pdf_thread, args=(cr, uid, sub_reminders,self.env.context))
                threaded_report.append(thread)
                thread.start()

    @api.one
    def delete(self):
        self.reminder_ids.unlink()
        self.reminders_journal_item_ids.unlink()
        self.unlink()
                       
    @api.one
    def validate(self):
        import pdb;pdb.set_trace()
        if len(self.activity_category_id.reminer_type_ids.ids) == 0 : 
            return False
        
        invoice_search_domain_date_range = []
        #selection on date range
        if self.date_from:
            if self.date_from > self.date_to:
                raise Warning(_("Date to must be bigger than date from !!!")) 
            invoice_search_domain_date_range = [('biller_id.invoices_date', '>=',self.date_from),
                                                 ('biller_id.invoices_date', '<=', self.date_to)
                                                 ]
                
                
        inv_obj = self.env['extraschool.invoice']
        payment_obj = self.env['extraschool.payment']
        inv_line_obj = self.env['extraschool.invoicedprestations']  
        biller_id = -1        
        #browse activivity categ reminder type 
        for reminder_type in self.activity_category_id.reminer_type_ids.sorted(key=lambda r: r.sequence, reverse=True):            
            #select invoices
            invoice_search_domain = [('activitycategoryid.id', '=',self.activity_category_id.id),                                    
                                    ('balance', '>',0), # todo: See if this is needed.
                                    ('balance', '>=',reminder_type.minimum_balance)]
            
            
            #add selection on date range
            invoice_search_domain += invoice_search_domain_date_range    
            #compute pa
            to_date = datetime.date.today() - datetime.timedelta(days=reminder_type.delay)
                  
            if reminder_type.select_reminder_type == False:
                invoice_search_domain+= [('payment_term', '<=',to_date),                                             
                                             ]
                #filter on payterm depend on reminder_type (no reminder_type = invoice_payment_term)                       
            elif reminder_type.selected_type_id.id == False or reminder_type.select_reminder_type == False:
                #payterm is taken from invoice 
                invoice_search_domain+= [('payment_term', '<=',to_date),
                                             ('last_reminder_id', '=', False)
                                             ]
            else:
                #payterm is taken from reminder_journal
                invoice_search_domain+= [('last_reminder_id.reminders_journal_item_id.reminder_type_id','=', reminder_type.selected_type_id.id),
                                             ('last_reminder_id.reminders_journal_item_id.payment_term', '<=',to_date)]
            
            invoice_ids = self.env['extraschool.invoice'].search(invoice_search_domain).sorted(key=lambda r: r.parentid.id)
            

                 
            reminders_journal_item_id = self.env['extraschool.reminders_journal_item'].create({'name' : "%s - %s" % (self.name,reminder_type.name),
                                                                   'reminder_type_id' : reminder_type.id,
                                                                   'reminders_journal_id' : self.id,
                                                                   'payment_term' : datetime.date.today() + datetime.timedelta(days=reminder_type.payment_term_in_day),
                                                                   'amount' : sum([invoice.balance for invoice in invoice_ids])})
            reminder = False
            parent_id = -1
            total_amount = 0.0
            amount = 0.0
            concerned_invoice_ids = []

            for invoice in invoice_ids:
                if invoice.parentid.id != parent_id:                    
                    if parent_id > 0:
                        if amount > reminder_type.minimum_balance:                            
                            total_amount += amount
                            if reminder_type.out_of_accounting:
                                amount = 0
                            reminder.write({'amount' : amount,
                                            'concerned_invoice_ids': [(6, 0, concerned_invoice_ids)]})
                            inv_obj.browse(concerned_invoice_ids).write({'last_reminder_id': reminder.id})
                        else:
                            reminder.unlink()
                            
                    amount = 0    
                    parent_id = invoice.parentid.id
                    concerned_invoice_ids = []
                    
                    reminder = self.env['extraschool.reminder'].create({'reminders_journal_item_id': reminders_journal_item_id.id,
                                                                        'reminders_journal_id': self.id,
                                                                        'parentid': parent_id,
                                                                        'school_implantation_id': invoice.schoolimplantationid.id,
                                                                        'structcom': invoice.activitycategoryid.get_next_comstruct('reminder',invoice.biller_id.get_from_year())['com_struct']                                                                        
                                                                        })                    
                    if reminder_type.fees_type == 'fix':
                        if biller_id == -1:
                            self.biller_id = self.env['extraschool.biller'].create({'period_from' : self.transmission_date,
                                                                            'period_to' : self.transmission_date,
                                                                            'activitycategoryid': self.activity_category_id.id,
                                                                            'invoices_date': self.transmission_date,
                                                                            })
                            biller_id = self.biller_id.id                            
                        
                        next_invoice_num = self.activity_category_id.get_next_comstruct('invoice',self.biller_id.get_from_year())                            
                        fees_invoice = inv_obj.create({'name' : _('invoice_%s') % (next_invoice_num['num'],),
                                                    'number' : next_invoice_num['num'],
                                                    'parentid' : parent_id,
                                                    'biller_id' : biller_id,
                                                    'activitycategoryid': self.activity_category_id.id,
                                                    'structcom': next_invoice_num['com_struct'],
                                                    'last_reminder_id': reminder.id,
                                                    'reminder_fees': True,
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
                    print "Last yop %s" % (concerned_invoice_ids)
                    total_amount += amount
                    if reminder_type.out_of_accounting:
                        amount = 0

                    reminder.write({'amount' : amount,
                                    'concerned_invoice_ids': [(6, 0, concerned_invoice_ids)]})
                    inv_obj.browse(concerned_invoice_ids).write({'last_reminder_id': reminder.id})
                else:                    
                    reminder.unlink()
            else:
                print "nothing to DO"
            if total_amount > 0:      
                reminders_journal_item_id.amount = total_amount
            else:
                reminders_journal_item_id.unlink()
                                
            if biller_id > 0 :
                self.biller_id.invoice_ids._compute_balance()
                                        
        #update invoice to exit from accounting
        get_invoice_exit_sql = """select r.id as reminder_id, i.id as invoice_id,balance
                                    from extraschool_reminder r
                                    left join extraschool_invoice i on i.last_reminder_id = r.id
                                    left join extraschool_reminders_journal_item ji on ji.id = r.reminders_journal_item_id
                                    left join extraschool_remindertype rt on rt.id = ji.reminder_type_id
                                    where r.reminders_journal_id = %s and rt.out_of_accounting = True                                    
                                """
        self.env.cr.execute(get_invoice_exit_sql, (self.id,))
        invoice_ids = self.env.cr.dictfetchall()
        
        for invoice in invoice_ids:
            self.env['extraschool.refound_line'].create({'invoiceid': invoice['invoice_id'],
                                                         'date': datetime.date.today(),
                                                         'description': _("exit from accounting"),
                                                         'amount': invoice['balance'],
                                                         'reminder_id': invoice['reminder_id']
                                                         })
            
        #update biller summary
        get_biller_summary_sql = """select distinct(i.biller_id) as biller_id,sum(balance) as reminder_amount,
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
            self.env['extraschool.reminders_journal_biller_item']. create({'name': "%s - %s" % (self.name,biller_summary['reminder_amount']),
                                                                           'reminders_journal_id': self.id,
                                                                           'biller_id': biller_summary['biller_id'],
                                                                           'reminder_amount': biller_summary['reminder_amount'],
                                                                           'exit_accounting_amount': biller_summary['refound_amount']})

        #
        #
        #    !!!!! COMIT !!!!
        #
        #
        self.env.cr.commit()
        self.generate_pdf()
    #    threading.Thread(target=self.go, args=(id, uid, self.reminder_ids.ids)).start()
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
        # Todo: Do this in a proper way.
        super(extraschool_remindersjournal, self).unlink()
    
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
    


        
