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

class extraschool_activityexclusiondates(osv.osv):
    _name = 'extraschool.activityexclusiondates'
    _description = 'Activity exclusion dates'

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        
        res=[]
        for exc_date in self.browse(cr, uid, ids,context=context):
            res.append((exc_date.id, exc_date.date_from + ' - ' + exc_date.date_to))    
    
        print str(res)

        return res     
            
    _columns = {
        'date_from' : fields.date('Date from', required=True),
        'date_to' : fields.date('Date to', required=True),
    }
extraschool_activityexclusiondates()
