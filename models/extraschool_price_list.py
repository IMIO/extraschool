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
from openerp.exceptions import Warning


class extraschool_price_list(models.Model):
    _name = 'extraschool.price_list'
    _description = 'Activities price list'
    _inherit = 'mail.thread'

    name = fields.Char('Name')
    price_list_version_ids = fields.One2many('extraschool.price_list_version', 'price_list_id', string='Versions',
                                             copy=True)

    def get_price(self, price_list, presta_date):
        price_list_obj = self.env['extraschool.price_list_version']
        ids = price_list_obj.search([('price_list_id', '=', price_list.price_list_version_ids.id),
                                     ('validity_from', '<=', presta_date),
                                     ('validity_to', '>=', presta_date),
                                     ])
        return ids if ids else False


class extraschool_price_list_version(models.Model):
    _name = 'extraschool.price_list_version'
    _description = 'Activities price list version'
    _order = 'validity_to'
    _inherit = 'mail.thread'

    name = fields.Char('Name', track_visibility='onchange')
    price_list_id = fields.Many2one('extraschool.price_list', 'Price list', ondelete='cascade',
                                    track_visibility='onchange')
    validity_from = fields.Date('Validity from', track_visibility='onchange')
    validity_to = fields.Date('Validity to', track_visibility='onchange')
    activity_ids = fields.Many2many('extraschool.activity', 'extraschool_activity_pricelist_rel', string='Activity',
                                    track_visibility='onchange')
    child_type_ids = fields.Many2many('extraschool.childtype', 'extraschool_childtype_pricelist_rel',
                                      string='Child type', track_visibility='onchange')
    child_position_ids = fields.Many2many('extraschool.childposition', 'extraschool_childposition_pricelist_rel',
                                          string='Child position', track_visibility='onchange')
    period_duration = fields.Integer('Period Duration', help='La durée de la période se calcule en minute',
                                     track_visibility='onchange', default=1)
    period_tolerance = fields.Integer('Period Tolerance',
                                      help='Si l\'on met une tolérance à 2, cela permet de pas facturer 120 minutes si l\'enfant est resté 62 minutes',
                                      track_visibility='onchange')
    price = fields.Float('Price', digits=(7, 3), help='Prix par durée définie ci-dessus', track_visibility='onchange')
    max_price = fields.Float('Max price', digits=(7, 3), default=0, track_visibility='onchange')
    # is_max_price_related_to_activity = fields.Boolean(default=False)
    # activity_for_max_price = fields.Many2one(comodel_name="extraschool.activity", string="Activity for max price")

    @api.model
    def create(self, vals):
        if (vals['period_duration'] == 0):
            raise Warning(_("The period must be higher than 0"))
        else:
            return super(extraschool_price_list_version, self).create(vals)
