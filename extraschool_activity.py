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
from datetime import date, datetime, timedelta as td


class extraschool_activity(models.Model):
    _name = 'extraschool.activity'
    _description = 'activity'

    name = fields.Char('Name', size=100, required=True)
    category = fields.Many2one('extraschool.activitycategory', 'Category')
    parent_id = fields.Many2one('extraschool.activity', 'Parent')
    root_id = fields.Many2one('extraschool.activity', 'Root')
    activity_child_ids = fields.One2many('extraschool.activity', 'parent_id','Activity child')
    placeids  = fields.Many2many('extraschool.place','extraschool_activity_place_rel', 'activity_id', 'place_id','Schoolcare place')
    schoolimplantationids = fields.Many2many('extraschool.schoolimplantation','extraschool_activity_schoolimplantation_rel', 'activity_id', 'schoolimplantation_id','Schoolcare schoolimplantation')
    short_name = fields.Char('Short name', size=20)        
    childtype_ids = fields.Many2many('extraschool.childtype','extraschool_activity_childtype_rel', 'activity_id', 'childtype_id','Child type')                        
    childregistration_ids = fields.One2many('extraschool.activitychildregistration', 'activity_id','Child registrations')
    autoaddchilds = fields.Boolean('Auto add registered')                
    onlyregisteredchilds = fields.Boolean('Only registered childs')               
    planneddates_ids = fields.Many2many('extraschool.activityplanneddate','extraschool_activity_activityplanneddate_rel', 'activity_id', 'activityplanneddate_id','Planned dates')        
    exclusiondates_ids = fields.Many2many('extraschool.activityexclusiondates','extraschool_activity_activityexclusiondates_rel', 'activity_id', 'activityexclusiondates_id','Exclusion dates')        
    days = fields.Selection((('0,1,2,3,4','All Monday to Friday'),('0','All Mondays'),('1','All Tuesdays'),('2','All Wednesdays'),('3','All Thursdays'),('4','All Fridays'),('0,1,3,4','All Mondays, Tuesdays, Thursday and Friday')),'Days')
    leveltype = fields.Selection((('M,P','Maternelle et Primaire'),('M','Maternelle'),('P','Primaire')),'Level type')
    prest_from = fields.Float('From')
    prest_to = fields.Float('To')        
    price = fields.Float('Price',digits=(7,3))
    price_list_id = fields.Many2one('extraschool.price_list', 'Price List')    
    period_duration = fields.Integer('Period Duration')  
    default_from_to = fields.Selection((('from','From'),('to','To'),('from_to','From and To')),'Default From To') 
    default_from = fields.Float('Default from')
    default_to = fields.Float('Default to')
    fixedperiod = fields.Boolean('Fixed period',default=False)
    subsidizedbyone = fields.Boolean('Subsidized by one')
    validity_from = fields.Date('Validity from')
    validity_to = fields.Date('Validity to')

        
    def populate_occurrence(self,date_from = None):
        cr,uid = self.env.cr, self.env.user.id
        
        activityoccurrence = self.env['extraschool.activityoccurrence']
        for activity in self:
            if len(activity.planneddates_ids):
                for planneddate in activity.planneddates_ids:
                    for place in activity.placeids:
                        activityoccurrence.create({'place_id' : place.id,
                                                  'occurrence_date' : datetime.strptime(planneddate.activitydate, '%Y-%m-%d'),
                                                  'activityid' : activity.id,
                                                   })
            else:
                d1 = activity.validity_from
                if date_from:
                    if date_from > activity.validity_from:
                        d1 = date_from
                
                d2 = activity.validity_to
                
                d1 = datetime.strptime(d1, '%Y-%m-%d')
                d2 = datetime.strptime(d2, '%Y-%m-%d')

                delta = d2 - d1

                for day in range(delta.days + 1):
                    current_day_date = d1 + td(days=day)
                    if str(current_day_date.weekday()) in activity.days:
                        cr.execute('select count(*) from extraschool_activity_activityexclusiondates_rel as ear inner join extraschool_activityexclusiondates as ea on ear.activityexclusiondates_id = ea.id where activity_id = %s and date_from <= %s and date_to >= %s',(activity.id, current_day_date, current_day_date))
                        exclu_activity_id = cr.fetchall()
                        if exclu_activity_id[0][0] == 0:
                            for place in activity.placeids:
                                activityoccurrence.create({'place_id' : place.id,
                                                          'occurrence_date' : current_day_date,
                                                          'activityid' : activity.id,
                                                          })

    def write(self, vals):
        res = super(extraschool_activity,self).write(vals)
        #to do handle changes on occurrences
        return res

    @api.model
    def create(self, vals):                 
        res = super(extraschool_activity,self).create(vals)

        if res:
            res.populate_occurrence()
        
        return res

    def get_start(self,activity):
        if activity.default_from_to == 'from' or activity.default_from_to == 'from_to':
            return activity.prest_from
        else:
            return False
        
    def get_stop(self,activity):
        if activity.default_from_to == 'to' or activity.default_from_to == 'from_to':
            return activity.prest_to
        else:
            return False
        
extraschool_activity()

