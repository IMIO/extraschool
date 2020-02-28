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
from openerp.exceptions import Warning


class extraschool_move_prepaiement(models.TransientModel):
    _name = 'extraschool.move_prepaiement'
    _description = 'Move prepaiement'

    categ_id = fields.Many2one('extraschool.activitycategory', 'Category', required=True)
    amount = fields.Float('Price', digits=(7, 2), help='Prix à mouvementer')

    @api.multi
    def move(self):

        activity = self._context.get('default_activity_category_id')
        if self.amount > self._context.get('default_solde'):
            raise Warning('Le montant indiqué est plus grand que le montant du prépaiement')
        else:

            self.categ_id.solde =  self.amount
            self.amount = self.amount - self._context.get('default_solde')
            parent = self.env['extraschool.parent'].browse(self._context.get('default_parent_id'))
            print parent.name
            #self.env['extraschool.parent'].search([('id', '=', self._context.get('default_parent_id')),
                        #                              ('payment_status_ids.activity_category_id', '=', activity)]).write(
                # {'payment_status_ids.solde': self.amount})
            #self.env['extraschool.parent'].search([('id', '=', self._context.get('default_parent_id')),
                                                 #     ('payment_status_ids.activity_category_id', '=', self.categ_id)]).write(
               # {'payment_status_ids.solde': self.categ_id.solde})

