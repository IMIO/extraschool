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


class extraschool_main_settings(models.Model):
    _inherit = 'res.config.settings'
    _name = 'extraschool.main_settings'

    lastqrcodenbr = fields.Integer('lastqrcodenbr')


class extraschool_one_settings(models.Model):
    _inherit = 'res.config.settings'
    _name = 'extraschool.onereport_settings'

    name = fields.Char("Name" , required=True, default="One report template")
    validity_from = fields.Date("Validity from")
    validity_to = fields.Date("Validity to")
    report_template = fields.Binary("Report template")
    one_logo = fields.Binary("ONE logo")

