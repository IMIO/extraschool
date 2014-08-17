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

from openerp.osv import osv, fields

class extraschool_reject(osv.osv):
    _name = 'extraschool.reject'
    _description = 'Reject'

    _columns = {
        'paymentdate' : fields.date('Date'),
        'structcom' : fields.char('Structured Communication', size=50),
        'account' : fields.char('Account', size=20),
        'name' : fields.char('Name', size=50),
        'addr1' : fields.char('Addr1', size=50),
        'addr2' : fields.char('Addr2', size=50),
        'amount' : fields.float('Amount'),
        'rejectcause' : fields.char('Reject cause', size=60),
        'coda' : fields.many2one('extraschool.coda', 'Coda', required=False),
    }
extraschool_reject()

