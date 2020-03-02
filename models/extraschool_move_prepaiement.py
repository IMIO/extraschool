# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
#    Coralie Cardon & Jenny Pans - Imio (<http://www.imio.be>).
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
from openerp.exceptions import Warning


class extraschool_move_prepaiement(models.TransientModel):
    _name = 'extraschool.move_prepaiement'
    _description = 'Move prepaiement'

    categ_id = fields.Many2one('extraschool.activitycategory', 'Category', required=True)
    amount = fields.Float('Price', digits=(7, 2), help='Prix à mouvementer')

    @api.multi
    def move(self):
        if self._context.get('default_solde') == 0.0:
            raise Warning('Il n\'a pas d\'argent à transférer')
        elif self.amount == 0:
            raise Warning('Il y doit y avoir un montant à transférer')
        elif self.amount > self._context.get('default_solde'):
            raise Warning('Le montant indiqué est plus grand que le montant du prépaiement')
        else:
            payment_status_report = self.env['extraschool.payment_status_report'].browse(self._context.get('active_id'))
            parent = payment_status_report.parent_id
            activity_category = parent.payment_status_ids.search([('parent_id', '=', parent.id),
                                                                  ('activity_category_id', '=', self.categ_id.id)])
            # créer un paiement
            # modifier la valeur du paiement
            # activity_category.write({
            #     'solde': activity_category.solde + self.amount
            # })
            # payment_status_report.write({
            #     'solde': payment_status_report.solde - self.amount
            # })
