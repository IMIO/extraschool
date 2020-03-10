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
    received_amount = fields.Float(compute="_compute_received_amount")

    def _compute_received_amount(self):
        import wdb; wdb.set_trace()
        for rec in self:
            rec.received_amount = 0
            invoices = self.env['extraschool.invoice'].search([('biller_id', '=', rec.biller_id.id),
                                                               ('balance', '=', 0.0)])
            for invoice in invoices:
                rec.received_amount += invoice.amount_received
            # obtenir toutes les factures dont le solde est == 0
            # obtenir toutes les factures de la catégorie d'activité de accrued
            # faire la somme du montant perçu

