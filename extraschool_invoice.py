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

from openerp import models, api, fields
from openerp.api import Environment
import openerp.addons.decimal_precision as dp
import datetime
import calendar

class extraschool_invoice(models.Model):
    _name = 'extraschool.invoice'
    _description = 'invoice'

    name = fields.Char('Name', size=20,readonly=True, default='Facture')
    schoolimplantationid = fields.Many2one('extraschool.schoolimplantation', 'School implantation', required=False,readonly=True)
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=False, index = True)
    invoicesendmethod = fields.Selection(related="parentid.invoicesendmethod", store=True)
    number = fields.Integer('Number',readonly=True)
    structcom = fields.Char('Structured Communication', size=50,readonly=True, index = True)
    amount_total = fields.Float(string='Amount',digits_compute=dp.get_precision('extraschool_invoice'),readonly=True, store=True)
    amount_received = fields.Float( string='Received',readonly=True,store=True)
    balance = fields.Float(compute="_compute_balance",digits_compute=dp.get_precision('extraschool_invoice'), string='Balance',readonly=True, store=True)
    no_value = fields.Float('No value',default=0.0,readonly=True)
    discount = fields.Float('Discount',readonly=True)
    biller_id = fields.Many2one('extraschool.biller', 'Biller', required=False,ondelete='cascade',readonly=True)
    filename = fields.Char('filename', size=20,readonly=True)
    invoice_file = fields.Binary('File', readonly=True)
    payment_ids = fields.One2many('extraschool.payment_reconciliation', 'invoice_id','Payments')
    invoice_line_ids = fields.One2many('extraschool.invoicedprestations', 'invoiceid','Details')    
    refound_line_ids = fields.One2many('extraschool.refound_line', 'invoiceid','Refound')    
    oldid = fields.Char('oldid', size=20)
    activitycategoryid = fields.Many2one(related='biller_id.activitycategoryid', auto_join=True)
    period_from = fields.Date(related='biller_id.period_from')
    period_to = fields.Date(related='biller_id.period_to')
    payment_term = fields.Date('Payment term')  
    comment = fields.Text("Comment",default="")
    last_reminder_id = fields.Many2one('extraschool.reminder', 'Last reminder',readonly=True, index = True)
    reminder_fees = fields.Boolean('Reminder fees', default = False)
        
#     @api.depends('invoice_line_ids')
#     def _compute_amount_total(self):
#         for invoice in self:
#             invoice.amount_total = sum(invoice_line.total_price for invoice_line in invoice.invoice_line_ids)
#             
#     @api.onchange('payment_ids')
#     @api.depends('payment_ids')
#     def _compute_amount_received(self):
#         for invoice in self:
#             invoice.amount_received = sum(reconcil_line.amount for reconcil_line in invoice.payment_ids)

#    @api.depends('amount_total' ,'amount_received')
    def _compute_balance(self):
        for invoice in self:

            total = 0 if len(invoice.invoice_line_ids) == 0 else sum(line.total_price for line in invoice.invoice_line_ids)
            reconcil = 0 if len(invoice.payment_ids) == 0 else sum(reconcil_line.amount for reconcil_line in invoice.payment_ids) 
            refound = 0 if len(invoice.refound_line_ids) == 0 else sum(refound_line.amount for refound_line in invoice.refound_line_ids)
            balance = total - reconcil - refound
            balance = 0 if balance == 0 or balance < 0 else total - reconcil - refound
            
            invoice.write({'amount_total' : total,
                           'amount_received' : reconcil,
                           'no_value' : refound,
                           'balance' : balance
                           })
            
    @api.multi
    def get_today(self):
        print datetime.datetime.now().strftime("%y-%m-%d")
        return datetime.datetime.now().strftime("%y-%m-%d")

    @api.multi
    def get_payment_term_str(self):
        print self.payment_term.strftime("%y-%m-%d")
        return self.payment_term.strftime("%y-%m-%d")
    
    @api.multi
    def is_echue(self):        
        return True if self.payment_term < fields.Datetime.now() else False
    
    
    @api.multi
    def reconcil(self):
        payment_obj = self.env['extraschool.payment']
        payment_reconcil_obj = self.env['extraschool.payment_reconciliation']
        self._compute_balance()
        for invoice in self:
            #search for open payment
            payments = payment_obj.search([('parent_id','=',invoice.parentid.id),
                                        ('structcom_prefix','=',invoice.activitycategoryid.payment_invitation_com_struct_prefix),
                                        ('solde','>',0),
                                        ]).sorted(key=lambda r: r.paymentdate)
#            print "%s payments found for invoice %s" % (len(payments),invoice.id)
#            print payments
            zz = 0
            print "invoice balance = %s" % (invoice.amount_total)
            
            solde = invoice.balance
            while zz < len(payments) and solde > 0:
                amount = solde if payments[zz].solde >= solde else payments[zz].solde
                print "Add payment reconcil - amount : %s" % (amount)
                payment_reconcil_obj.create({'payment_id': payments[zz].id,
                                         'invoice_id': invoice.id,
                                         'amount': amount,
                                         'date': fields.Date.today(),
                                         })
                solde -= amount
                zz += 1
            
            invoice._compute_balance()
            
    def get_concerned_short_name(self):
        res = []
        
        for line in self.invoice_line_ids:
            if line.activity_activity_id.short_name not in res:
                res.append(line.activity_activity_id.short_name)
                
        return res

            
    def get_concerned_child(self):
        res = []
        
        for line in self.invoice_line_ids:
            if line.childid not in res:
                res.append(line.childid)
                
        return res

           
    def get_invoice_calendar(self, child_id = None):
        print "child:%s" % (child_id)
        concened_months = self.biller_id.get_concerned_months()
        for month in concened_months:
            month['days'] = calendar.monthcalendar(month['year'], month['month'])
            month['activity'] = self.get_concerned_short_name()
            month['quantity'] = []
            zz=0
            for week in month['days']:
                month['quantity'].append([])
                
                for d in week:
                    d={'day_id': d,
                       'quantity': [],
                       }
                    print "%s" % (self.period_from)
                    for activity in month['activity']:                        
                        d['quantity'].append(sum(self.invoice_line_ids.filtered(lambda r: r.childid.id == child_id 
                                                                                and r.prestation_date == '%s-%02d-%02d' % (month['year'],month['month'],d['day_id']) 
                                                                                and r.activity_activity_id.short_name == activity).mapped('quantity')))
                    month['quantity'][zz].append(d)
                
                zz+=1
                        
        print concened_months 
        
        return concened_months

            
