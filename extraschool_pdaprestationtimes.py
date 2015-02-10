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

class extraschool_pdaprestationtimes(osv.osv):
    _name = 'extraschool.pdaprestationtimes'
    _description = 'PDA Prestation Times'
    
    _columns = {        
        'placeid' : fields.many2one('extraschool.place', 'Schoolcare Place', required=True),
        'activitycategoryid' : fields.many2one('extraschool.activitycategory', 'Activity Category', required=False),
        'childid' : fields.many2one('extraschool.child', 'Child', required=False),
        'prestation_date' : fields.date('Date'),
        'prestation_time' : fields.float('Time'),
        'es' : fields.selection((('E','In'), ('S','Out')),'ES' ),    
        'prestation_times_of_the_day_id' : fields.many2one('extraschool.prestation_times_of_the_day', 'Prestation of the day'),           
    }

    def create(self, cr, uid, vals, *args, **kw):               
        prestation_times_of_the_day_obj = self.pool.get('extraschool.prestation_times_of_the_day')
        prestation_times_obj = self.pool.get('extraschool.prestationtimes')
        
        prestation_times_of_the_day_ids = prestation_times_of_the_day_obj.search(cr,uid,[('child_id.id', '=', vals['childid']),
                                                                                ('date_of_the_day', '=', vals['prestation_date']),
                                                                                ])
        if not prestation_times_of_the_day_ids:
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_obj.create(cr,uid,{'child_id' : vals['childid'],
                                                           'date_of_the_day' : vals['prestation_date'],
                                                           })
        else :
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_ids[0]
        
        prestation_times_obj.create(cr,uid,vals)
        return super(extraschool_pdaprestationtimes, self).create(cr, uid, vals)    
    
extraschool_pdaprestationtimes()
