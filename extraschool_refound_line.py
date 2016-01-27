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

class extraschool_refound_line(models.Model):
    _name = 'extraschool.refound_line'
    _description = 'invoiced Prestations'

    invoiceid = fields.Many2one('extraschool.invoice', 'invoice',ondelete='cascade')
    date = fields.Date(string="Date", required=False)
    description = fields.Char('Description', required=False)        
    amount = fields.Float('Amount', required=False)    
    prestation_ids = fields.One2many('extraschool.prestationtimes','invoiced_prestation_id',ondelete='restrict')        
    
    
    def confirm(self):
        print "refound confirm"
        payment_reconcil_obj = self.env['extraschool.payment_reconciliation']
        
        for refound in self:
            amount_to_refound = refound.amount - refound.invoiceid.balance
            print "amount to refound : %s" % (amount_to_refound)
            zz = len(refound.invoiceid.payment_ids) - 1
            while amount_to_refound > 0 and zz >= 0:
                print "loop : zz %s amount to refound %s" % (zz, amount_to_refound)                
                if refound.invoiceid.payment_ids[zz].amount <= amount_to_refound:
                    amount = refound.invoiceid.payment_ids[zz].amount
                else:
                    amount = amount_to_refound
                
                payment_reconcil_obj.create({'payment_id': refound.invoiceid.payment_ids[zz].payment_id.id,
                                         'invoice_id': refound.invoiceid.id,
                                         'amount': amount*(-1),
                                         })
                amount_to_refound -= amount
                zz -= 1
            refound.invoiceid._compute_balance()

    @api.model
    def create(self,vals):
        new_obj = super(extraschool_refound_line, self).create(vals)
        
        new_obj.confirm()
        
        return new_obj
    