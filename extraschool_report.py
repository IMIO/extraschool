# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014 
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot - Imio (<http://www.imio.be>).
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

from openerp import models, api, fields
from openerp.api import Environment

class extraschool_report(models.Model):
    _name = 'extraschool.report'
    _description = 'Report'
    _order = 'name'

    name = fields.Char('Name', size=50, required=True)
    report_type_id = fields.Many2one('ir.actions.report.xml', 'Report type', required=True)
    inline_report_ids = fields.Many2many('extraschool.inline_report','extraschool_report_inline_report_rel', 'report_id', 'inline_report_id','Inline reports')


class extraschool_inline_report(models.Model):
    _name = 'extraschool.inline_report'
    _description = 'Report'
    _order = 'sequence asc'


    name = fields.Char('Name', size=50, required=True)
    report_id = fields.Many2one('extraschool.report', 'Report')
    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of sales order lines.")
    inline_report_id = fields.Many2one('ir.ui.view', 'Report', required=True)
    