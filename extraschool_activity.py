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
from datetime import date, datetime, timedelta as td


class extraschool_activity(osv.osv):
    _name = 'extraschool.activity'
    _description = 'activity'

    _columns = {
        'name' : fields.char('Name', size=50),
        'category' : fields.many2one('extraschool.activitycategory', 'Category'),
        'placeids'  : fields.many2many('extraschool.place','extraschool_activity_place_rel', 'activity_id', 'place_id','Schoolcare place'),
        'parent_id' : fields.many2one('extraschool.activity', 'Parent'),
        'activity_child_ids' : fields.one2many('extraschool.activity', 'parent_id','Activity child'),
        'schoolimplantationids'  : fields.many2many('extraschool.schoolimplantation','extraschool_activity_schoolimplantation_rel', 'activity_id', 'schoolimplantation_id','Schoolcare schoolimplantation'),
        'short_name' : fields.char('Short name', size=20),        
        'childtype_ids' : fields.many2many('extraschool.childtype','extraschool_activity_childtype_rel', 'activity_id', 'childtype_id','Child type'),                        
        'childregistration_ids' : fields.one2many('extraschool.activitychildregistration', 'activity_id','Child registrations'),
        'autoaddchilds' : fields.boolean('Auto add registered'),                
        'onlyregisteredchilds' : fields.boolean('Only registered childs'),                
        'planneddates_ids' : fields.many2many('extraschool.activityplanneddate','extraschool_activity_activityplanneddate_rel', 'activity_id', 'activityplanneddate_id','Planned dates'),        
        'exclusiondates_ids' : fields.many2many('extraschool.activityexclusiondates','extraschool_activity_activityexclusiondates_rel', 'activity_id', 'activityexclusiondates_id','Exclusion dates'),        
        'days' : fields.selection((('0,1,2,3,4','All Monday to Friday'),('0','All Mondays'),('1','All Tuesdays'),('2','All Wednesdays'),('3','All Thursdays'),('4','All Fridays'),('0,1,3,4','All Mondays, Tuesdays, Thursday and Friday')),'Days'),
        'leveltype' : fields.selection((('M,P','Maternelle et Primaire'),('M','Maternelle'),('P','Primaire')),'Level type'),
        'prest_from' : fields.float('From'),
        'prest_to' : fields.float('To'),        
        'price' : fields.float('Price',digits=(7,3)),
        'period_duration' : fields.integer('Period Duration'),    
        'default_from' : fields.float('Default from'),
        'default_to' : fields.float('Default to'),
        'fixedperiod': fields.boolean('Fixed period'),
        'subsidizedbyone': fields.boolean('Subsidized by one'),
        'validity_from' : fields.date('Validity from'),
        'validity_to' : fields.date('Validity to')
    }
    _defaults = {
        'fixedperiod' : lambda *a: False,
    }
    
    def populate_occurrence(self,cr,uid,ids,date_from = None):
        activityoccurrence = self.pool.get('extraschool.activityoccurrence')
        activity_obj = self.pool.get('extraschool.activity')
        for activity in activity_obj.browse(cr,uid,ids):
            if (len(activity.planneddates_ids)):
                for planneddate in activity.planneddates_ids:
                    activityoccurrence.create(cr,uid,{'occurrence_date' : planneddate.activitydate,
                                                      'activityid' : activity.id,
                                               })
            else:
                d1 = activity.validity_from
                if (date_from):
                    if (date_from > activity.validity_from):
                        d1 = date_from
                
                d2 = activity.validity_to
                
                d1 = datetime.strptime(d1, '%Y-%m-%d')
                d2 = datetime.strptime(d2, '%Y-%m-%d')

                delta = d2 - d1

                for day in range(delta.days + 1):
                    current_day_date = d1 + td(days=day)
                    if (str(current_day_date.weekday()) in activity.days):
                        cr.execute('select count(*) from extraschool_activity_activityexclusiondates_rel as ear inner join extraschool_activityexclusiondates as ea on ear.activityexclusiondates_id = ea.id where date_from <= %s and date_to >= %s',(current_day_date, current_day_date))
                        exclu_activity_id = cr.fetchall()
                        if (exclu_activity_id[0][0] == 0):
                            activityoccurrence.create(cr,uid,{'occurrence_date' : current_day_date,
                                                              'activityid' : activity.id,
                                                              })
    def write(self,cr,uid,ids,vals,context = None):
        super(extraschool_activity,self).write(cr,uid,ids,vals)
        self.populate_occurrence(cr, uid, ids)

extraschool_activity()

