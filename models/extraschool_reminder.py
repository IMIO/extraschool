# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
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

from openerp import models, api, fields,_
import openerp.addons.decimal_precision as dp
from datetime import date, datetime, timedelta as td


class extraschool_reminder(models.Model):
    _name = 'extraschool.reminder'
    _description = 'Reminder'

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        res = []
        for reminder in self.browse(cr, uid, ids, context=context):
            res.append((reminder.id, reminder.parentid.name))
        return res

    reminders_journal_item_id = fields.Many2one('extraschool.reminders_journal_item', 'Reminders journal item',ondelete='cascade', required=False)
    reminders_journal_id = fields.Many2one('extraschool.remindersjournal', 'Reminders journal', ondelete='cascade', required=False)
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=False)
    remindersendmethod = fields.Selection(related="parentid.remindersendmethod", store=True)
    #todo mettre à jour
    amount = fields.Float('Amount',digits_compute=dp.get_precision('extraschool_reminder'),readonly=True, store=True)
    structcom = fields.Char('Structured Communication', size=50)
    school_implantation_id = fields.Many2one('extraschool.schoolimplantation', 'School implantation', required=False)
    concerned_invoice_ids = fields.Many2many('extraschool.invoice','extraschool_reminder_invoice_rel', 'reminder_id', 'invoice_id','Concerned invoices')
    # activity_category_id = fields.Many2one(related='reminders_journal_id.activity_category_id', string='Activity Category')
    activity_category_ids = fields.Many2many(related='reminders_journal_id.activity_category_ids', string='Activities Category')
    payment_term = fields.Date('reminders_journal_item_id.payment_term')
    transmission_date = fields.Date('reminders_journal_id.transmission_date')
    fees_amount = fields.Integer(default=0.0)
    balance = fields.Float('Solde',digits_compute=dp.get_precision('extraschool_reminder'),readonly=True, store=True)
    amount_received = fields.Float(string='Received', compute='_get_amount_received',
                                   readonly=True)

    @api.multi
    def _get_amount_received(self):
        for reminder in self :
            reminder.amount_received = reminder.amount - reminder.balance

    @api.multi
    def get_date(self, invoice_ids):
        dates = invoice_ids.filtered(lambda r : r.biller_id.period_from)
        return " %s au %s" % (datetime.strptime(dates[0].biller_id.period_from, '%Y-%m-%d').strftime('%d-%m-%Y'),
                              datetime.strptime(dates[-1].biller_id.period_to, '%Y-%m-%d').strftime('%d-%m-%Y'))
