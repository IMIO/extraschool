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
from openerp import api, modules
from datetime import date, datetime, timedelta as td
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)


class extraschool_activityoccurrence(osv.osv):
    _name = 'extraschool.activityoccurrence'
    _description = 'activity occurrence'

    _columns = {
        'name' : fields.char('Name', size=50),
        'occurrence_date' : fields.date('Date'),
        'activityid' : fields.many2one('extraschool.activity', 'Activity'),
        'activityname' : fields.related('activityid', 'name', type='char', string='name'),
        'prest_from' : fields.related('activityid', 'prest_from', type='float', string='prest_from'),
        'prest_to' : fields.related('activityid', 'prest_to', type='float', string='prest_to'),
        'date_start' : fields.datetime('Date start',compute='_compute_date_start', store=True),
        'date_stop' : fields.datetime('Date stop',compute='_compute_date_stop', store=True), 
        'child_registration_ids' : fields.many2many('extraschool.child','extraschool_activityoccurrence_cild_rel', 'activityoccurrence_id', 'child_id','Child registration'),        
        'prestation_times_ids' : fields.one2many('extraschool.prestationtimes', 'activity_occurrence_id','Child prestation times'),   
        'place_id' : fields.many2one('extraschool.place', 'Place', required=False),                     
    }

    def name_get(self, cr, uid, ids, context={}):            
            if not len(ids):
                return []
            
            res=[]
            for occurrence in self.browse(cr, uid, ids,context=context):
                res.append((occurrence.id, occurrence.activityname + ' - ' + occurrence.occurrence_date))    
    
            return res    
        
    @api.depends('occurrence_date', 'prest_from')
    def _compute_date_start(self):
        for record in self:
            if record.occurrence_date:
                hour = int(record.prest_from)
                minute = int((record.prest_from - hour) * 60)
                hour = hour -1            
                record.date_start = datetime.strptime(record.occurrence_date + ' ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00', DEFAULT_SERVER_DATETIME_FORMAT)        
            
    @api.depends('occurrence_date', 'prest_from')
    def _compute_date_stop(self):
        for record in self:
            if record.occurrence_date:
                hour = int(record.prest_to)
                minute = int((record.prest_to - hour) * 60)
                hour = hour -1
                record.date_stop = datetime.strptime(record.occurrence_date + ' ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00', DEFAULT_SERVER_DATETIME_FORMAT)
    
    def add_presta(self,cr,uid,activity_occurrence,child_id,parent_activity_occurrence = None, verified = True, manualy_encoded = False, entry = True, exit = True,entry_time = None, exit_time = None,exit_all= False):
        print "add_presta " + activity_occurrence.activityname
        prestation_times_obj = self.pool.get('extraschool.prestationtimes')
        entry_time = entry_time if entry_time else activity_occurrence.prest_from
        exit_time = exit_time if exit_time else activity_occurrence.prest_to
        
        prestation_time = {'placeid' : activity_occurrence.place_id.id,
                           'activitycategoryid' : activity_occurrence.activityid.category.id,
                           'childid' : child_id,
                           'prestation_date' : activity_occurrence.occurrence_date,
                           'manualy_encoded' : manualy_encoded,
                           'verified' : verified,
                           'activityid' : activity_occurrence.activityid.id,
                           'activity_occurrence_id' : activity_occurrence.id,
                           'exit_all': exit_all,
                           }    
        if parent_activity_occurrence:
            if parent_activity_occurrence.default_from_to == 'from_to' or exit_all:
                #Parent activity has default_from_to or exit_all has been found .... Don't add Parent presta
                parent_activity_occurrence = None
            else:
                parent_prestation_time = {'placeid' : parent_activity_occurrence.place_id.id,
                                          'activitycategoryid' : parent_activity_occurrence.activityid.category.id,
                                          'childid' : child_id,
                                          'prestation_date' : parent_activity_occurrence.occurrence_date,
                                          'manualy_encoded' : manualy_encoded,
                                          'verified' : verified,
                                          'activityid' : parent_activity_occurrence.activityid.id,
                                          'activity_occurrence_id' : parent_activity_occurrence.id,
                                          }

        if entry:
            prestation_time['es'] = 'E'               
            prestation_time['prestation_time'] = entry_time

            prestation_times_obj.create(cr,uid,prestation_time)
            if parent_activity_occurrence:
                #add only if opposite presta exist in parent occurrence
                prestation_left = prestation_times_obj.search(cr,uid,[('id', 'in',[prestation.id for prestation in parent_activity_occurrence.prestation_times_ids]),
                                                    ('prestation_time', '<=', entry_time),
                                                    ])
                if len(prestation_left) and prestation_left[0].es == 'E':                             
                    parent_prestation_time['es'] = 'S'   
                    parent_prestation_time['prestation_time'] = entry_time   
                    prestation_times_obj.create(cr,uid,parent_prestation_time)
    
        if exit:
            prestation_time['es'] = 'S'   
            prestation_time['prestation_time'] = exit_time
            print "--------------"
            print str(prestation_time)
            print "--------------"
            prestation_times_obj.create(cr,uid,prestation_time)
            if parent_activity_occurrence:
                #add only if opposite presta exist in parent occurrence
                prestation_right = prestation_times_obj.search(cr,uid,[('id', 'in',[prestation.id for prestation in parent_activity_occurrence.prestation_times_ids]),
                                                    ('prestation_time', '>=', exit_time),
                                                    ])
                if len(prestation_right) and prestation_right[0].es == 'S':                   
                    parent_prestation_time['es'] = 'E'   
                    parent_prestation_time['prestation_time'] = exit_time   
                    prestation_times_obj.create(cr,uid,parent_prestation_time)
        
    def create(self, cr, uid, vals, context = None): 
        occurrence_id = super(extraschool_activityoccurrence, self).create(cr, uid, vals)
        
        activity = self.pool.get('extraschool.activity').browse(cr, uid, vals['activityid'])
        activity_occurrence_obj = self.pool.get('extraschool.activityoccurrence')
        
        child_ids = []
        occurrence_date_str = vals['occurrence_date'].strftime(DEFAULT_SERVER_DATE_FORMAT)
        for child_registration in activity.childregistration_ids:
            if child_registration.registration_from <= occurrence_date_str and child_registration.registration_to >= occurrence_date_str and child_registration.place_id.id == vals['place_id']:
                child_ids.append(child_registration.child_id.id)
                if activity.autoaddchilds:
                    self.add_presta(cr,uid,activity_occurrence_obj.browse(cr,uid,occurrence_id), child_registration.child_id.id, None,False)
                    
        #use syntax to replace existing records by new records
        vals['child_registration_ids'] = [(6, False, child_ids)] 
        
        activity_occurrence_obj.write(cr,uid,[occurrence_id],vals)       
        
        return occurrence_id
    



extraschool_activityoccurrence()
