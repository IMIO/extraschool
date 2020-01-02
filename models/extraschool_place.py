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

from odoo import models, api, fields


class extraschool_place(models.Model):
    _name = 'extraschool.place'
    _description = 'Schoolcare Place'
    _inherit = 'mail.thread'

    active = fields.Boolean('Active', default=True, track_visibility='onchange')
    name = fields.Char('Name', size=50, track_visibility='onchange')
    street = fields.Char('Street', size=50, track_visibility='onchange')
    zipcode = fields.Char('ZipCode', size=6, track_visibility='onchange')
    city = fields.Char('City', size=50, track_visibility='onchange')
    schoolimplantation_ids = fields.Many2many('extraschool.schoolimplantation','extraschool_place_schoolimplantation_rel', 'place_id', 'schoolimplantation_id','School implantations')
    schedule = fields.Text('Schedule')
    street_code = fields.Char('Street Code') # onyx
    oldid = fields.Integer('oldid')

extraschool_place()
