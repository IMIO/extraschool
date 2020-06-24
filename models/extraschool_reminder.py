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

from openerp import models, api, fields, _
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

    reminders_journal_item_id = fields.Many2one('extraschool.reminders_journal_item', 'Reminders journal item',
                                                ondelete='cascade', required=False)
    reminders_journal_id = fields.Many2one('extraschool.remindersjournal', 'Reminders journal', ondelete='cascade',
                                           required=False)
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=False)
    remindersendmethod = fields.Selection(related="parentid.remindersendmethod", store=True)
    # todo mettre à jour
    amount = fields.Float(string='Amount', compute='_compute_amount', readonly=True)
    structcom = fields.Char('Structured Communication', size=50)
    school_implantation_id = fields.Many2one('extraschool.schoolimplantation', 'School implantation', required=False)
    concerned_invoice_ids = fields.Many2many('extraschool.invoice', 'extraschool_reminder_invoice_rel', 'reminder_id',
                                             'invoice_id', 'Concerned invoices')
    activity_category_ids = fields.Many2many(related='reminders_journal_id.activity_category_ids',
                                             string='Activities Category')
    payment_term = fields.Date('reminders_journal_item_id.payment_term')
    transmission_date = fields.Date('reminders_journal_id.transmission_date')
    fees_amount = fields.Integer(default=0.0)
    balance_computed = fields.Float(string='Solde', compute='_compute_balance', readonly=True)
    balance = fields.Float(default=0.0)
    amount_received = fields.Float(string='Received', compute='_compute_amount_received',
                                   readonly=True)
    no_values = fields.Float(string="No values", compute="_compute_no_values", readonly=True)

    @api.multi
    def _compute_no_values(self):
        """
        Compute no_values for invoices
        :return: None
        """
        for reminder in self:
            for invoice in reminder.concerned_invoice_ids:
                reminder.no_values += invoice.no_value_amount

    @api.multi
    def _compute_amount_received(self):
        """
        Compute amount received for invoices
        :return: None
        """
        for reminder in self:
            for invoice in reminder.concerned_invoice_ids:
                reminder.amount_received += invoice.amount_received

    @api.multi
    def _compute_balance(self):
        """
        Compute amount received for invoices
        :return: None
        """
        for reminder in self:
            for invoice in reminder.concerned_invoice_ids:
                reminder.balance_computed += invoice.balance
                reminder.write({'balance': reminder.balance_computed})

    @api.multi
    def _compute_amount(self):
        """
        Compute amount received for invoices
        :return: None
        """
        for reminder in self:
            for invoice in reminder.concerned_invoice_ids:
                reminder.amount += invoice.amount_total

    @api.multi
    def get_date(self, invoice_ids):
        dates = invoice_ids.filtered(lambda r: r.biller_id.period_from)
        return " %s au %s" % (datetime.strptime(dates[0].biller_id.period_from, '%Y-%m-%d').strftime('%d-%m-%Y'),
                              datetime.strptime(dates[-1].biller_id.period_to, '%Y-%m-%d').strftime('%d-%m-%Y'))
