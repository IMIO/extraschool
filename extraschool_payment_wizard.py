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
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp
from openerp.tools import float_compare, float_round



class extraschool_payment_wizard(models.TransientModel):
    _name = 'extraschool.payment_wizard'

    '''
    payment_type = fields.Selection((('1','Prepaid'),
                                    ('2','Invoice'),
                                    ),'Payment type', required=True)
    '''
    payment_date = fields.Date('Date', required=True)
    amount = fields.Float('Amount', digits_compute=dp.get_precision('extraschool_invoice'), required=True)
    reconciliation_amount_balance = fields.Float(compute="_compute_reconciliation_amount_balance", string='Amount to reconcil')    
    reconciliation_amount = fields.Float(compute="_compute_reconciliation_amount", string='Amount reconcilied')
    parent_id = fields.Many2one("extraschool.parent")
    activity_category_id = fields.Many2one("extraschool.activitycategory")
    payment_reconciliation_ids = fields.One2many('extraschool.payment_wizard_reconcil','payment_wizard_id')
    reject_id = fields.Many2one('extraschool.reject', string='Reject')
    comment = fields.Char('Comment')
    state = fields.Selection([('init', 'Init'),
                             ('print_payment', 'Print payment'),
                             ('print_reconciliation', 'Print reconciliation')],
                            'State', required=True, default='init'
                            )
    
    @api.onchange('parent_id','amount','activity_category_id')
    @api.one
    def _on_change_payment_type(self):
        
        self.payment_reconciliation_ids = [(5, 0, 0)]
        print "self.activity_category_id : %s" % (self.activity_category_id)
        reconciliations = []
        if len(self.activity_category_id) and self.parent_id:
            reconciliations = self.env['extraschool.payment']._get_reconciliation_list(self.parent_id.id,self.activity_category_id.payment_invitation_com_struct_prefix,1,self.amount)
            
        tmp_payment_reconciliation_ids = []
        for reconciliation in reconciliations:           
            tmp_payment_reconciliation_ids.append((0,0,reconciliation))
            
        print "reconcil : %s" % (tmp_payment_reconciliation_ids)
        self.payment_reconciliation_ids = tmp_payment_reconciliation_ids
    

    @api.onchange('reconciliation_amount')
    @api.depends('reconciliation_amount')
    def _compute_reconciliation_amount_balance(self):
        for payment in self:
            payment.reconciliation_amount_balance = payment.amount - payment.reconciliation_amount

    @api.onchange('payment_reconciliation_ids')
    @api.depends('payment_reconciliation_ids')
    def _compute_reconciliation_amount(self):
        for payment in self:
            payment.reconciliation_amount = sum(reconcil_line.amount for reconcil_line in payment.payment_reconciliation_ids)


#     @api.model
#     def default_get(self,fields):
#         print "default_get"
#         print {'state': 'init',
#                 'parent_id': self.env.context.get('parent_id'),
#                 'reject_id': self.env.context.get('reject_id'),
#                 'amount': self.env.context.get('amount'),}
# 
#         return {'state': 'init',
#                 'parent_id': self.env.context.get('parent_id'),
#                 'reject_id': self.env.context.get('reject_id'),
#                 'amount': self.env.context.get('amount'),}

    @api.multi
    def next(self):
        self.payment_reconciliation_ids = [(5, 0, 0)]
        print "self.activity_category_id : %s" % (self.activity_category_id)
        reconciliations = []
        if len(self.activity_category_id):
            reconciliations = self.env['extraschool.payment']._get_reconciliation_list(self.parent_id.id,self.activity_category_id.payment_invitation_com_struct_prefix,1,self.amount)
        
        tmp_payment_reconciliation_ids = []
        for reconciliation in reconciliations:           
            tmp_payment_reconciliation_ids.append((0,0,reconciliation))
            
        print "reconcil : %s" % (tmp_payment_reconciliation_ids)
        self.payment_reconciliation_ids = tmp_payment_reconciliation_ids
        #check if reconcil amount on line is never greater than balance
        zz = 0
        total = 0
        print "*********"
        for r in self.payment_reconciliation_ids:
            total += r.amount
            print "total = %s, amount = %s" % (r.amount,r.invoice_balance)
            if float_compare(r.amount,r.invoice_balance,2) > 0  : 
                print "boum !!"
                zz += 1             
        
        if zz:
            print "At least one reconciliation line is not correct : amount greater than balance"
            raise Warning(_("At least one reconciliation line is not correct : amount greater than balance"))
        
        '''
        #if invoice payment amount reconcil MUST be equal to payment amount
        print "type: %s amount: %s total: %s" % (self.payment_type,self.amount,total)
        if self.payment_type == '2' and total != self.amount:
            print "Reconcil amount MUST be equal to payment amount"
            raise Warning(_("Reconcil amount MUST be equal to payment amount"))
        '''
        
        #Amount must be >= reconcil
        if total - self.amount >= 0.0000001:
            print "--- total: %s amount: %s diff : %s---" % (total,self.amount,total-self.amount)
            print "Reconcil amount MUST be less than payment amount"
            raise Warning(_("Reconcil amount MUST be less than payment amount"))
        
        
        self.create_payment()

    @api.multi
    def create_payment(self):
        payment = self.env['extraschool.payment']
        print "-------------------"
        print self.reject_id
        print "-------------------"
        
        payment = payment.create({'parent_id': self.parent_id.id,
                        'paymentdate': self.payment_date,
                        'structcom_prefix': self.activity_category_id.payment_invitation_com_struct_prefix,
                        'amount': self.amount,
                        'reject_id': self.reject_id.id if self.reject_id else False,
                        'comment': self.comment})
        
        if self.reject_id:
            self.env['extraschool.reject'].browse(self.reject_id.id).corrected_payment_id = payment.id
        
        print "payment id : %s" % (payment.id)
        
        payment_reconciliation = self.env['extraschool.payment_reconciliation']
        for reconciliation in self.payment_reconciliation_ids:
            payment_reconciliation.create({'payment_id' : payment.id,
                                           'invoice_id' : reconciliation.invoice_id.id,
                                           'amount' : reconciliation.amount,
                                           'date' : fields.Date.today()})
            reconciliation.invoice_id._compute_balance()
        return {}
         
class extraschool_payment_wizard_reconcil(models.TransientModel):
    _name = 'extraschool.payment_wizard_reconcil'

    payment_wizard_id = fields.Many2one("extraschool.payment_wizard")
    invoice_id = fields.Many2one("extraschool.invoice")
    invoice_balance = fields.Float(related="invoice_id.balance", string = "Balance")
    amount = fields.Float('Amount', digits_compute=dp.get_precision('extraschool_invoice'), required=True)
    
