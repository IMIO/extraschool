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


class extraschool_inline_report(models.Model):
    _name = 'extraschool.inline_report'
    _description = 'Report'
    _order = 'section asc,sequence asc'

    name = fields.Char('Name', size=50, required=True)
    report_id = fields.Many2one(comodel_name='extraschool.report', string='Report', ondelete='cascade')
    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list.")
    inline_report_id = fields.Many2one(comodel_name='ir.ui.view', string='Report', required=True, ondelete='cascade')
    section = fields.Selection([('a_header', 'Header'),
                                ('b_body', 'Body'),
                                ('c_footer', 'Footer'), ], required=True)
    page_break_after = fields.Boolean(string="Page break after", default=False)
    visibility = fields.Selection([('hide_firstpage', 'Hidden on first page'), ('show_firstpage', 'First page only'),
                                   ('show_lastpage', 'Last page only'), ])
    verso = fields.Boolean(default=False)