# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Michael Colicchia - Imio (<http://www.imio.be>).
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
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschoolNoValueWizard(models.TransientModel):
    _name = 'extraschool.no_value_wizard'

    def _get_invoiced_prestation(self):
        invoiced_prestation_ids =  self.env['extraschool.invoicedprestations'].search([
            ('invoiceid', 'in', self.env.context.get('active_ids'))
        ])

        for invoiced_prestation in invoiced_prestation_ids:
            invoiced_prestation.on_tax_certificate = invoiced_prestation.activity_activity_id.on_tax_certificate

        return invoiced_prestation_ids

    description = fields.Text(
        string='Description'
    )
    invoice_prestation_ids = fields.Many2many(
        'extraschool.invoicedprestations',
        string='Invoiced prestations',
        default=_get_invoiced_prestation,
    )
    date_no_value = fields.Date(
        string='Date of no value'
    )
    amount = fields.Float(
        string='Amount of no value'
    )

    @api.onchange('amount')
    def _on_change_no_value(self):
        if self.amount > sum(x.total_price for x in self.invoice_prestation_ids):
            raise Warning(_("The amount of no value must at least equal or less than the total amount"))
