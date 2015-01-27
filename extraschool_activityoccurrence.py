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
        'occurrence_date' : fields.date('Date'),
        'activityid' : fields.many2one('extraschool.activity', 'Activity'),
        'activityname' : fields.related('activityid', 'name', type='char', string='name'),
        'prest_from' : fields.related('activityid', 'prest_from', type='float', string='prest_from'),
        'prest_to' : fields.related('activityid', 'prest_to', type='float', string='prest_to'),
        'date_start' : fields.datetime('Date start',compute='_compute_date_start', store=True),
        'date_stop' : fields.datetime('Date stop',compute='_compute_date_stop', store=True), 
        'child_registration_ids' : fields.many2many('extraschool.child','extraschool_activityoccurrence_cild_rel', 'activityoccurrence_id', 'child_id','Child registration'),        
        'prestation_times_ids' : fields.one2many('extraschool.prestationtimes', 'activity_occurrence_id','Child prestation times'),        
    }
    
    @api.depends('occurrence_date', 'prest_from')
    def _compute_date_start(self):
        for record in self:
            hour = int(record.prest_from)
            minute = int((record.prest_from - hour) * 60)
            hour = hour -1            
            record.date_start = datetime.strptime(record.occurrence_date + ' ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00', DEFAULT_SERVER_DATETIME_FORMAT)        
            
    @api.depends('occurrence_date', 'prest_from')
    def _compute_date_stop(self):
        for record in self:
            hour = int(record.prest_to)
            minute = int((record.prest_to - hour) * 60)
            hour = hour -1
            record.date_stop = datetime.strptime(record.occurrence_date + ' ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00', DEFAULT_SERVER_DATETIME_FORMAT)
    
    def create(self, cr, uid, vals, context = None): 
        id = super(extraschool_activityoccurrence, self).create(cr, uid, vals)
        
        activity = self.pool.get('extraschool.activity').browse(cr, uid, vals['activityid'])
        prestation_times_obj = self.pool.get('extraschool.prestationtimes')
        
        child_ids = []
        occurrence_date_str = vals['occurrence_date'].strftime(DEFAULT_SERVER_DATE_FORMAT)
        for child_registration in activity.childregistration_ids:
            if child_registration.registration_from <= occurrence_date_str and child_registration.registration_to >= occurrence_date_str:
                child_ids.append(child_registration.child_id)
                if activity.autoaddchilds:
                    prestation_time = {'placeid' : child_registration.place_id.id,
                                       'activitycategoryid' : activity.category.id,
                                       'childid' : child_registration.child_id.id,
                                       'prestation_date' : occurrence_date_str,
                                       'manualy_encoded' : False,
                                       'verified' : False,
                                       'activityid' : activity.id,
                                       'activity_occurrence_id' : id,
                                       }    
                                 
                    prestation_time['ES'] = 'E'   
                    prestation_time['prestation_time'] = activity.prest_from   
                    prestation_times_obj.create(cr,uid,prestation_time)

                    prestation_time['ES'] = 'S'   
                    prestation_time['prestation_time'] = activity.prest_to   
                    prestation_times_obj.create(cr,uid,prestation_time)

                    
        #use syntax to replace existing records by new records
        vals['child_registration_ids'] = [(6, False, child_ids)]        

        
        return id       


extraschool_activityoccurrence()
