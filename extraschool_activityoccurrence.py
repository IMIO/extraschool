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
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
#import datetime


class extraschool_activityoccurrence(models.Model):
    _name = 'extraschool.activityoccurrence'
    _description = 'activity occurrence'

    name = fields.Char('Name', size=50)
    occurrence_date = fields.Date('Date')
    activityid = fields.Many2one('extraschool.activity', 'Activity')
    activityname = fields.Char(related='activityid.name')
    prest_from = fields.Float(related='activityid.prest_from')
    prest_to = fields.Float(related='activityid.prest_to')
    date_start = fields.Datetime('Date start',compute='_compute_date_start', store=True)
    date_stop = fields.Datetime('Date stop',compute='_compute_date_stop', store=True) 
    child_registration_ids = fields.Many2many('extraschool.child','extraschool_activityoccurrence_cild_rel', 'activityoccurrence_id', 'child_id','Child registration')        
    prestation_times_ids = fields.One2many('extraschool.prestationtimes', 'activity_occurrence_id','Child prestation times')   
    place_id = fields.Many2one('extraschool.place', 'Place', required=False)                     

    def name_get(self):            
        res=[]
        for occurrence in self:
            res.append((occurrence.id, occurrence.activityname + ' - ' + datetime.strptime(occurrence.occurrence_date, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y")))    

        return res    
        
    @api.depends('occurrence_date', 'prest_from')
    def _compute_date_start(self):
        for record in self:
            if record.occurrence_date:
                hour = int(record.prest_from)
                minute = int((record.prest_from - hour) * 60)
                hour = hour -1 if hour else 0         
                record.date_start = datetime.strptime(record.occurrence_date + ' ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00', DEFAULT_SERVER_DATETIME_FORMAT)        
            
    @api.depends('occurrence_date', 'prest_from')
    def _compute_date_stop(self):
        for record in self:
            if record.occurrence_date:
                hour = int(record.prest_to)
                minute = int((record.prest_to - hour) * 60)
                hour = hour -1 if hour else 0
                record.date_stop = datetime.strptime(record.occurrence_date + ' ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00', DEFAULT_SERVER_DATETIME_FORMAT)
    
    def add_presta(self,activity_occurrence,child_id,parent_activity_occurrence = None, verified = True, manualy_encoded = False, entry = True, exit = True,entry_time = None, exit_time = None,exit_all= False):
        prestation_times_obj = self.env['extraschool.prestationtimes']
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

            prestation_times_obj.create(prestation_time)
            if parent_activity_occurrence:
                #add only if opposite presta exist in parent occurrence
                prestation_left = prestation_times_obj.search([('id', 'in',[prestation.id for prestation in parent_activity_occurrence.prestation_times_ids]),
                                                    ('prestation_time', '<=', entry_time),
                                                    ])
                if len(prestation_left) and prestation_left[0].es == 'E':                             
                    parent_prestation_time['es'] = 'S'   
                    parent_prestation_time['prestation_time'] = entry_time   
                    prestation_times_obj.create(parent_prestation_time)
    
        if exit:
            prestation_time['es'] = 'S'   
            prestation_time['prestation_time'] = exit_time
            prestation_times_obj.create(prestation_time)
            if parent_activity_occurrence:
                #add only if opposite presta exist in parent occurrence
                prestation_right = prestation_times_obj.search([('id', 'in',[prestation.id for prestation in parent_activity_occurrence.prestation_times_ids]),
                                                    ('prestation_time', '>=', exit_time),
                                                    ])
                if len(prestation_right) and prestation_right[0].es == 'S':                   
                    parent_prestation_time['es'] = 'E'   
                    parent_prestation_time['prestation_time'] = exit_time   
                    prestation_times_obj.create(parent_prestation_time)
        
    @api.model
    def create(self, vals): 
        occurrence = super(extraschool_activityoccurrence, self).create(vals)
        
        activity = self.env['extraschool.activity'].browse(vals['activityid'])
        
        child_ids = []
        occurrence_date_str = vals['occurrence_date'].strftime(DEFAULT_SERVER_DATE_FORMAT)
        for child_registration in activity.childregistration_ids:
            if child_registration.registration_from <= occurrence_date_str and child_registration.registration_to >= occurrence_date_str and child_registration.place_id.id == vals['place_id']:
                child_ids.append(child_registration.child_id.id)
                
                if activity.autoaddchilds:
                    self.add_presta(occurrence, child_registration.child_id.id, None,False)
                    
        #use syntax to replace existing records by new records
        
        occurrence.child_registration_ids = [(6, False, child_ids)] 
        
        
        return occurrence
    



extraschool_activityoccurrence()
