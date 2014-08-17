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

class extraschool_guardian(osv.osv):
    _name = 'extraschool.guardian'
    _description = 'Guardian'
    _columns = {
        'name' : fields.char('FullName', size=100),
        'firstname' : fields.char('FirstName', size=50),
        'lastname' : fields.char('LastName', size=50 , required=True),
        'tagid' : fields.char('Tag ID', size=50),
        'oldid' : fields.integer('oldid'),                
    }
extraschool_guardian()
