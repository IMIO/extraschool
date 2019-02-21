# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Colicchia Michael - Imio (<http://www.imio.be>).
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
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import tools
from datetime import datetime

class extraschool_annual_report(models.Model):
    _name = 'extraschool.annual_report'

    annual_report_item_ids = fields.One2many('extraschool.annual_report_item', 'annual_report_id', 'Items')
    year = fields.Char(default=datetime.now().year - 1, string='Inscrivez l\'année souhaitée')
    total_amount = fields.Float(string='Montant total')
    total_reconcil_amount = fields.Float(string='Montant total réconcilié')
    total_reconcil_no_fees = fields.Float(string='Total sans les frais de rappels')
    total_fees = fields.Float(string='Montant total des frais de rappels')

    @api.onchange('year')
    @api.multi
    def compute_annual_report(self):
        total_payment_ids = self.env['extraschool.payment'].search([
            ('paymentdate', '>=', '{}-01-01'.format(self.year)),
            ('paymentdate', '<=', '{}-12-31'.format(self.year)),
        ])

        total_reconcil_ids = self.env['extraschool.payment_reconciliation'].search([
            ('paymentdate', '>=', '{}-01-01'.format(self.year)),
            ('paymentdate', '<=', '{}-12-31'.format(self.year)),
        ])

        total_reconcil = total_reconcil_ids.filtered(lambda r: r.invoice_id.no_value == 0)

        self.total_amount = sum(amount.amount for amount in total_payment_ids)

        self.total_reconcil_amount = sum(amount.amount for amount in total_reconcil)

        total_reconcil_no_fees = total_reconcil_ids.filtered(lambda r: r.invoice_id.no_value == 0)

        self.total_reconcil_no_fees = sum(amount.amount for amount in total_reconcil_no_fees.filtered(lambda r: r.invoice_id.reminder_fees == False))

        self.total_fees = self.total_reconcil_amount - self.total_reconcil_no_fees

        data = {}

        for reconcil_id in total_reconcil:
            if not reconcil_id.biller_id.id in data.keys():
                data[reconcil_id.biller_id.id] = [reconcil_id.amount]
            else:
                data[reconcil_id.biller_id.id].append(reconcil_id.amount)

        item_ids = []

        for id in data.keys():
            total = sum(data[id])
            if total:
                item_ids.append((0, 0, {
                    'biller_id': id,
                    'date': self.env['extraschool.biller'].browse(id).period_from,
                    'amount': total,
                }))

        self.annual_report_item_ids = item_ids



class extraschool_annual_report_item(models.TransientModel):
    _name = 'extraschool.annual_report_item'
    _order = 'date'

    annual_report_id = fields.Many2one('extraschool.annual_report')
    biller_id = fields.Many2one('extraschool.biller', string='Facturier')
    date = fields.Date()
    ref = fields.Char(related='biller_id.other_ref')
    amount = fields.Float()
