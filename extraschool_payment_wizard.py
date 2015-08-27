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
import cStringIO
import base64
import os
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschool_payment_wizard(models.TransientModel):
    _name = 'extraschool.payment_wizard'

    
    payment_type = fields.Selection((('1','Prepaid'),
                                    ('2','Invoice'),
                                    ),'Payment type', required=True)
    payment_date = fields.Date('Date', required=True)
    amount = fields.Float('Amount', required=True)
    reconciliation_amount_balance = fields.Float(compute="_compute_reconciliation_amount_balance", string='Amount to reconcil')    
    reconciliation_amount = fields.Float(compute="_compute_reconciliation_amount", string='Amount reconcilied')
    parent_id = fields.Many2one("extraschool.parent")
    activity_category_id = fields.Many2one("extraschool.activitycategory")
    payment_reconciliation_ids = fields.One2many('extraschool.payment_wizard_reconcil','payment_wizard_id')

    state = fields.Selection([('init', 'Init'),
                             ('print_payment', 'Print payment'),
                             ('print_reconciliation', 'Print reconciliation')],
                            'State', required=True, default='init'
                            )

    @api.onchange('payment_type','amount','activity_category_id')
    @api.one
    def _on_change_payment_type(self):
        
        self.payment_reconciliation_ids = [(5, 0, 0)]
        print "self.activity_category_id : %s" % (self.activity_category_id)
        reconciliations = []
        if self.payment_type == '1':
            if len(self.activity_category_id):
                reconciliations = self.env['extraschool.payment']._get_reconciliation_list(self.parent_id.id,self.activity_category_id.payment_invitation_com_struct_prefix,self.payment_type,self.amount)
        else:
                reconciliations = self.env['extraschool.payment']._get_reconciliation_list(self.parent_id.id,self.activity_category_id.payment_invitation_com_struct_prefix,self.payment_type,self.amount)
            
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


    @api.model
    def default_get(self,fields):
        print "----------------"
        print "context : %s" % (self.env.context,)
        print "----------------"
        print "fields : %s" % (fields,)
        print "----------------"
        print "return : %s" % {'parent_id': self.env.context.get('parent_id'),}
        return {'state': 'init',
                'parent_id': self.env.context.get('parent_id'),}

    @api.multi
    def next(self):

        #check if reconcil amount on line is never greater than balance
        print "************************"
        zz = 0
        for r in self.payment_reconciliation_ids:
            if r.amount > r.invoice_balance : 
                zz += 1
                
        print str(self.payment_reconciliation_ids.ids)
        
        print "************************"
        
        if zz:
            raise Warning("At least one reconciliation line is not correct : amount greater than balance")
        self.create_payment()

    @api.multi
    def create_payment(self):
        payment = self.env['extraschool.payment']
        payment = payment.create({'parent_id': self.parent_id.id,
                        'paymentdate': self.payment_date,
                        'structcom_prefix': self.activity_category_id.payment_invitation_com_struct_prefix,
                        'amount': self.amount})
        
        payment_reconciliation = self.env['extraschool.payment_reconciliation']
        for reconciliation in self.payment_reconciliation_ids:
            payment_reconciliation.create({'payment_id' : payment.id,
                                           'invoice_id' : reconciliation.invoice_id.id,
                                           'amount' : reconciliation.amount})
        return {}
         
class extraschool_payment_wizard_reconcil(models.TransientModel):
    _name = 'extraschool.payment_wizard_reconcil'

    payment_wizard_id = fields.Many2one("extraschool.payment_wizard")
    invoice_id = fields.Many2one("extraschool.invoice")
    invoice_balance = fields.Float(related="invoice_id.balance", string = "Balance")
    amount = fields.Float('Amount', required=True)
    
