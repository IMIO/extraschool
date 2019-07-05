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

from odoo import models, api, fields, _
from odoo.api import Environment

class extraschool_reject(models.Model):
    _name = 'extraschool.reject'
    _description = 'Reject'

    paymentdate = fields.Date('Date')
    structcom = fields.Char('Structured Communication')
    freecom = fields.Char('Free communication')
    account = fields.Char('Account')
    name = fields.Char('Name')
    addr1 = fields.Char('Addr1')
    addr2 = fields.Char('Addr2')
    amount = fields.Float('Amount')
    rejectcause = fields.Char('Reject cause')
    coda = fields.Many2one('extraschool.coda', 'Coda')
    corrected_payment_id  = fields.Many2one('extraschool.payment', string='Payment corrigé')
    
    @api.multi
    def correct_reject(self):
        cr,uid = self.env.cr, self.env.user.id
        view_id = self.pool.get('ir.ui.view').search(cr,uid,[('model','=','extraschool.payment_wizard'),
                                                             ('name','=','extraschool.payment.wizard.form')])

        context = self._context.copy()
        context.update({'default_reject_id': self.id,
                        'default_amount': self.amount})

        return {
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.payment_wizard',
                'name': _("Correction du paiement"),
#                'res_id': biller.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'new',                   
                'context': {'default_reject_id': self.id,
                            'default_amount': self.amount,
                            'default_payment_date': self.coda.codadate}
            }
