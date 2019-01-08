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

from openerp import models, api, fields, _

class extraschool_organising_power(models.Model):
    _name = 'extraschool.organising_power'
    _description = 'Organising Power that contains all activities'

    activity_category_ids = fields.One2many('extraschool.activitycategory', 'organising_power_id', 'Activity Category')
    town = fields.Char('Name of the town', required=True)
    max_school_implantation = fields.Integer()
    dominant_activity_category_id = fields.Many2one('extraschool.activitycategory')

