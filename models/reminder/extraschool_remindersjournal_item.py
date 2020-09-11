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


class extraschool_remindersjournal_item(models.Model):
    _name = 'extraschool.reminders_journal_item'
    _description = 'Reminders journal item'

    name = fields.Char('Name', required=True)
    reminder_type_id = fields.Many2one(comodel_name='extraschool.remindertype', string='Reminder type', required=True)
    reminders_journal_id = fields.Many2one(comodel_name='extraschool.remindersjournal', string='Reminder journal',
                                           ondelete='cascade',
                                           required=True)
    payment_term = fields.Date('Payment term', required=True)
    amount = fields.Float('Amount', required=True)
