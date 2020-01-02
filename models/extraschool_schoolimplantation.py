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


class extraschool_schoolimplantation(models.Model):
    _name = 'extraschool.schoolimplantation'
    _description = 'School implantation'

    name = fields.Char('Name', size=100, required=False)
    schoolid = fields.Many2one('extraschool.school', 'School', required=False)
    street = fields.Char('Street')
    zipcode = fields.Char('ZipCode')
    city = fields.Char('City')

    oldid = fields.Integer('oldid')



