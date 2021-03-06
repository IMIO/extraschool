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

    def _get_activity_category_id(self):
        return self.env['extraschool.activitycategory'].search([]).filtered('id').id

    name = fields.Char('name', required=True)
    sequence = fields.Integer('Order')
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity category', default=_get_activity_category_id)
    fees_type = fields.Selection([('free','Free'),('fix','Fixed amount'),], 'Reminder cost type',required=True)
    fees_amount = fields.Float('Fees amount')
    fees_description = fields.Char('Fees description')
    mail_template_id = fields.Many2one('email.template', 'Email template')
    report_id = fields.Many2one('extraschool.report', 'Document report')
    text = fields.Text('Text')
    select_reminder_type = fields.Boolean(string='Select a reminder type')
    selected_type_id = fields.Many2one('extraschool.remindertype', 'Reminder type to select')
    delay = fields.Integer('Delay')
    payment_term_in_day = fields.Integer('payment_term_in_day')
    minimum_balance = fields.Float('Minimum balance', default=0.01)
    out_of_accounting = fields.Boolean(string="Out of accounting")
    
    @api.onchange('out_of_accounting')
    def onchange_week(self):    
        self.fees_type = 'free'
        self.fees_amount = 0
        self.fees_description = False
    
    
         

