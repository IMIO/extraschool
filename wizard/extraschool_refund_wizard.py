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


class extraschool_refund_wizard(models.TransientModel):
    _name = 'extraschool.refund_wizard'

    amount = fields.Float(string='Amount to refund', required=True)
    comment = fields.Char(string='Comment about the refund', required=True)

    @api.multi
    def refund(self):
        if self.amount > round(self._context.get('amount'), 3):
            raise Warning(_('You cannot refund more than the actual amount'))
        elif self.amount < 0.01:
            raise Warning(_('Please input a number greater than 0.01'))
        else:
            if self.amount == round(self._context.get('amount'), 3):
                self.env['extraschool.payment'].search(
                    [('id', '=', self._context.get('payment_id'))]).refund += self._context.get('amount')
            else:
                self.env['extraschool.payment'].search(
                    [('id', '=', self._context.get('payment_id'))]).refund += self.amount
            comment = self.env['extraschool.payment'].search([('id', '=', self._context.get('payment_id'))]).comment
            if comment:
                self.env['extraschool.payment'].search([('id', '=', self._context.get('payment_id'))]).comment += \
                    self.env['extraschool.helper'].add_date_user(self.comment)
            else:
                self.env['extraschool.payment'].search([('id', '=', self._context.get('payment_id'))]).comment = \
                    self.env['extraschool.helper'].add_date_user(self.comment)

            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
