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
    comment = fields.Text()
        

    def _check_duplicate(self,strict=False):
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
                                                           ('activityid.autoaddchilds', '=', False)                                                        
                                                           ])
    
    def _get_left_right(self,prestation_time,right = True):
        if right:
            return_prestation_time_rs = self.prestationtime_ids.filtered(lambda r: r.prestation_time >= prestation_time.prestation_time and r.id != prestation_time.id)
        else:
            return_prestation_time_rs = self.prestationtime_ids.filtered(lambda r: r.prestation_time <= prestation_time.prestation_time and r.id != prestation_time.id)
                
#     def _completion(self, prestation_time):
#         activity_occurrence_obj = self.pool.get('extraschool.activityoccurrence')
#         print "++++++Completion+++++"
#         print str(prestation_time)
#         if prestation_time.es == 'E':
#             right = True
#             add_entry = False
#             add_exit = True
#             opposite = "S"
#             default_from_to = "to"
#         else:
#             right = False
#             add_entry = True
#             add_exit = False
#             opposite = "E"
#             default_from_to = "from"
#                                    
#         next_prestation_times = self._get_left_right(prestation_time,right)
#         #no next presta even in an other occurrence
#         if not next_prestation_times:
#             #add opposite presta in same occurrence 
#             print "add missing presta"
#             if prestation_time.activity_occurrence_id.activityid.default_from_to == default_from_to:
#                 activity_occurrence_obj.add_presta(self.env.cr,self.env.uid,prestation_time.activity_occurrence_id, prestation_time.childid.id, None,True,False,add_entry,add_exit)
#             else:
#                 prestation_time.error_msg = 'Entry without Exit or Exit without Entry'
#                 return self
#         else :
#             next_prestation_time = next_prestation_times[0]
#             #Check if opposite presta is in same occurrence
#             if prestation_time.activity_occurrence_id.id == next_prestation_time.activity_occurrence_id.id:
#                 if next_prestation_time.es != opposite:
#                     #error duplicate presta of same type
#                     prestation_time.error_msg = next_prestation_time.error_msg = "Duplicate"
#                 else :                    
#                     #look for child presta in timeslot
#                     for occurrence in self._get_child_activity_occurrence_ids(prestation_time, prestation_time.activity_occurrence_id.activityid.prest_from, next_prestation_time.activity_occurrence_id.prest_to, True):
#                         #add missing presta !!! register conflict must be handled in activity 
#                         print "add"
#                         print str(occurrence)
#                         print "-------"
#                         activity_occurrence_obj.add_presta(self.env.cr,self.env.uid,occurrence, prestation_time.childid.id, prestation_time.activity_occurrence_id)
#             else: #Next presta is not in same occurrence
#                 if next_prestation_time.exit_all: #kid go home
#                     
#                     activity_occurrence_obj.add_presta(self.env.cr,self.env.uid,next_prestation_time.activity_occurrence_id, prestation_time.childid.id, prestation_time.activity_occurrence_id,True,False,True,True,None,next_prestation_time.prestation_time)
#                     return self
#                 if prestation_time.activity_occurrence_id.id == next_prestation_time.activity_occurrence_id.id and next_prestation_time.es == prestation_time.es:
#                 print "else"

    def _add_comment(self,comment,reset=False):
        tmp_comment = self.comment
        if not tmp_comment:
            tmp_comment = "" 
        if reset:
            tmp_comment = ""
        tmp_comment = tmp_comment + "\n" if tmp_comment else tmp_comment
        
        self.comment = tmp_comment + comment 
        
        return self

    def _completion_entry(self,root_activity):
        activity_occurrence_obj = self.pool.get('extraschool.activityoccurrence')
           
        #get presta matching the root_activity
        prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.root_id.id == root_activity.id)    
        prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
        #check if first presta is an entry
        first_prestation_time = prestation_times_rs[0]
        if first_prestation_time.es == 'E':
            return first_prestation_time
        else:
            #get the default start
            entry_time = root_activity.get_start(root_activity)
            if entry_time:
                #get the occurrence of the root activity
                occurrence = self.env['extraschool.activityoccurrence'].search([('activityid.id', '=',root_activity.id),
                                                                                ('occurrence_date', '=', self.date_of_the_day),
                                                                                ('place_id.id', '=', first_prestation_time.placeid.id)])
                #add missing entry presta
                activity_occurrence_obj.add_presta(self.env.cr,self.env.uid,occurrence, self.child_id.id, None,True,False,True,False)
                #return presta added - the first one in prestationtime_ids 
                prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.id == root_activity.id)    
                prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
                return prestation_times_rs[0]
            else:
                self._add_comment("Unable to define an entry")
                return False
                    
    def _completion_exit(self,root_activity):
        activity_occurrence_obj = self.pool.get('extraschool.activityoccurrence')
           
        #get presta matching the root_activity
        prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.root_id.id == root_activity.id)    
        prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
        #check if first presta is an exit
        last_prestation_time = prestation_times_rs[len(prestation_times_rs)-1]
        if last_prestation_time.es == 'S':
            return last_prestation_time
        else:
            #get the default start
            entry_time = root_activity.get_start(root_activity)
            if entry_time:
                #get the occurrence of the root activity
                occurrence = self.env['extraschool.activityoccurrence'].search([('activityid.id', '=',root_activity.id),
                                                                                ('occurrence_date', '=', self.date_of_the_day),
                                                                                ('place_id.id', '=', last_prestation_time.placeid.id)])
                #add missing entry presta
                activity_occurrence_obj.add_presta(self.env.cr,self.env.uid,occurrence, self.child_id.id, None,True,False,False,True)
                #return presta added
                prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.id == root_activity.id)  
                prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)  
                return prestation_times_rs[len(prestation_times_rs)-1]
            else:
                self._add_comment("Unable to define an entry")
                return False
    def _occu_start_stop_completion(self,occurrence):
        print occurrence.id
        
    def _occu_completion(self,start_time,stop_time,occurrence,down,from_occurrence):
        if not occurrence:
            #first call of the fct .... Here we are .... let's go
            down = True
            occurrence = start_time.activity_occurrence_id
        self._occu_start_stop_completion(occurrence)
        if stop_time.activity_occurrence_id.id == occurrence.id:
            "this is the end, we have reached the last occurrence"
            return self
        
        print "down"
        #get child occurrence starting after current occu
        from_occurrence_id = from_occurrence.id if from_occurrence else -1
        child_occurrences = self.env['extraschool.activityoccurrence'].search([('activityid.id', 'in',occurrence.activityid.activity_child_ids.ids),
                                                                               ('activityid.id', '!=',from_occurrence_id),
                                                                            ('occurrence_date', '=', self.date_of_the_day),
                                                                            ('place_id.id', '=', occurrence.place_id.id),
                                                                            ('prest_from', '>=', occurrence.prest_from),
                                                                            ('prest_to', '<=', occurrence.prest_to)])
        for child_occurrence in child_occurrences:
            self._occu_completion(start_time,stop_time,child_occurrence,True,occurrence)

        # try to go up         
        if (from_occurrence == None and occurrence.activityid.parent_id) or (from_occurrence and occurrence.parent_id and occurrence.parent_id.id != from_occurrence.id):
            self._occu_completion(start_time,stop_time,occurrence.parent_id,False,occurrence)
        else:
            return self      
        
        return self
          
    def check(self):
        print "_check presta of the day" 
        prestation_time_ids = [prestation_time.id for prestation_time in self.prestationtime_ids]
        print str(prestation_time_ids)
        #if no presta than error and exit
        if not self.prestationtime_ids:
            self._add_comment("Error : No presta found",True)
            self.verified = False
            return self 
                   
        #Get distinct ROOT activity ID
        str_prestation_ids = str(self.prestationtime_ids.ids).replace('[','(').replace(']',')')
        self.env.cr.execute("select distinct(root_id) from extraschool_prestationtimes ep left join extraschool_activityoccurrence o on ep.activity_occurrence_id = o.id left join extraschool_activity a on o.activityid = a.id where a.root_id > 0 and ep.id in " + str_prestation_ids)

        prestationtimes = self.env.cr.dictfetchall()
        root_ids = [r['root_id'] for r in prestationtimes]
        
        for root_activity in self.env['extraschool.activity'].browse(root_ids):
            print "loop-" + str(root_activity)
            print "-> IN loop-" + str(root_activity)   
            start_time = self._completion_entry(root_activity)
            if start_time :
                print "start_time:" + str(start_time.prestation_time)
            stop_time = self._completion_exit(root_activity)
            if stop_time :
                print "stop_time:" + str(stop_time.prestation_time)
            print "<-----<----"
            
            if start_time and stop_time:
                print "go"
                self._occu_completion(start_time,stop_time,None,True,None)
            else:
                #an error has been found and added to comment field
                self.verified = False
        
        return self
                
            

extraschool_prestation_times_of_the_day()   
