# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
#    Jenny Pans - Imio (<http://www.imio.be>).
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


class extraschool_address(models.Model):
    _name = 'extraschool.address'
    _rec_name = 'full'

    number = fields.Char(string='Number')
    street = fields.Char(string='Street')
    zip_code = fields.Char(string='Zip code')
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country', string='Country', default=21)
    full = fields.Char(compute='_compute_address', string='Full address')

    @api.multi
    def _compute_address(self):
        for address in self:
            address.full = ''.join(
                (address.number, ' ', address.street, ' ', address.zip_code, ' ', address.city, ' ',
                 address.country_id.name))
