# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia  & Jenny Pans - Imio (<http://www.imio.be>).
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

import openerp.addons.decimal_precision as dp

from openerp import models, fields


class extraschool_payment_wizard_reconcil(models.TransientModel):
    _name = 'extraschool.payment_wizard_reconcil'

    payment_wizard_id = fields.Many2one("extraschool.payment_wizard")
    invoice_id = fields.Many2one("extraschool.invoice")
    invoice_balance = fields.Float(related="invoice_id.balance", string="Balance")
    amount = fields.Float('Amount', digits_compute=dp.get_precision('extraschool_invoice'), required=True)
    tag = fields.Many2one(related='invoice_id.tag', store=True)
    number_id = fields.Integer('Number', related='invoice_id.number', readonly=True)
