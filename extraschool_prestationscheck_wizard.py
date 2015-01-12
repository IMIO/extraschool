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


class extraschool_prestationscheck_wizard(osv.osv_memory):
    _name = 'extraschool.prestationscheck_wizard'
    _placeids = []

    def _get_places(self, cr, uid, ids, field_names, arg=None, context=None):
        result = {ids[0]: self._placeids, 'nodestroy': True}
        return result

    def _set_places(self, cr, uid, ids, field_names, value, arg=None, context=None):
        self._placeids=value[0][2]
    
    def _get_prestations(self, cr, uid, ids, field_names, arg=None, context=None):
        obj_prestations = self.pool.get('extraschool.prestationtimes')
        wiz_obj = self.browse(cr, uid, ids)[0]
        prestations_ids=obj_prestations.search(cr, uid, [('childid', '=', wiz_obj.childid.id),('prestation_date', '=', wiz_obj.currentdate)], order='prestation_time')        
        result = {ids[0]:prestations_ids, 'nodestroy': True}
        return result

    def _set_prestations(self, cr, uid, ids, field_names, value, arg=None, context=None):
        return True
    
    def _get_pdaprestations(self, cr, uid, ids, field_names, arg=None, context=None):
        obj_pdaprestations = self.pool.get('extraschool.pdaprestationtimes')
        wiz_obj = self.browse(cr, uid, ids)[0]
        pdaprestations_ids=obj_pdaprestations.search(cr, uid, [('childid', '=', wiz_obj.childid.id),('prestation_date', '=', wiz_obj.currentdate)], order='prestation_time')        
        result = {ids[0]:pdaprestations_ids, 'nodestroy': True}
        return result

    
    def _get_activitycategory(self, cr, uid, ids, field_names, arg=None, context=None):
        obj_activitycategory = self.pool.get('extraschool.activitycategory')
        wiz_obj = self.browse(cr, uid, ids)[0]
        categories_ids=obj_activitycategory.search(cr, uid, [('schoolimplantation_ids', '=', wiz_obj.schoolimplantationid.id),], order='priorityorder')        
        result = {ids[0]:categories_ids, 'nodestroy': True}
        return result    

    def _get_defaultfrom(self,cr, uid, ids, context=None):
        cr.execute('select max(prestation_date) as prestation_date from extraschool_invoicedprestations')
        rec=cr.dictfetchall()[0]
        try:
            fromdate=datetime.datetime.strptime(rec['prestation_date'], '%Y-%m-%d').date()
            frommonth=fromdate.month+1
            fromyear=fromdate.year
            if frommonth == 13:
                frommonth = 12
                fromyear = fromyear +1
            strfrommonth=str(frommonth)
            if len(strfrommonth) == 1:
                strfrommonth='0'+strfrommonth
            return str(fromyear)+'-'+strfrommonth+'-01'            
        except:
            return str(datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,1))
            
    def _get_defaultto(self,cr, uid, ids, context=None):
        #todate=datetime.date(2013,11,1)
        cr.execute('select max(prestation_date) as prestation_date from extraschool_invoicedprestations')
        lastdate = cr.dictfetchall()[0]['prestation_date']
        if lastdate and (lastdate < datetime.datetime.now()):
            todate=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,1)-datetime.timedelta(1)
        else:
            month=datetime.datetime.now().month
            if month == 12:
                month=1
            else:
                month=month+1
            todate=datetime.date(datetime.datetime.now().year,month,1)-datetime.timedelta(1)
            
        return str(todate)
        

    _columns = {
        'placeid' : fields.function(fnct=_get_places,fnct_inv=_set_places, method=True, type='many2many', relation='extraschool.place', string='Places'), 
        'period_from' : fields.date('Period from', required=True),
        'period_to' : fields.date('Period to', required=True),
        'currentdate' : fields.date('Current date',readonly=True),
        'childid' : fields.many2one('extraschool.child', 'Child',readonly=True),        
        'prestations_id': fields.function(fnct=_get_prestations,fnct_inv=_set_prestations, method=True, type='one2many', relation='extraschool.prestationtimes', string='Prestations'), 
        'pdaprestations_id': fields.function(fnct=_get_pdaprestations, method=True, type='one2many', relation='extraschool.pdaprestationtimes', string=' PDA Prestations'), 
        'activitycategory': fields.many2one('extraschool.activitycategory', 'Activity category'),                
        'prestation_time' : fields.char('Time', size=5),
        'es' : fields.selection((('E','In'), ('S','Out')),'ES' ),       
        'state' : fields.selection(
            [('init', 'Init'),('prestations_to_verify', 'Prestations to verify'),('end_of_verification', 'End of verification')],
            'State', required=True
        ),
    }    
    _defaults = {
        'state' : lambda *a: 'init',  
        'period_from' : '2014-01-01',
        'period_to' : '2014-03-31', 
        'activitycategory' : 1,     
        #'period_from' : _get_defaultfrom,
        #'period_to' : _get_defaultto,
    }
    
    def onchange_prestations(self, cr, uid, ids, prestations, childid, currentdate):
        obj_prestation = self.pool.get('extraschool.prestationtimes')
        for prestation in prestations:            
            if prestation[0]==2:                        
                res = obj_prestation.unlink(cr, uid, [prestation[1]])
            if prestation[0]==1:
                res = obj_prestation.write(cr, uid,[prestation[1]], prestation[2])
            if prestation[0]==0:
                values=prestation[2]
                prestids = obj_prestation.search(cr,uid,[('childid', '=', childid),('prestation_date', '=', currentdate),('prestation_time', '=', values['prestation_time']),('ES', '=', values['ES'])])
                if not prestids:
                    values['childid']=childid
                    values['prestation_date']=currentdate
                    values['manualy_encoded']=True
                    res = obj_prestation.create(cr, uid, values)
        return False        
    
    def onchange_schoolimplantation(self, cr, uid, ids, schoolimplantationid):
        obj_activitycategory = self.pool.get('extraschool.activitycategory')
        v={}        
        categories_ids=obj_activitycategory.search(cr, uid, [('schoolimplantation_ids', '=', schoolimplantationid)])
        v['activitycategory']=categories_ids
        return {'value':v}
    
    def action_save_prestation(self, cr, uid, ids, context=None):     
        obj_prestation = self.pool.get('extraschool.prestationtimes')           
        form = self.read(cr,uid,ids,)[-1]
        if form['es'] and form['prestation_time'] and form['currentdate'] and form['childid'] and form['placeid']:
            prestation_time=form['prestation_time']
            prestation_id = obj_prestation.create(cr, uid, {'placeid':form['placeid'][0],'childid':form['childid'][0],'prestation_date':form['currentdate'],'prestation_time':prestation_time,'ES':form['es'],'activitycategoryid' : form['activitycategory'][0],'manualy_encoded':True}, context=context)           
            return self.write(cr, uid, ids,{'prestation_time' : '', 'prestation_date':None,'es':None,}, context=context)
        else:
            return False
    
    def onchange_record(self, cr, uid, ids, currentdate,childid):
        obj_prestations = self.pool.get('extraschool.prestationtimes')
        obj_pdaprestations = self.pool.get('extraschool.pdaprestationtimes')
        v={}        
        prestations_ids=obj_prestations.search(cr, uid, [('childid', '=', childid),('prestation_date', '=', currentdate)])
        pdaprestations_ids=obj_pdaprestations.search(cr, uid, [('childid', '=', childid),('prestation_date', '=', currentdate)])
        v['prestations_id']=prestations_ids
        v['pdaprestations_id']=pdaprestations_ids
        return {'value':v}

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

    def get_prestation_activityid(self, cr, uid, prestation):
        obj_activity = self.pool.get('extraschool.activity')
