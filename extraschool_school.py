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

class extraschool_school(osv.osv):
    _name = 'extraschool.school'
    _description = 'School'

    _columns = {
        'name' : fields.char('Name', size=50),
        'street' : fields.char('Street', size=50),
        'zipcode' : fields.char('ZipCode', size=6),
        'city' : fields.char('City', size=50),
        'schoolimplantations' : fields.one2many('extraschool.schoolimplantation', 'schoolid','schoolimplantations'),
        'oldid' : fields.integer('oldid'),                
    }
extraschool_school()
