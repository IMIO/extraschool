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
    def _get_left_right(self,prestation_time,right = True):
        if right:
            return_prestation_time_rs = self.prestationtime_ids.filtered(lambda r: r.prestation_time >= prestation_time.prestation_time and r.id != prestation_time.id)
        else:
            return_prestation_time_rs = self.prestationtime_ids.filtered(lambda r: r.prestation_time <= prestation_time.prestation_time and r.id != prestation_time.id)
                
    def _completion(self, prestation_time):
        activity_occurrence_obj = self.pool.get('extraschool.activityoccurrence')
        print "++++++Completion+++++"
        print str(prestation_time)
        if prestation_time.es == 'E':
            right = True
            add_entry = False
            add_exit = True
            opposite = "S"
            default_from_to = "to"
        else:
            right = False
            add_entry = True
            add_exit = False
            opposite = "E"
            default_from_to = "from"
                                   
        next_prestation_times = self._get_left_right(prestation_time,right)
        #no next presta even in an other occurrence
        if not next_prestation_times:
            #add opposite presta in same occurrence 
            print "add missing presta"
            activity_occurrence_obj.add_presta(self.env.cr,self.env.uid,prestation_time.activity_occurrence_id, prestation_time.childid.id, None,True,False,add_entry,add_exit)
        else :
            next_prestation_time = next_prestation_times[0]
            #Check if opposite presta in same occurrence exist
            if prestation_time.activity_occurrence_id.id == next_prestation_time.activity_occurrence_id.id and next_prestation_time.es == opposite:
                #look for child presta in timeslot
                for occurrence in self._get_child_activity_occurrence_ids(prestation_time, prestation_time.activity_occurrence_id.activityid.prest_from, next_prestation_time.activity_occurrence_id.prest_to, True):
                    #add missing presta !!! register conflict must be handled in activity 
                    print "add"
                    print str(occurrence)
                    print "-------"
                    activity_occurrence_obj.add_presta(self.env.cr,self.env.uid,occurrence, prestation_time.childid.id, prestation_time.activity_occurrence_id)
            #Check if next presta is same es type and same occurrence ..... it could be an error
            elif prestation_time.activity_occurrence_id.id == next_prestation_time.activity_occurrence_id.id and next_prestation_time.es == prestation_time.es:
                print "else"

        
    def _check(self):
        print "_check presta of the day" 
        prestation_time_ids = [prestation_time.id for prestation_time in self.prestationtime_ids]
        print str(prestation_time_ids)
        
        self._check_doublon(False)
        for prestation_time in self.env['extraschool.prestationtimes'].browse(prestation_time_ids):
            self._completion(prestation_time)
                
                
                
            

extraschool_prestation_times_of_the_day()   
