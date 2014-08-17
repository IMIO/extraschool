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

class extraschool_discountrule(osv.osv):
    _name = 'extraschool.discountrule'
    _description = 'Discount Rule'

    _columns = {
        'name' : fields.char('Name', size=50),
        'field' : fields.char('Field', size=60),
        'operator' : fields.selection((('=','='),('= et ignorer case','ilike'),('>','>'),('<','<'),('>=','>='),('<=','<='),('<>','<>'),('in','in'),('is','is'),('is not','is not')),'Operator'),
        'value' : fields.char('Value', size=50),
    }
extraschool_discountrule()
