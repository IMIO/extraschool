# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014
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

from openerp import models, api, fields, _
from openerp.api import Environment
from datetime import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning
import logging
_logger = logging.getLogger(__name__)
import math

class ExtraSchoolPaymentPlan(models.Model):
    _name = 'extraschool.payment_plan'
    _description = 'Payment Plan'

    @api.depends('total_amount', 'paid_amount')
    def _get_due_amount(self):
        return self.total_amount - self.paid_amount

    parent_id = fields.Many2one(
        'extraschool.parent',
        string="Parent",
        required=True,
        domain="[('isdisabled', '=', False)]",
    )
    invoice_ids = fields.Many2many(
        'extraschool.invoice',
        'extraschool_payment_plan_invoice_rel',
        'payment_plan_id', 'invoice_id',
        required=True,
        domain="[('parentid', '=', parent_id), ('balance', '!=', 0), ('tag', '=', False)]",
    )
    payment_plan_document_ids = fields.One2many(
        'extraschool.payment_plan_document',
        'payment_plan_id',
        string='Payment Plan Document'
    )
    payment_rate = fields.Float(
        string='Amount per month',
    )
    month_rate = fields.Integer(
        string='Month to pay',
    )
    total_amount = fields.Float(
        string='Total to pay',
    )
    paid_amount = fields.Float(
        string='Total paid',
    )
    due_amount = fields.Float(
        string='Amount Due',
        default=_get_due_amount,
    )
    number_of_payment = fields.Integer(
        string='Number of payment',
    )
    comm_struct = fields.Char(
        string='Communication',
    )
    active = fields.Boolean(
        default=True,
    )

    @api.onchange('invoice_ids')
    def _onchange_invoice_ids(self):
        self.total_amount = sum([invoice.balance for invoice in self.invoice_ids])
        self.due_amount = self.total_amount - self.paid_amount

    @api.onchange('payment_rate')
    def _onchange_payment_rate(self):
        if not self.payment_rate:
            return False

        total_month = self.total_amount / self.payment_rate
        self.month_rate = math.ceil(total_month)

class ExtraSchoolPaymentPlanDocument(models.Model):
    _name = 'extraschool.payment_plan_document'
    _description = 'Payment Plan Document'

    payment_plan_id = fields.Many2one(
        'extraschool.payment_plan',
        string='Payment Plan'
    )
    document_date = fields.Datetime(
        string='Document date',
        readonly=True,
        default=datetime.now(),
    )
    state = fields.Selection(
        [
            ('created', 'Created'),
            ('sent', 'Sent'),
            ('paid', 'Paid'),
            ('expired', 'Expired')
        ],
        readonly=True,
        default='created',
    )
    number = fields.Integer(
        string='Number of payment plan',
        readonly=True,
    )
