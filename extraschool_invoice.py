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
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=False)
    number = fields.Integer('Number',readonly=True)
    structcom = fields.Char('Structured Communication', size=50,readonly=True)
    amount_total = fields.Float('Amount',readonly=True)
    amount_received = fields.Float('Received',readonly=True)
    balance = fields.Float('Balance',readonly=True)
    no_value = fields.Float('No value',readonly=True)
    discount = fields.Float('Discount',readonly=True)
    biller_id = fields.Many2one('extraschool.biller', 'Biller', required=False,ondelete='cascade',readonly=True)
    filename = fields.Char('filename', size=20,readonly=True)
    invoice_file = fields.Binary('File', readonly=True)
    payment_ids = fields.One2many('extraschool.payment', 'concernedinvoice','Payments')
    oldid = fields.Char('oldid', size=20)
    activitycategoryid = fields.Many2one('biller_id.activitycategoryid', string='Activity Category')
    period_from = fields.Date('biller_id.period_from')
    period_to = fields.Date('biller_id.period_to')
    payment_term = fields.Date('biller_id.payment_term')      


extraschool_invoice()
