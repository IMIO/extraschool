# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia - Imio (<http://www.imio.be>).
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
    _description = 'Non valeurs'

    invoiceid = fields.Many2one(
        'extraschool.invoice',
        'invoice',
        ondelete='cascade')
    date = fields.Date(
        string="Date",
        required=False)
    description = fields.Char(
        'Description',
        required=False)
    amount = fields.Float(
        string='Amount',
        required=False)
    prestation_ids = fields.One2many(
        'extraschool.prestationtimes',
        'invoiced_prestation_id',
        ondelete='restrict')
    reminder_id = fields.Many2one(
        'extraschool.reminder',
        'Reminder',
        ondelete='restrict')

    def confirm(self):
        payment_reconcil_obj = self.env['extraschool.payment_reconciliation']
        
        for refound in self:
            amount_to_refound = refound.amount - refound.invoiceid.balance
            zz = len(refound.invoiceid.payment_ids) - 1
            while amount_to_refound > 0 and zz >= 0:
                if refound.invoiceid.payment_ids[zz].amount <= amount_to_refound:
                    amount = refound.invoiceid.payment_ids[zz].amount
                else:
                    amount = amount_to_refound

                payment_reconcil_obj.create({'payment_id': refound.invoiceid.payment_ids[zz].payment_id.id,
                                             'invoice_id': refound.invoiceid.id,
                                             'date': self.date,
                                             'amount': amount * (-1),
                                             })
                amount_to_refound -= amount
                zz -= 1
            refound.invoiceid._compute_balance()

    @api.model
    def create(self, vals):
        new_obj = super(extraschool_refound_line, self).create(vals)
        
        new_obj.confirm()
        
        return new_obj

    @api.multi
    def unlink(self): 
        invoice_ids = []
        for refound in self:
            if refound.invoiceid.id not in invoice_ids:
                invoice_ids.append(refound.invoiceid.id)

        res = super(extraschool_refound_line, self).unlink()
              
        self.env['extraschool.invoice'].browse(invoice_ids)._compute_balance()
        
        return res
