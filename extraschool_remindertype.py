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

class extraschool_remindertype(models.Model):
    _name = 'extraschool.remindertype'
    _description = 'Reminder type'

    name = fields.Char('name', required=True)
    sequence = fields.Integer('Order')
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity category')
    fees_type = fields.Selection([('free','Free'),('fix','Fixed amount'),], 'Reminder cost type',required=True)
    fees_amount = fields.Char('fees_amount')
    mail_template_id = fields.Many2one('email.template', 'Email template')
    report_id = fields.Many2one('extraschool.report', 'Document report')
    
    out_of_accounting = fields.Boolean(string="Out of accounting")
         