#        import pdb
#        pdb.set_trace()
        print "date checked=" + str(prestation.prestation_date)
        #
        #   Get activity with exclusion date matching the presta
        #
        exclusion_activity_ids = obj_activity.search(cr, uid, ['&',('validity_from','<=',prestation.prestation_date),
                                                              ('validity_to','>=',prestation.prestation_date),
                                                              '&',('exclusiondates_ids.date_from','<=', prestation.prestation_date),
                                                              ('exclusiondates_ids.date_to','>=', prestation.prestation_date),
                                                              ])
        #
        #   Get activity with registration ONLY and presta.childid not in childregistration_ids 
        #
        exclusion_activity_on_registeredchild_ids = obj_activity.search(cr, uid, ['&',('validity_from','<=',prestation.prestation_date),
                                                              ('validity_to','>=',prestation.prestation_date),
                                                              '&',('onlyregisteredchilds','=', True),
                                                              ('childregistration_ids','=', prestation.childid.id),
                                                              ])
        
        activity_ids = obj_activity.search(cr, uid, [('validity_from','<=',prestation.prestation_date),
                                      ('validity_to','>=',prestation.prestation_date),
                                      ('category','=',prestation.activitycategoryid.id),                               
                                      ('placeids','in', [place.id for place in prestation.placeid]),
                                      ('schoolimplantationids','in', [prestation.childid.schoolimplantation.id]),
                                      '&', ('id', 'not in', exclusion_activity_ids), #on ne prend pas les activité avec une date d'excusion 
                                      ('id', 'not in', exclusion_activity_on_registeredchild_ids), #on ne prend pas les activité avec inscri uniquement et ou on est pas inscri 
                                      ('prest_from', '<=', prestation.prestation_time),
                                      ('prest_to', '>=', prestation.prestation_time),
                                       ])
        
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
                            prestation_activity_id = self.get_prestation_activityid(cr, uid, prestation)
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
