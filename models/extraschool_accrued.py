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


class extraschoolAccrued(models.Model):
    _name = 'extraschool.accrued'
    _description = 'Droit constatés'

    biller_id = fields.Many2one('extraschool.biller')
    activity_category_id = fields.Many2one('extraschool.activitycategory')
    amount = fields.Float()
    ref = fields.Char()
    amount_received = fields.Float(compute='_compute_amount_received')

    @api.multi
    def get_invoiced_prestations(self):
        invoices = self.biller_id.invoice_ids.filtered(lambda r: r.balance == 0 and r.amount_received > 0)
        invoiced_prestations = []
        for invoice in invoices:
            invoiced_prestations += invoice.invoice_line_ids.filtered(
                lambda r: r.activity_activity_id.category_id == self.activity_category_id)
        return invoiced_prestations

    @api.multi
    def _compute_amount_received(self):
        if len(self) > 1:
            for rec in self:
                invoiced_prestations = rec.get_invoiced_prestations()
                amount_received = 0
                for invoiced_prestation in invoiced_prestations:
                    no_value_amount = invoiced_prestation.no_value_amount
                    total_price = invoiced_prestation.total_price
                    discount_value = invoiced_prestation.discount_value
                    if no_value_amount < total_price:
                        amount_received += (total_price - discount_value)
                        if no_value_amount > 0.0:
                            amount_received -= no_value_amount
                rec.amount_received = amount_received
