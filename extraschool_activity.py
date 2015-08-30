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
from openerp.exceptions import except_orm, Warning
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)

from datetime import date, datetime, timedelta as td
import time
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschool_activity(models.Model):
    _name = 'extraschool.activity'
    _description = 'activity'

    name = fields.Char('Name', required=True)
    category = fields.Many2one('extraschool.activitycategory', 'Category')
    parent_id = fields.Many2one('extraschool.activity', 'Parent')
    root_id = fields.Many2one('extraschool.activity', 'Root',compute='_compute_root_activity', store=True)
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
    default_from_to = fields.Selection((('from','default_from_to From'),('to','default_from_to To'),('from_to','default_from_to From and To')),'default_from_to Default From To') 
    default_from = fields.Float('Default from')
    default_to = fields.Float('Default to')
    fixedperiod = fields.Boolean('Fixed period',default=False)
    subsidizedbyone = fields.Boolean('Subsidized by one')
    validity_from = fields.Date('Validity from')
    validity_to = fields.Date('Validity to')
 
    @api.onchange('parent_id')
    @api.depends('parent_id')
    def _compute_root_activity(self):
        #to do à déplacer ds activity
        for activity in self: 
            # set root activity_id if 
            if activity.parent_id:
                parent = activity.parent_id                
                while parent.parent_id:
                    parent = parent.parent_id
                activity.root_id = parent
            else:
                activity.root_id = activity.id
    def build_timestamp(self,tsdate,tstime):
        hour = int(tstime)
        minute = int((tstime - hour) * 60)
        hour = hour -1 if hour else 0         
        return datetime.strptime(tsdate + ' ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00', DEFAULT_SERVER_DATETIME_FORMAT)
           
    def populate_occurrence(self,date_from = None):
        cr,uid = self.env.cr, self.env.user.id
        
        activityoccurrence = self.env['extraschool.activityoccurrence']
        for activity in self:
            if len(activity.planneddates_ids):
                for planneddate in activity.planneddates_ids:
                    for place in activity.placeids:
                        activityoccurrence.create({'place_id' : place.id,
                                                  'occurrence_date' : datetime.strptime(planneddate.activitydate, DEFAULT_SERVER_DATE_FORMAT),
                                                  'activityid' : activity.id,
                                                  'prest_from' : activity.prest_from,
                                                  'prest_to' : activity.prest_to,
                                                   })
            else:
                d1 = activity.validity_from
                if date_from:
                    if date_from > activity.validity_from:
                        d1 = date_from
                
                d2 = activity.validity_to
                
                d1 = datetime.strptime(d1, DEFAULT_SERVER_DATE_FORMAT)
                d2 = datetime.strptime(d2, DEFAULT_SERVER_DATE_FORMAT)

                delta = d2 - d1
                insert_data=''
                print str(datetime.now())+" START"
                args=[]
                for day in range(delta.days + 1):
                    print "day %s" % day
                    current_day_date = d1 + td(days=day)
                    if str(current_day_date.weekday()) in activity.days:
                        cr.execute('select count(*) from extraschool_activity_activityexclusiondates_rel as ear inner join extraschool_activityexclusiondates as ea on ear.activityexclusiondates_id = ea.id where activity_id = %s and date_from <= %s and date_to >= %s',(activity.id, current_day_date, current_day_date))
                        exclu_activity_id = cr.fetchall()
                        if exclu_activity_id[0][0] == 0:
                            for place in activity.placeids:
                                if insert_data:
                                    insert_data.join(',')
                                '''
                                activityoccurrence.create({'place_id' : place.id,
                                                          'occurrence_date' : current_day_date,
                                                          'activityid' : activity.id,
                                                          'prest_from' : activity.prest_from,
                                                          'prest_to' : activity.prest_to,
                                                          })
                                '''
                                str_current_day_date = str(current_day_date)[:10]
                                args.append((uid,
                                             self.build_timestamp(str_current_day_date,activity.prest_to),
                                             self.build_timestamp(str_current_day_date,activity.prest_from),
                                             activity.name + ' - ' + str_current_day_date,
                                             uid,
                                             activity.category.id,
                                             place.id,
                                             current_day_date,
                                             activity.id,
                                             activity.prest_from,
                                             activity.prest_to))
                                
                                #insert_data = insert_data.join('('+str(place.id)+','+str(current_day_date)+','+str(activity.id)+','+str(activity.prest_from)+','+str(activity.prest_to)+')')
                if len(args):
                    print str(datetime.now())+" Build query2"
                    args_str = ','.join(cr.mogrify("(%s,%s,%s,current_timestamp,%s,%s,current_timestamp,%s,%s,%s,%s,%s,%s)", x) for x in args)
                    print str(datetime.now())+" START QUERY" 
                    #print insert_data               
                    occurrence_ids = cr.execute("insert into extraschool_activityoccurrence (create_uid,date_stop,date_start,create_date,name,write_uid,write_date,activity_category_id,place_id,occurrence_date,activityid,prest_from,prest_to) VALUES "+args_str)
                    print str(datetime.now())+" END"
                    #get ids of created occu
                    occurrence_ids = cr.execute("""select id 
                                                   from extraschool_activityoccurrence 
                                                   where create_uid = %s
                                                     and activityid = %s
                                                """,(uid, activity.id))
                    occurrence_ids = [id['id'] for id in cr.dictfetchall()]
                    print "ids created : %s" % (occurrence_ids)
                    for occu in self.env['extraschool.activityoccurrence'].search([('id', 'in', occurrence_ids)]): 
                        occu.auto_add_registered_childs()
    @api.one                            
    def check_if_modifiable(self):
        invoicedprestations = self.env['extraschool.invoicedprestations'].search([('activity_occurrence_id.activityid', '=', self.id),
                                                                                ('prestation_date', '>=', time.strftime(DEFAULT_SERVER_DATE_FORMAT))])
        if len(invoicedprestations):
            return False
        else:
            return True

                
    @api.multi
    def write(self, vals):
        print "----- activity  write ----"
        for activity in self:
            if not activity.check_if_modifiable() :
                raise Warning("It's not possible to update the activity because there are invoiced prestations after the current date")
                return False
            
            res = super(extraschool_activity,activity).write(vals)
            if res:
                #set all the future presta of this activity as NOT verified
                prestations = self.env['extraschool.prestationtimes'].search([('activity_occurrence_id.activityid.id', '=', activity.id),
                                                                              ('prestation_date', '>=', time.strftime(DEFAULT_SERVER_DATE_FORMAT))])
                prestations.write({'verified' : False})
                #delete all future occurrence of this activity
                occurrences = self.env['extraschool.activityoccurrence'].search([('activityid', '=', activity.id),
                                                                                  ('occurrence_date', '>=', time.strftime(DEFAULT_SERVER_DATE_FORMAT))])
                print "delete occu !!!!"
                occurrences.unlink()
                #populate occurrence
                activity.populate_occurrence(time.strftime(DEFAULT_SERVER_DATE_FORMAT))
 
            else: 
                return res
           
        return True

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

