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
from openerp import models, api, fields,_
from openerp.api import Environment
from datetime import date, datetime, timedelta as td
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)

class extraschool_reminder(models.Model):
    _name = 'extraschool.reminder'
    _description = 'Reminder'


    reminders_journal_item_id = fields.Many2one('extraschool.reminders_journal_item', 'Reminders journal item',ondelete='cascade', required=False)
    reminders_journal_id = fields.Many2one('extraschool.remindersjournal', 'Reminders journal', ondelete='cascade', required=False)    
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=False)
    remindersendmethod = fields.Selection(related="parentid.remindersendmethod", store=True)
    amount = fields.Float('Amount', digits=(7,2))
    structcom = fields.Char('Structured Communication', size=50)
    school_implantation_id = fields.Many2one('extraschool.schoolimplantation', 'School implantation', required=False)
    concerned_invoice_ids = fields.Many2many('extraschool.invoice','extraschool_reminder_invoice_rel', 'reminder_id', 'invoice_id','Concerned invoices')
    activity_category_id = fields.Many2one(related='reminders_journal_id.activity_category_id', string='Activity Category')
    payment_term = fields.Date('reminders_journal_item_id.payment_term')
    transmission_date = fields.Date('reminders_journal_id.transmission_date')
    fees_amount = fields.Integer(default=0.0)
