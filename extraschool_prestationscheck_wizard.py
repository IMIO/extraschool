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
from openerp import models,api, fields
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
        
        if prestationtimes_rs: #If a presta not verified exist 
            fromdate = datetime.datetime.strptime(prestationtimes_rs[0].prestation_date, DEFAULT_SERVER_DATE_FORMAT).date()
            user_time_zone = self.env.context.get('tz', False) #self.env.user.tz si ca ne fct pas !!!
            local = pytz.timezone (user_time_zone) 
            fromdate = local.localize(fromdate, is_dst=None)
            
            return fromdate.strftime("%Y-%m-%d")  
        else:
            date_now = datetime.datetime.now()
            return str(datetime.date(date_now.year,date_now.month,1))

    def _get_defaultto(self):          
        return datetime.datetime.now().strftime("%Y-%m-%d")  

    def _default_activitycategory(self):
        activitycategory_rs = self.env['extraschool.activitycategory']
        
        return activitycategory_rs[0].id if activitycategory_rs else None
    
    placeid = fields.Many2many('extraschool.place')
    period_from = fields.Date(required=True, default=_get_defaultfrom)
    period_to = fields.Date(required=True, default=_get_defaultto)
    activitycategory = fields.Many2one('extraschool.activitycategory', default=_default_activitycategory),                     
    state = fields.Selection([('init', 'Init'),
                                ('prestations_to_verify', 'Prestations to verify'),
                                ('end_of_verification', 'End of verification')],
                               'State', default='init', required=True)    
        
    def insertprestation(self,cr,uid,placeid,prestation_date,childid,ES,prestation_time,activitycategoryid,manualy_encoded,activityid):
        cr.execute('select * from extraschool_prestationtimes where prestation_date = %s and childid = %s and prestation_time = %s and "ES"=%s', (prestation_date,childid,prestation_time,ES))
        prests=cr.dictfetchall()
        if not prests:
            obj_prestation = self.pool.get('extraschool.prestationtimes')
            # On recupere le niveau de priorite
            cr.execute('select priorityorder from extraschool_activitycategory where id=%s',(activitycategoryid,))
            priorityorder=cr.dictfetchall()[0]['priorityorder']        
            if ES=='E':
                # si c est une entree on va chercher la derniere prestation de priorite inferieure
                #cr.execute('select max(prestation_time),max("ES") as "ES",max("activitycategoryid") as activitycategoryid from extraschool_prestationtimes left join extraschool_activitycategory on activitycategoryid = extraschool_activitycategory.id where prestation_date = %s and childid = %s and prestation_time < %s and priorityorder < %s', (prestation_date,childid,prestation_time,priorityorder))
                cr.execute('select prestation_time,"ES",activitycategoryid from extraschool_prestationtimes left join extraschool_activitycategory on activitycategoryid = extraschool_activitycategory.id where prestation_date = %s and childid = %s and prestation_time < %s and priorityorder < %s order by prestation_time desc,"ES" desc,activitycategoryid desc', (prestation_date,childid,prestation_time,priorityorder))
                lastprest=cr.dictfetchall()
                if lastprest:
                    if lastprest[0]['ES']=='E':
                        # si la derniere prestation de priorite inferieure est une entree on insere une sortie
                        cr.execute('select * from extraschool_prestationtimes where prestation_date = %s and childid = %s and prestation_time = %s and "ES"=%s and activitycategoryid=%s', (prestation_date,childid,(prestation_time-0.016666667),'S',lastprest[0]['activitycategoryid']))
                        prests=cr.dictfetchall()
                        if not prests:
                            obj_prestation.create(cr,uid, {'placeid':placeid,'prestation_date': prestation_date,'childid': childid,'ES':'S','prestation_time' : (prestation_time-0.016666667),'activitycategoryid' : lastprest[0]['activitycategoryid'],'manualy_encoded':manualy_encoded,'activityid':activityid})            
                       
            else:
                # si c est une sortie on va chercher la premiere prestation de priorite inferieure
                #cr.execute('select min(prestation_time),min("ES") as "ES",max("activitycategoryid") as activitycategoryid from extraschool_prestationtimes left join extraschool_activitycategory on activitycategoryid = extraschool_activitycategory.id where prestation_date = %s and childid = %s and prestation_time > %s and priorityorder < %s', (prestation_date,childid,prestation_time,priorityorder))
                cr.execute('select prestation_time,"ES",activitycategoryid from extraschool_prestationtimes left join extraschool_activitycategory on activitycategoryid = extraschool_activitycategory.id where prestation_date = %s and childid = %s and prestation_time > %s and priorityorder < %s order by prestation_time asc,"ES" asc,activitycategoryid desc', (prestation_date,childid,prestation_time,priorityorder))
                firstprest=cr.dictfetchall()
                if firstprest:
                    if firstprest[0]['ES']=='S':
                        cr.execute('select * from extraschool_prestationtimes where prestation_date = %s and childid = %s and prestation_time = %s and "ES"=%s and activitycategoryid=%s', (prestation_date,childid,(prestation_time+0.016666667),'E',firstprest[0]['activitycategoryid']))
                        prests=cr.dictfetchall()
                        if not prests:
                            obj_prestation.create(cr,uid, {'placeid':placeid,'prestation_date': prestation_date,'childid': childid,'ES':'E','prestation_time' : (prestation_time+0.016666667),'activitycategoryid' : firstprest[0]['activitycategoryid'],'manualy_encoded':manualy_encoded,'activityid':activityid})
                       
            obj_prestation.create(cr,uid, {'placeid':placeid,'prestation_date': prestation_date,'childid': childid,'ES':ES,'prestation_time' : prestation_time,'activitycategoryid' : activitycategoryid,'manualy_encoded':manualy_encoded,'activityid':activityid})

    def get_prestation_activityid(self, prestation):
        obj_activity = self.env['extraschool.activity']
        obj_activity_occurrence = self.env['extraschool.activityoccurrence']
        obj_activity_child_registration = self.env['extraschool.activitychildregistration']
 
        #get occurence of the presta day        
        occurrence_rs = obj_activity_occurrence.search([('occurrence_date','=',prestation.prestation_date)])
        #extract activity ID from occurence
        activity_ids = [occurrence.activityid.id for occurrence in occurrence_rs]

        #check if there is a occurrence in witch the child is registered for that date
        registeredchild_ids = obj_activity_child_registration.search([('activity_id','in',activity_ids),                                                                             
                                                                      ('child_id','=',prestation.childid.id),
                                                                      ('registration_from','<=',prestation.prestation_date),
                                                                      ('registration_to','>=',prestation.prestation_date),
                                                                      ('activity_id.prest_from','<=',prestation.prestation_time),
                                                                      ('activity_id.prest_to','>=',prestation.prestation_time),
                                                                     ])
 
        if registeredchild_ids:
            activity_occurrence_id = obj_activity_occurrence.search([('occurence_date','=',prestation.prestation_date),
                                                                     ('activity_id','=',registeredchild_ids[0].activity_id.id)
                                                                   ])
            return activity_occurrence_id
        
        
    
        print activity_ids
        
        '''
        activity_ids = [occurrence.activityid for occurrence in obj_activity_occurrence.browse(cr,uid,activity_occurrences_ids)]
        registeredchild_ids = obj_activity_child_registration.search(cr,uid,[('activity_id','in',activity_ids),                                                                             
                                                                             ('child_id','=',prestation.childid),
                                                                             ('registration_from','<=',prestation.prestation_date),
                                                                             ('registration_to','>=',prestation.prestation_date),
                                                                             ('activity_id.prest_from','<=',prestation.prestation_time),
                                                                             ('activity_id.prest_to','>=',prestation.prestation_time),
                                                                             ])
        if registeredchild_ids:
            activity_occurrence_id = obj_activity_occurrence.search(cr, uid, [('occurence_date','=',prestation.prestation_date),
                                                                             ('activity_id','=',obj_activity_child_registration.browse(cr,uid,registeredchild_ids[0]).activity_id.id)
                                                                             ])
            return activity_occurrence_id
        
        
            
            
        
        exclusion_activity_on_registeredchild_ids = obj_activity.search(cr, uid, [('validity_from','<=',prestation.prestation_date),
                                                              ('validity_to','>=',prestation.prestation_date),
                                                              ('onlyregisteredchilds','=', True),
                                                              ('childregistration_ids','!=', prestation.childid.id),
                                                              ])
        
        activity_ids = obj_activity.search(cr, uid, [('validity_from','<=',prestation.prestation_date),
                                      ('validity_to','>=',prestation.prestation_date),
                                      ('category','=',prestation.activitycategoryid.id),                               
                                      ('placeids','in', [place.id for place in prestation.placeid]),
                                      ('schoolimplantationids','in', [prestation.childid.schoolimplantation.id]),
                                      ('id', 'not in', exclusion_activity_ids), #on ne prend pas les activité avec une date d'excusion 
   #                                   ('id', 'not in', exclusion_activity_on_registeredchild_ids), #on ne prend pas les activités avec inscri uniquement et ou on est pas inscri 
                                      ('days','like','%'+str(datetime.datetime.strptime(prestation.prestation_date, '%Y-%m-%d').weekday())+'%'),
                                      ('leveltype','like','%'+prestation.childid.levelid.leveltype+'%'),
                                      ('prest_from', '<=', prestation.prestation_time),
                                      ('prest_to', '>=', prestation.prestation_time),
                                       ],
                                    order='prest_from DESC')
                                                
       
#        obj_activity.search(cr, uid, [('id' in activity_ids
 #                                      'childid not in'activity_ids
        print "activities finded : " + str(activity_ids)
        '''
        return activity_ids
            
    def _check(self,cr,uid,form, context=None):
        print '-----------------------'
        print 'Check'
