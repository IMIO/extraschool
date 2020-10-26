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

from openerp import models, fields


class extraschool_report(models.Model):
    _name = 'extraschool.report'
    _description = 'Report'
    _order = 'name'

    name = fields.Char('Name', size=50, required=True)
    report_type_id = fields.Many2one(comodel_name='ir.actions.report.xml', string='Report type', required=True)
    inline_report_ids = fields.One2many(comodel_name='extraschool.inline_report', inverse_name='report_id',
                                        ondelete='cascade', copy=True)
    paper_format_id = fields.Many2one(comodel_name='report.paperformat', string='Paper format', required=True)
