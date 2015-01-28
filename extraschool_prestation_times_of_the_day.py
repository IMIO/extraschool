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



class extraschool_prestation_times_of_the_day(models.Model):
    _name = 'extraschool.prestation_times_of_the_day'

    date_of_the_day = fields.Date(required=True)    
    child_id = fields.Many2one('extraschool.child', required=True)                    
    prestationtime_ids = fields.One2many('extraschool.prestationtimes','prestation_times_of_the_day_id')    
    verified = fields.Boolean()                

    def _check_doublon(self,strict=False):
        prestation_time_ids = [prestation_time.id for prestation_time in self.prestationtime_ids]
        
        saved_prestation_time = None
        verified = True
        for prestation_time in self.env['extraschool.prestationtimes'].browse(prestation_time_ids):
            if prestation_time.error_msg:
                self.verified = False
                return self
            #check doublon
            if saved_prestation_time == None:
                saved_prestation_time = prestation_time
            else:
                if (prestation_time.activity_occurrence_id == saved_prestation_time.activity_occurrence_id and prestation_time.es == saved_prestation_time.es) \
                or (prestation_time.es == saved_prestation_time.es and strict == True):
                    prestation_time.error_msg = "Duplicate"
                    saved_prestation_time.error_msg = "Duplicate"
                    verified = False
                
        self.verified = verified
        return self               
    def _get_child_activity_occurrence_ids(self,prestation_time,time_from,time_to,registered = True):
        #
        # !!!!  Could be better if we handle occurrence child and parent
        #
        #get occurrence in time slot
        return self.env['extraschool.activityoccurrence'].search([('occurrence_date', '=', prestation_time.prestation_date),
                                                           ('prest_from', '>=', time_from),
                                                           ('prest_to', '<=', time_to),
                                                           ('activityid', 'in', [activity.id for activity in prestation_time.activity_occurrence_id.activityid.activity_child_ids]),
                                                           ('child_registration_ids', '=', prestation_time.childid.id)                                                           
                                                           ])
                
    def _completion(self, prestation_time):
        activity_occurrence_obj = self.pool.get('extraschool.activityoccurrence')
        
        if prestation_time.es == 'E':           
            prestation_times_right = self.prestationtime_ids.filtered(lambda r: r.prestation_time > prestation_time.prestation_time)
            #no Exit presta even in an other occurrence
            if not prestation_times_right:
                #add exit presta 
                print "add exit presta"
            else :
                prestation_time_right = prestation_times_right[0]
                #Exit exit presta in same occurrence
                if prestation_time.activity_occurrence_id.id == prestation_time_right.activity_occurrence_id.id and prestation_time_right.es == 'S':
                    #look for child presta in timeslot
                    for occurrence in self._get_child_activity_occurrence_ids(prestation_time, prestation_time.activity_occurrence_id.activityid.prest_from, prestation_time_right.activity_occurrence_id.prest_to, True):
                        #add missing presta !!! register conflict must be handled in activity 
                        print "add"
                        print str(occurrence)
                        print "-------"
                        activity_occurrence_obj.add_presta(occurrence, prestation_time.childid.id, prestation_time.activity_occurrence_id)
                #Exit in other occurrence
                elif prestation_time.activity_occurrence_id.id == prestation_time_right.activity_occurrence_id.id and prestation_time_right.es == 'S':
                    print "else"
            
        
    def _check(self):
        prestation_time_ids = [prestation_time.id for prestation_time in self.prestationtime_ids]
        
        self._check_doublon(False)
        for prestation_time in self.env['extraschool.prestationtimes'].browse(prestation_time_ids):
            self._completion(prestation_time)
                
                
                
            

extraschool_prestation_times_of_the_day()   
