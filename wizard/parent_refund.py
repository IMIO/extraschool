# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014
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

from openerp import models, fields, api


class ParentRefund(models.TransientModel):
    _name = 'extraschool.parent_refund_wizard'

    def _get_payment(self):
        return self.env['extraschool.payment'].search([
            ('parent_id', '=', self._context.get('default_parent_id')),
            ('solde', '>', 0),
        ])

    parent_id = fields.Many2one(
        'extraschool.parent',
        string='Parent to be refund of payment',
        required=True,
    )
    payment_ids = fields.One2many(
        'extraschool.payment',
        'parent_id',
        string='List of payment available to refund',
        default=_get_payment,
        readonly=True,
    )
    amount = fields.Float(
        string='Amount of refund'
    )

    @api.multi
    def generate_refund_parent(self):
        import wdb;wdb.set_trace()
