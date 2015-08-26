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

class extraschool_invoice(models.Model):
    _name = 'extraschool.invoice'
    _description = 'invoice'

    name = fields.Char('Name', size=20,readonly=True, default='Facture')
    schoolimplantationid = fields.Many2one('extraschool.schoolimplantation', 'School implantation', required=False,readonly=True)
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=False, index = True)
    number = fields.Integer('Number',readonly=True)
    structcom = fields.Char('Structured Communication', size=50,readonly=True, index = True)
    amount_total = fields.Float('Amount',readonly=True)
    amount_received = fields.Float(compute="_compute_amount_received", string='Received',readonly=True,store=True)
    balance = fields.Float(compute="_compute_balance",string='Balance',readonly=True, store=True)
    no_value = fields.Float('No value',readonly=True)
    discount = fields.Float('Discount',readonly=True)
    biller_id = fields.Many2one('extraschool.biller', 'Biller', required=False,ondelete='cascade',readonly=True)
    filename = fields.Char('filename', size=20,readonly=True)
    invoice_file = fields.Binary('File', readonly=True)
    payment_ids = fields.One2many('extraschool.payment_reconciliation', 'invoice_id','Payments')
    invoice_line_ids = fields.One2many('extraschool.invoicedprestations', 'invoiceid','Details')    
    oldid = fields.Char('oldid', size=20)
    activitycategoryid = fields.Many2one(related='biller_id.activitycategoryid')
    period_from = fields.Date(related='biller_id.period_from')
    period_to = fields.Date(related='biller_id.period_to')
    payment_term = fields.Date(related='biller_id.payment_term')  
        

    @api.onchange('payment_ids')
    @api.depends('payment_ids')
    def _compute_amount_received(self):
        for invoice in self:
            invoice.amount_received = sum(reconcil_line.amount for reconcil_line in invoice.payment_ids)

    @api.depends('amount_received')
    def _compute_balance(self):
        for invoice in self:
            invoice.balance = invoice.amount_total - invoice.amount_received
