# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
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
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp
from openerp.tools import float_compare, float_round
from datetime import datetime


class extraschool_payment_wizard(models.TransientModel):
    _name = 'extraschool.payment_wizard'

    payment_date = fields.Date('Date', default=datetime.now(), required=True)
    amount = fields.Float('Amount', digits_compute=dp.get_precision('extraschool_invoice'), required=True)
    reconciliation_amount_balance = fields.Float(compute="_compute_reconciliation_amount_balance", string='Amount to reconcil')
    reconciliation_amount = fields.Float(compute="_compute_reconciliation_amount", string='Amount reconcilied')
    parent_id = fields.Many2one("extraschool.parent")
    activity_category_id = fields.Many2one('extraschool.activitycategory', required=True)
    # activity_category_id = fields.Many2many('extraschool.activitycategory', 'extraschool_payment_wizard_activity_category_rel', required=True)
    payment_reconciliation_ids = fields.One2many('extraschool.payment_wizard_reconcil','payment_wizard_id')
    reject_id = fields.Many2one('extraschool.reject', string='Reject')
    comment = fields.Char('Comment')
    state = fields.Selection(
        [('init', 'Init'),
        ('print_payment', 'Print payment'),
        ('print_reconciliation', 'Print reconciliation')],
        'State', required=True, default='init',
        )

    @api.onchange('parent_id','amount','activity_category_id')
    def _on_change_payment_type(self):

        self.payment_reconciliation_ids = [(5, 0, 0)]

        reconciliations = []
        if len(self.activity_category_id) and self.parent_id:
            com_struct_prefix_list = []
            for activity_category in self.activity_category_id:
                com_struct_prefix_list.append(activity_category.payment_invitation_com_struct_prefix)
            reconciliations = self.env['extraschool.payment']._get_reconciliation_list(self.parent_id.id,
                                                                                       com_struct_prefix_list,
                                                                                       1, self.amount)

        tmp_payment_reconciliation_ids = []
        for reconciliation in reconciliations:
            tmp_payment_reconciliation_ids.append((0, 0, reconciliation))

        self.payment_reconciliation_ids = tmp_payment_reconciliation_ids

    @api.onchange('reconciliation_amount')
    @api.depends('reconciliation_amount')
    def _compute_reconciliation_amount_balance(self):
        for payment in self:
            payment.reconciliation_amount_balance = payment.amount - payment.reconciliation_amount

    @api.onchange('payment_reconciliation_ids')
    @api.depends('payment_reconciliation_ids')
    def _compute_reconciliation_amount(self):
        for payment in self:
            payment.reconciliation_amount = sum(reconcil_line.amount for reconcil_line in payment.payment_reconciliation_ids)

    @api.multi
    def next(self):
        if self.amount == 0.0:
            raise Warning(_("Amount can't be equal to 0"))
        # check if reconcil amount on line is never greater than balance
        reconciliation_error = 0
        total = 0

        for payment_reconciliation in self.payment_reconciliation_ids:
            total += payment_reconciliation.amount
            if float_compare(payment_reconciliation.amount,payment_reconciliation.invoice_balance,2) > 0:
                reconciliation_error += 1

        if reconciliation_error:
            raise Warning(_("At least one reconciliation line is not correct : amount greater than balance"))

        # Amount must be >= reconcil
        if total - self.amount >= 0.0000001:
            raise Warning(_("Reconcil amount MUST be less than payment amount"))

        self.create_payment()

    @api.multi
    def create_payment(self):
        payment = self.env['extraschool.payment']

        payment = payment.create({
            'parent_id': self.parent_id.id,
            'paymentdate': self.payment_date,  # This is Coda date.
            'structcom_prefix': self.activity_category_id.payment_invitation_com_struct_prefix,
            'activity_category_id': [(6, 0, [self.activity_category_id.id])],
            'amount': self.amount,
            'reject_id': self.reject_id.id if self.reject_id else False,
            'comment': self.comment,
        })

        if self.reject_id:
            self.env['extraschool.reject'].browse(self.reject_id.id).corrected_payment_id = payment.id

        payment_reconciliation = self.env['extraschool.payment_reconciliation']

        for reconciliation in self.payment_reconciliation_ids:
            payment_reconciliation.create({
                'payment_id': payment.id,
                'invoice_id': reconciliation.invoice_id.id,
                'amount': reconciliation.amount,
                'date': fields.Date.today()
            })  # Todo: si la date facture <= coda: date coda sinon date facture

            reconciliation.invoice_id._compute_balance()

        return {}


class extraschool_payment_wizard_reconcil(models.TransientModel):
    _name = 'extraschool.payment_wizard_reconcil'

    payment_wizard_id = fields.Many2one("extraschool.payment_wizard")
    invoice_id = fields.Many2one("extraschool.invoice")
    invoice_balance = fields.Float(related="invoice_id.balance", string = "Balance")
    amount = fields.Float('Amount', digits_compute=dp.get_precision('extraschool_invoice'), required=True)
    tag = fields.Many2one(related='invoice_id.tag', store=True)
    number_id = fields.Integer('Number',related='invoice_id.number', readonly=True)

