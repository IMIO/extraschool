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

class extraschool_activitychildregistration(osv.osv):
    _name = 'extraschool.activitychildregistration'
    _description = 'activity child registration'
    def _compute_name (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):     
            to_return[record.id]=record.child_id.name
        return to_return
        

    _columns = {
        'name' : fields.function(_compute_name, method=True, type="char", string="Name"),
        'child_id' : fields.many2one('extraschool.child', 'Child'),
        'activity_id' : fields.many2one('extraschool.activity', 'Activity'),
        'registration_from' : fields.date('Registration from'),
        'registration_to' : fields.date('Registration to'),
    }
extraschool_activitychildregistration()