#        print form
        obj_prestation = self.pool.get('extraschool.prestationtimes')
        
        if form['currentdate']:
            currentdate=datetime.datetime.strptime(form['currentdate'], '%Y-%m-%d')
        else:
            currentdate=datetime.datetime.strptime(form['period_from'], '%Y-%m-%d')
        periodto=datetime.datetime.strptime(form['period_to'], '%Y-%m-%d')
        for placeid in form['placeid']:
            while currentdate <= periodto:
                weekday = currentdate.weekday()
                strcurrentdate=str(currentdate)[0:10]                
                #On récupère la liste des enfants qui ont des présences dans la pếriode demandée
                cr.execute('select distinct("childid"),extraschool_child.name,childtypeid,levelid,schoolimplantation from "extraschool_prestationtimes"  left join "extraschool_child" on childid="extraschool_child".id where placeid=%s and "prestation_date"=%s and verified=FALSE', (placeid,strcurrentdate))
                childs = cr.dictfetchall()
                if childs:
                    print '-----------------------'
                    print 'Y a des gosses!'
                for child in childs:
                        '''
                        #On récupère le niveau de l'enfant en cours                    
                        cr.execute('select leveltype from extraschool_level where id=%s',(child['levelid'],))
                        try:
                            leveltype= cr.dictfetchall()[0]['leveltype']
                        except:
                            #Si pas de niveau erreur
                            raise osv.except_osv('Error','Error '+str(child['name'])+' '+strcurrentdate)                                             
                        #On récupère les présences de l'enfant en cours pour la date en cours
                        cr.execute('select * from "extraschool_prestationtimes" where placeid=%s and "prestation_date"=%s and "childid"=%s and activitycategoryid=%s order by prestation_time', (placeid,strcurrentdate,child['childid'],form['activitycategory']))
                        prestations = cr.dictfetchall()
                        '''
                        print '-----------------------'
                        print 'For child in childs'
                        #On est foutu on fait un browse
                        prestation_ids = obj_prestation.search(cr, uid, [('placeid','=',placeid),
                                                        ('prestation_date','=',strcurrentdate),
                                                        ('childid','=',child['childid']),
                                                        ('activitycategoryid','in',[form['activitycategory'][0]]),])
                        print '-----------------------'
                        print 'presta du gosse ('+str(child['childid'])+') : ' + str(prestation_ids)
                        
                        prestations = obj_prestation.browse(cr, uid, prestation_ids)
                        
                        for prestation in prestations:
                            prestation_activity_id = self.get_prestation_activityid(prestation)
                currentdate=currentdate+datetime.timedelta(1)
                        
                        
                        
                '''
                        cr.execute("""select * from "extraschool_activity" where validity_from <= %s and validity_to >= %s 
                                    and category=%s 
                                    and id in (select activity_id from extraschool_activity_place_rel where place_id=%s)
                                    and id in (select activity_id from extraschool_activity_schoolimplantation_rel where schoolimplantation_id=%s)
                                    and id in (select activity_id from extraschool_activity_childtype_rel where childtype_id=%s) 
                                    and id in (select activity_id from extraschool_activity_activityplanneddate_rel left join extraschool_activityplanneddate on activityplanneddate_id=extraschool_activityplanneddate.id where activitydate=%s) 
                                    and id not in (select activity_id from extraschool_activity_activityexclusiondates_rel left join extraschool_activityexclusiondates on activityexclusiondates_id = extraschool_activityexclusiondates.id where date_from <= %s and date_to >= %s)
                                    and leveltype like %s 
                                    and ((onlyregisteredchilds = FALSE) or (id in (select activity_id from extraschool_activitychildregistration where child_id=%s and registration_from <= %s and registration_to >= %s)))
                                    order by prest_from""", (strcurrentdate,strcurrentdate,activitycategory['id'],placeid,child['schoolimplantation'],child['childtypeid'],strcurrentdate,strcurrentdate,strcurrentdate,'%'+leveltype+'%',child['childid'],strcurrentdate,strcurrentdate))
                        plannedactivities=cr.dictfetchall()
                        if plannedactivities:
                            activities = plannedactivities
                            for plannedactivity in plannedactivities:
                                cr.execute("""select * from "extraschool_activity" where validity_from <= %s and validity_to >= %s 
                                        and ((prest_from < %s) or (prest_to > %s))
                                        and category=%s 
                                        and id in (select activity_id from extraschool_activity_place_rel where place_id=%s)
                                        and id in (select activity_id from extraschool_activity_schoolimplantation_rel where schoolimplantation_id=%s) 
                                        and id in (select activity_id from extraschool_activity_childtype_rel where childtype_id=%s) 
                                        and id not in (select activity_id from extraschool_activity_activityplanneddate_rel) 
                                        and days like %s 
                                        and id not in (select activity_id from extraschool_activity_activityexclusiondates_rel left join extraschool_activityexclusiondates on activityexclusiondates_id = extraschool_activityexclusiondates.id where date_from <= %s and date_to >= %s)
                                        and leveltype like %s order by prest_from""", (strcurrentdate,strcurrentdate,plannedactivity['prest_from'],plannedactivity['prest_to'],activitycategory['id'],placeid,child['schoolimplantation'],child['childtypeid'],'%'+str(weekday)+'%',strcurrentdate,strcurrentdate,'%'+leveltype+'%'))                
                                addactivities=cr.dictfetchall()
                                if addactivities:
                                    activities=addactivities+activities
                                    print activities
                                
                        else:
                            cr.execute("""select * from "extraschool_activity" where validity_from <= %s and validity_to >= %s 
                                        and category=%s 
                                        and id in (select activity_id from extraschool_activity_place_rel where place_id=%s)
                                        and id in (select activity_id from extraschool_activity_schoolimplantation_rel where schoolimplantation_id=%s) 
                                        and id in (select activity_id from extraschool_activity_childtype_rel where childtype_id=%s) 
                                        and id not in (select activity_id from extraschool_activity_activityplanneddate_rel) 
                                        and days like %s 
                                        and id not in (select activity_id from extraschool_activity_activityexclusiondates_rel left join extraschool_activityexclusiondates on activityexclusiondates_id = extraschool_activityexclusiondates.id where date_from <= %s and date_to >= %s)
                                        and leveltype like %s order by prest_from""", (strcurrentdate,strcurrentdate,activitycategory['id'],placeid,child['schoolimplantation'],child['childtypeid'],'%'+str(weekday)+'%',strcurrentdate,strcurrentdate,'%'+leveltype+'%'))
                            activities=cr.dictfetchall()
    
                        for activity in activities:
                            activityok = False
                            cr.execute('select count(*) as nbrchilds from extraschool_activitychildregistration where activity_id = %s', (activity['id'],))
                            if cr.dictfetchall()[0]['nbrchilds'] == 0:
                                #if activity['onlyregisteredchilds'] == False:
                                activityok = True
                            #peut etre a virer
                            else:
                                cr.execute('select count(*) as nbrchilds from extraschool_activitychildregistration where activity_id = %s and child_id = %s', (activity['id'],child['childid']))
                                if cr.dictfetchall()[0]['nbrchilds'] > 0:
                                    activityok = True
                            #---
                            if activityok:
                                prestactivity=[]
                                for prestation in prestations:
                                    if (activity['fixedperiod']):
                                        if (prestation['prestation_time'] >= activity['default_from']) and (prestation['prestation_time'] <= activity['default_to']):
                                            if not (((prestation['prestation_time'] == activity['default_from']) and (prestation['ES'] == 'S')) or ((prestation['prestation_time'] == activity['default_to']) and (prestation['ES'] == 'E'))):
                                                prestactivity.append(prestation)
                                    else:
                                        if (activity['default_from'] > 0):                             
                                            if (prestation['prestation_time'] > activity['default_from']) and (prestation['prestation_time'] <= activity['prest_to']):
                                                if not ((prestation['prestation_time'] == activity['prest_to']) and (prestation['ES'] == 'E')):
                                                    prestactivity.append(prestation)
                                        if (activity['default_to'] > 0):                                     
                                            if (prestation['prestation_time'] >= activity['prest_from']) and (prestation['prestation_time'] < activity['default_to']):                                        
                                                if not ((prestation['prestation_time'] == activity['prest_from']) and (prestation['ES'] == 'S')):                                                    
                                                    prestactivity.append(prestation)
                                if prestactivity:
                                    if (activity['fixedperiod']):
                                        for prest in prestations:
                                            if (prest['prestation_time'] >= activity['default_from']) and (prest['prestation_time'] <= activity['default_to']):
                                                obj_prestation.unlink(cr, uid, prest['id'])
                                        if not (obj_prestation.search(cr,uid, [('prestation_date', '=', prestactivity[0]['prestation_date']),('childid', '=', prestactivity[0]['childid']),('ES', '=', 'E'),('prestation_time', '=', activity['default_from'])])):
                                            self.insertprestation(cr,uid,placeid,prestactivity[0]['prestation_date'],prestactivity[0]['childid'],'E',activity['default_from'],activity['category'],False,activity['id'])                                
                                        if not (obj_prestation.search(cr,uid, [('prestation_date', '=', prestactivity[0]['prestation_date']),('childid', '=', prestactivity[0]['childid']),('ES', '=', 'S'),('prestation_time', '=', activity['default_to'])])):
                                            self.insertprestation(cr,uid,placeid,prestactivity[0]['prestation_date'],prestactivity[0]['childid'],'S',activity['default_to'],activity['category'],False,activity['id'])
                                    else:
                                        if (activity['default_from'] > 0):                                
                                            if prestactivity[0]['ES'] == 'S':                                    
                                                if not (obj_prestation.search(cr,uid, [('prestation_date', '=', prestactivity[0]['prestation_date']),('childid', '=', prestactivity[0]['childid']),('ES', '=', 'E'),('prestation_time', '=', activity['default_from'])])):
                                                    self.insertprestation(cr,uid,placeid,prestactivity[0]['prestation_date'],prestactivity[0]['childid'],'E',activity['default_from'],activity['category'],False,activity['id'])
                                        if (activity['default_to'] > 0):
                                            if prestactivity[len(prestactivity)-1]['ES'] == 'E':
                                                if not (obj_prestation.search(cr,uid, [('prestation_date', '=', prestactivity[0]['prestation_date']),('childid', '=', prestactivity[0]['childid']),('ES', '=', 'S'),('prestation_time', '=', activity['default_to'])])):
                                                    self.insertprestation(cr,uid,placeid,prestactivity[0]['prestation_date'],prestactivity[0]['childid'],'S',activity['default_to'],activity['category'],False,activity['id'])                           

                # Ajout automatique des activites                        
                cr.execute("""select extraschool_activity.id as id,prest_from,prest_to,category,leveltype,onlyregisteredchilds from extraschool_activity left join extraschool_activitycategory on category = extraschool_activitycategory.id where  
                    validity_from <= %s and validity_to >= %s 
                    and extraschool_activity.id in (select activity_id from extraschool_activity_place_rel where place_id=%s) 
                    and autoaddchilds = True 
                    and ((extraschool_activity.id in (select activity_id from extraschool_activity_activityplanneddate_rel left join extraschool_activityplanneddate on activityplanneddate_id=extraschool_activityplanneddate.id where activitydate = %s )) or (days like %s)) 
                    and extraschool_activity.id not in (select activity_id from extraschool_activity_activityexclusiondates_rel left join extraschool_activityexclusiondates on activityexclusiondates_id = extraschool_activityexclusiondates.id where date_from <= %s and date_to >= %s)
                    order by priorityorder,prest_from""",(strcurrentdate,strcurrentdate,placeid,strcurrentdate,'%'+str(weekday)+'%',strcurrentdate,strcurrentdate,))
                activities=cr.dictfetchall()
                for activity in activities:
                    cr.execute('select child_id as id from extraschool_activitychildregistration where activity_id = %s and registration_from <= %s and registration_to >= %s',(activity['id'],strcurrentdate,strcurrentdate))
                    #cr.execute('select child_id as id from extraschool_activity_child_rel where activity_id = %s',(activity['id'],))
                    childs=cr.dictfetchall()                
                    if not childs:
                        cr.execute('select count(*) as nbrchilds from extraschool_activitychildregistration where activity_id = %s', (activity['id'],))
                        if (cr.dictfetchall()[0]['nbrchilds'] == 0) and (activity['onlyregisteredchilds'] == False):                    
                            if (activity['leveltype']=='M') or (activity['leveltype']=='P'):                        
                                cr.execute('select * from extraschool_child where schoolimplantation in (select schoolimplantation_id from extraschool_place_schoolimplantation_rel where place_id = %s) and childtypeid in (select childtype_id from extraschool_activity_childtype_rel where activity_id=%s)  and levelid in (select id from extraschool_level where leveltype=%s)',(placeid,activity['id'],activity['leveltype'],))
                            else:
                                cr.execute('select * from extraschool_child where schoolimplantation in (select schoolimplantation_id from extraschool_place_schoolimplantation_rel where place_id = %s) and childtypeid in (select childtype_id from extraschool_activity_childtype_rel where activity_id=%s) ',(placeid,activity['id'],))
                            childs=cr.dictfetchall()
                    for child in childs:
                        prestids = obj_prestation.search(cr,uid, [('prestation_date', '=', strcurrentdate),('childid', '=', child['id']),('prestation_time', '>', activity['prest_from']),('prestation_time', '<', activity['prest_to']),('activitycategoryid.priorityorder', '<=', 2)])
                        jm = obj_prestation.unlink(cr, uid, prestids)
                        self.insertprestation(cr,uid,placeid,currentdate,child['id'],'E',activity['prest_from'],activity['category'],False,activity['id'])
                        self.insertprestation(cr,uid,placeid,currentdate,child['id'],'S',activity['prest_to'],activity['category'],False,activity['id'])
                    

                cr.execute('select distinct("childid"),childtypeid,placeid from "extraschool_prestationtimes"  left join "extraschool_child" on childid="extraschool_child".id where placeid=%s and "prestation_date"=%s', (placeid,strcurrentdate))
                childs = cr.dictfetchall()
                for child in childs:                                                                                                
                    cr.execute('select * from "extraschool_prestationtimes" where placeid=%s and "prestation_date"=%s and "childid"=%s order by prestation_time asc, "ES" desc, activitycategoryid asc', (placeid,strcurrentdate,child['childid']))
                    prestations = cr.dictfetchall()
                    es='E'                
                    prestationids=[]
                    if len(prestations)%2 != 0:
                        erreur=True
                    else:
                        currentactivitycategory=prestations[0]['activitycategoryid']
                        erreur=False
                    for prestation in prestations:
                        prestationids.append(prestation['id'])
                        if prestation['ES']!=es:
                            erreur=True
                        if es=='E':
                            currentactivitycategory=prestation['activitycategoryid']
                            es='S'
                        else:
                            if currentactivitycategory!=prestation['activitycategoryid']:
                                erreur=True
                            es='E'

                    if erreur:
                        return {'state' : 'prestations_to_verify','currentdate':strcurrentdate,'childid':child['childid']}
                    else:
                        for prestationid in prestationids:
                            cr.execute('update extraschool_prestationtimes set verified = TRUE where id=%s',(str(prestationid),))
                            #obj_prestation.write(cr,uid,[prestationid], {'verified':True})
                        
                currentdate=currentdate+datetime.timedelta(1)
            currentdate=datetime.datetime.strptime(form['period_from'], '%Y-%m-%d')
            '''
            return {'state' : 'end_of_verification',}        
    
    def action_prestationscheck(self, cr, uid, ids, context=None):        
        form = self.read(cr,uid,ids,)[-1] 
        print '-----------------------'
        print 't88888tu'
        return self.write(cr, uid, ids,self._check(cr,uid,form), context=context)


extraschool_prestationscheck_wizard()
