# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Michael Colicchia & Jenny Pans - Imio (<http://www.imio.be>).
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
from math import fsum

from openerp import models, api, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschoolNoValueWizard(models.TransientModel):
    _name = 'extraschool.no_value_wizard'

    def _get_invoiced_prestation(self):
        invoiced_prestation_ids =  self.env['extraschool.invoicedprestations'].search([
            ('invoiceid', 'in', self.env.context.get('active_ids'))
        ])
        invoiced_prestation_ids = invoiced_prestation_ids.filtered(lambda r: r.total_price > 0.00)

        for invoiced_prestation in invoiced_prestation_ids:
            invoiced_prestation.on_tax_certificate = invoiced_prestation.activity_activity_id.on_tax_certificate

        return invoiced_prestation_ids

    description = fields.Text(
        string='Description',
        track_visibility='onchange',
        # required=True,
    )
    invoice_prestation_ids = fields.Many2many(
        'extraschool.invoicedprestations',
        string='Invoiced prestations',
        default=_get_invoiced_prestation,
    )
    date_no_value = fields.Date(
        string='Date of no value',
        track_visibility='onchange',
        # required=True,
    )
    amount_total = fields.Float(
        string='Amount of no value',
        readonly=True,
    )

    @api.onchange('invoice_prestation_ids')
    def _on_change_invoice_prestation(self):
        if not self._is_no_value_amount_correct():
            raise Warning(_("The amount of no value is superior of the total amount"))
        else:
            self.amount_total = round(fsum(x.no_value_amount for x in self.invoice_prestation_ids), 2)

        #invoice_id = self.env['extraschool.invoice_prestation_ids'].browse(self.env.context.get('active_ids'))

    @api.multi
    def validate(self):
        for i in self.invoice_prestation_ids:
            if i.no_value_amount > 0 :
                i.description = self.description
                i.date_no_value = self.date_no_value
        if not self._is_no_value_amount_correct():
            raise Warning(_("The amount of no value is superior of the total amount"))
        else:
            invoice_id = self.env['extraschool.invoice'].browse(self.env.context.get('active_ids'))

            invoice_id.write({
                'no_value_amount': round(fsum(x.no_value_amount for x in self.invoice_prestation_ids), 2),
            })
            invoice_id._compute_balance()

            return True

    @api.multi
    def _is_no_value_amount_correct(self):
        invoice_id = self.env['extraschool.invoice'].browse(self.env.context.get('active_ids'))
        total_no_value = round(fsum(x.no_value_amount for x in self.invoice_prestation_ids), 2)

        if total_no_value > round(fsum(x.total_price for x in self.invoice_prestation_ids), 2):
            return False
        if round(invoice_id.amount_total - invoice_id.amount_received, 2) - total_no_value < 0.00:
            return False
        for invoiced_prestation in self.invoice_prestation_ids:
            if invoiced_prestation.no_value_amount > invoiced_prestation.total_price:
                return False
        return True
