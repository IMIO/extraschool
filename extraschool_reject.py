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

class extraschool_reject(models.Model):
    _name = 'extraschool.reject'
    _description = 'Reject'

    paymentdate = fields.Date('Date')
    structcom = fields.Char('Structured Communication', size=50)
    account = fields.Char('Account', size=20)
    name = fields.Char('Name', size=50)
    addr1 = fields.Char('Addr1', size=50),
    addr2 = fields.Char('Addr2', size=50),
    amount = fields.Float('Amount')
    rejectcause = fields.Char('Reject cause', size=60)
    coda = fields.Many2one('extraschool.coda', 'Coda', required=False)

extraschool_reject()

