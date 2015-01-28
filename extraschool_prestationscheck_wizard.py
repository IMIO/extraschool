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

#from openerp.osv import osv, fields
from openerp import models, api, fields
from openerp.api import Environment
from datetime import date
import datetime
import calendar
import cStringIO
import base64
import appy.pod.renderer
import os
import math
import lbutils
import re
from pyPdf import PdfFileWriter, PdfFileReader
from pytz import timezone
import pytz
from dateutil.relativedelta import *
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)


class extraschool_prestationscheck_wizard(models.TransientModel):
    _name = 'extraschool.prestationscheck_wizard'
    
    def _get_prestations(self, cr, uid, ids, field_names, arg=None, context=None):
        obj_prestations = self.pool.get('extraschool.prestationtimes')
        wiz_obj = self.browse(cr, uid, ids)[0]
        prestations_ids=obj_prestations.search(cr, uid, [('childid', '=', wiz_obj.childid.id),('prestation_date', '=', wiz_obj.currentdate)], order='prestation_time')        
        result = {ids[0]:prestations_ids, 'nodestroy': True}
        return result

    def _get_defaultfrom(self):
        #look for first oldest prest NOT verified
        prestationtimes_rs = self.env['extraschool.prestationtimes'].search([('verified', '=', False)], order='prestation_date ASC', limit=1)
        print "_get_defaultfrom"
        if prestationtimes_rs: #If a presta not verified exist 
            fromdate = datetime.datetime.strptime(prestationtimes_rs[0].prestation_date, DEFAULT_SERVER_DATE_FORMAT)
            print "----------"
            print str(self.env.context)
            print "----------"
            
            user_time_zone = self.env.context.get('tz', False) #self.env.user.tz si ca ne fct pas !!!
            print "--" + str(fromdate) + "---"
            local = pytz.timezone (user_time_zone) 
            print "--" + str(local) + "---"
            fromdate = local.localize(fromdate, is_dst=False)
            print "--" + str(fromdate) + "---"
            
            return fromdate.strftime("%Y-%m-%d")  
        else:
            date_now = datetime.datetime.now()
            return str(datetime.date(date_now.year,date_now.month,1))

    def _get_defaultto(self):          
        return datetime.datetime.now().strftime("%Y-%m-%d")  

    def _default_activitycategory(self):
        activitycategory_rs = self.env['extraschool.activitycategory']
        
        return activitycategory_rs[0].id if activitycategory_rs else None
    
    placeid = fields.Many2many(comodel_name='extraschool.place',
                               relation='extraschool_prestationscheck_wizard_place_rel',
                               column1='prestationscheck_wizard_id',
                               column2='place_id')
    period_from = fields.Date(default=_get_defaultfrom)
    period_to = fields.Date(default=_get_defaultto)
    activitycategory = fields.Many2one('extraschool.activitycategory', default=_default_activitycategory)                    
    state = fields.Selection([('init', 'Init'),
                                ('prestations_to_verify', 'Prestations to verify'),
                                ('end_of_verification', 'End of verification')],
                               'State', default='init', required=True)    
        
    def insertprestation(self,cr,uid,placeid,prestation_date,childid,ES,prestation_time,activitycategoryid,manualy_encoded,activityid):
        cr.execute('select * from extraschool_prestationtimes where prestation_date = %s and childid = %s and prestation_time = %s and "es"=%s', (prestation_date,childid,prestation_time,ES))
        prests=cr.dictfetchall()
        if not prests:
            obj_prestation = self.pool.get('extraschool.prestationtimes')
            # On recupere le niveau de priorite
            cr.execute('select priorityorder from extraschool_activitycategory where id=%s',(activitycategoryid,))
            priorityorder=cr.dictfetchall()[0]['priorityorder']        
            if ES=='E':
                # si c est une entree on va chercher la derniere prestation de priorite inferieure
                #cr.execute('select max(prestation_time),max("es") as "es",max("activitycategoryid") as activitycategoryid from extraschool_prestationtimes left join extraschool_activitycategory on activitycategoryid = extraschool_activitycategory.id where prestation_date = %s and childid = %s and prestation_time < %s and priorityorder < %s', (prestation_date,childid,prestation_time,priorityorder))
                cr.execute('select prestation_time,"es",activitycategoryid from extraschool_prestationtimes left join extraschool_activitycategory on activitycategoryid = extraschool_activitycategory.id where prestation_date = %s and childid = %s and prestation_time < %s and priorityorder < %s order by prestation_time desc,"es" desc,activitycategoryid desc', (prestation_date,childid,prestation_time,priorityorder))
                lastprest=cr.dictfetchall()
                if lastprest:
                    if lastprest[0]['ES']=='E':
                        # si la derniere prestation de priorite inferieure est une entree on insere une sortie
                        cr.execute('select * from extraschool_prestationtimes where prestation_date = %s and childid = %s and prestation_time = %s and "es"=%s and activitycategoryid=%s', (prestation_date,childid,(prestation_time-0.016666667),'S',lastprest[0]['activitycategoryid']))
                        prests=cr.dictfetchall()
                        if not prests:
                            obj_prestation.create(cr,uid, {'placeid':placeid,'prestation_date': prestation_date,'childid': childid,'ES':'S','prestation_time' : (prestation_time-0.016666667),'activitycategoryid' : lastprest[0]['activitycategoryid'],'manualy_encoded':manualy_encoded,'activityid':activityid})            
                       
            else:
                # si c est une sortie on va chercher la premiere prestation de priorite inferieure
                #cr.execute('select min(prestation_time),min("es") as "es",max("activitycategoryid") as activitycategoryid from extraschool_prestationtimes left join extraschool_activitycategory on activitycategoryid = extraschool_activitycategory.id where prestation_date = %s and childid = %s and prestation_time > %s and priorityorder < %s', (prestation_date,childid,prestation_time,priorityorder))
                cr.execute('select prestation_time,"es",activitycategoryid from extraschool_prestationtimes left join extraschool_activitycategory on activitycategoryid = extraschool_activitycategory.id where prestation_date = %s and childid = %s and prestation_time > %s and priorityorder < %s order by prestation_time asc,"es" asc,activitycategoryid desc', (prestation_date,childid,prestation_time,priorityorder))
                firstprest=cr.dictfetchall()
                if firstprest:
                    if firstprest[0]['ES']=='S':
                        cr.execute('select * from extraschool_prestationtimes where prestation_date = %s and childid = %s and prestation_time = %s and "es"=%s and activitycategoryid=%s', (prestation_date,childid,(prestation_time+0.016666667),'E',firstprest[0]['activitycategoryid']))
                        prests=cr.dictfetchall()
                        if not prests:
                            obj_prestation.create(cr,uid, {'placeid':placeid,'prestation_date': prestation_date,'childid': childid,'ES':'E','prestation_time' : (prestation_time+0.016666667),'activitycategoryid' : firstprest[0]['activitycategoryid'],'manualy_encoded':manualy_encoded,'activityid':activityid})
                       
            obj_prestation.create(cr,uid, {'placeid':placeid,'prestation_date': prestation_date,'childid': childid,'ES':ES,'prestation_time' : prestation_time,'activitycategoryid' : activitycategoryid,'manualy_encoded':manualy_encoded,'activityid':activityid})

    def get_prestation_activityid(self, prestation):
        #dico of return value
        return_val = {'return_code': 0,
                      'error_msg' : 'Unknown Error',
                      'occurrence_id' : -1}
        
        obj_activity_occurrence = self.env['extraschool.activityoccurrence']
        obj_activity_child_registration = self.env['extraschool.activitychildregistration']
 
        #get occurrence of the presta day matching the time slot      
        occurrence_rs = obj_activity_occurrence.search([('place_id','=',prestation.placeid.id),
                                                        ('occurrence_date','=',prestation.prestation_date),
                                                        ('activityid.prest_from','<=',prestation.prestation_time),
                                                        ('activityid.prest_to','>=',prestation.prestation_time),
                                                        ])
        print "yop"
        if not occurrence_rs:  #Error No matching occurrence found
            return_val['error_msg'] = "No matching occurrence found"
            return return_val
            
        #extract activity ID from occurrence
        activity_ids = [occurrence.activityid.id for occurrence in occurrence_rs]

        #check if there is a occurrence in witch the child is registered for that date
        registeredchild_ids = obj_activity_child_registration.search([('place_id.id','=',prestation.placeid.id),
                                                                      ('activity_id.id','in',activity_ids),                                                                             
                                                                      ('child_id.id','=',prestation.childid.id),
                                                                      ('registration_from','<=',prestation.prestation_date),
                                                                      ('registration_to','>=',prestation.prestation_date),
                                                                     ])
        print "yup"
        
        if registeredchild_ids:
            activity_occurrence_id = obj_activity_occurrence.search([('place_id.id','=',prestation.placeid.id),
                                                                     ('occurrence_date','=',prestation.prestation_date),
                                                                     ('activityid.id','=',registeredchild_ids[0].activity_id.id)
                                                                     ])
            return_val['return_code'] = 1   
            return_val['occurrence_id'] = activity_occurrence_id[0].id     
            return return_val
        
        #filter occurence to remove occurence with registration
        occurrence_no_register_rs = occurrence_rs.filtered(lambda r: len(r.activityid.activity_child_ids) == 0)
        
        
        #try to find a leaf matching the time slot
        occurrence_leaf_rs = occurrence_no_register_rs.filtered(lambda r: len(r.activityid.childregistration_ids) == 0)
        print "yip"
        
        if len(occurrence_leaf_rs) > 1:  #Error more than 1 occurrence found
            return_val['error_msg'] = "More than one leaf occurrence found"
            return return_val

        if occurrence_leaf_rs: #One occurrence found
            return_val['return_code'] = 1   
            return_val['occurrence_id'] = occurrence_leaf_rs[0].id     
            return return_val
        
        #try to find a branch matching the time slot
        occurrence_branch_rs = occurrence_no_register_rs.filtered(lambda r: len(r.activityid.activity_child_ids) > 0)
        print "yap"
        
        if len(occurrence_branch_rs) > 1:  #Error more than 1 occurrence found
            return_val['error_msg'] = "More than one branch occurrence found"
            return return_val
        print "yyyp"

        if occurrence_branch_rs: #One occurrence found
            return_val['return_code'] = 1   
            return_val['occurrence_id'] = occurrence_branch_rs[0].id     
            return return_val
        
        return return_val

    def _prestation_completion(self,prestation):
        if prestation.es == 'E':
            # Entrance
            print "Entrance"
        else:    
            # exit
            print "Exit"
            
    def _prestation_activity_occurrence_completion(self,prestation):
        #Look for activityoccurrence maching the prestation
        res = self.get_prestation_activityid(prestation)
        print "+++++" + str(res) + "----"
        if not res['return_code']:
            prestation.error_msg = res['error_msg']
        else:
            prestation.activity_occurrence_id = res['occurrence_id']
                
        return self
        
        
        
        
    def _check(self):        
        prestation_search_domain = [('verified', '=', False),]
        
        if self.placeid:
            prestation_search_domain.append(('placeid.id', 'in', [place.id for place in self.placeid]))
        if self.activitycategory:
            prestation_search_domain.append(('activitycategoryid.id', '=', self.activitycategory[0].id))
        if self.period_from:
            prestation_search_domain.append(('prestation_date', '>=', self.period_from))
        if self.period_to:
            prestation_search_domain.append(('prestation_date', '<=', self.period_to))
                                    
        obj_prestation_rs = self.env['extraschool.prestationtimes'].search(prestation_search_domain)
        print "---obj_prestation_rs---"
        print str(obj_prestation_rs)
        print "---FILTERED obj_prestation_rs---"
        print str(obj_prestation_rs.filtered(lambda r: not r.activity_occurrence_id))
                        
        #add activity occurrence when missing
        for prestation in obj_prestation_rs.filtered(lambda r: not r.activity_occurrence_id):   
            print "add activity occurrence id "       
            self._prestation_activity_occurrence_completion(prestation)

        obj_prestation_of_the_day_rs = self.env['extraschool.prestation_times_of_the_day'].search([('prestationtime_ids.verified', '=', False)])
        #add activity occurrence when missing
        for prestation_of_the_day in obj_prestation_of_the_day_rs:      
            prestation_of_the_day._check()   

        self.state = 'end_of_verification'
        
        return self        
    
    @api.multi    
    def action_prestationscheck(self):    
            
        return self._check()


extraschool_prestationscheck_wizard()
