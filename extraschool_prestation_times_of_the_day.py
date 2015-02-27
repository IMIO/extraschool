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
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
from datetime import date
import datetime


class extraschool_prestation_times_of_the_day(models.Model):
    _name = 'extraschool.prestation_times_of_the_day'

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        
        res=[]
        for presta in self.browse(cr, uid, ids,context=context):
            res.append((presta.id, presta.child_id.name + ' - ' + datetime.datetime.strptime(presta.date_of_the_day, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y")  ))    
    
        print str(res)

        return res      

    
    date_of_the_day = fields.Date(required=True)    
    child_id = fields.Many2one('extraschool.child', required=True)                    
    prestationtime_ids = fields.One2many('extraschool.prestationtimes','prestation_times_of_the_day_id')    
    pda_prestationtime_ids = fields.One2many('extraschool.pdaprestationtimes','prestation_times_of_the_day_id')    
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
                    saved_prestation_time.verified = False
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
        activity_occurrence_obj = self.env['extraschool.activityoccurrence']
           
        #get presta matching the root_activity
        prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.root_id.id == root_activity.id)    
        prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
        #check if first presta is an entry
        first_prestation_time = prestation_times_rs[0]
        if first_prestation_time.es == 'E':
            #correction if default_from_to
            if first_prestation_time.activity_occurrence_id.activityid.default_from_to == 'from_to':
                first_prestation_time.prestation_time = first_prestation_time.activity_occurrence_id.prest_from
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
                activity_occurrence_obj.add_presta(occurrence, self.child_id.id, None,True,False,True,False)
                #return presta added - the first one in prestationtime_ids 
                prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.id == root_activity.id)    
                prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
                return prestation_times_rs[0]
            else:
                self._add_comment("Unable to define an entry")
                return False
                    
    def _completion_exit(self,root_activity):
        activity_occurrence_obj = self.env['extraschool.activityoccurrence']
           
        #get presta matching the root_activity
        prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.root_id.id == root_activity.id)    
        prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
        #check if last presta is an exit
        last_prestation_time = prestation_times_rs[len(prestation_times_rs)-1]
        if last_prestation_time.es == 'S':
            #correction if default_from_to
            if last_prestation_time.activity_occurrence_id.activityid.default_from_to == 'from_to':
                last_prestation_time.prestation_time = last_prestation_time.activity_occurrence_id.prest_to            
            return last_prestation_time
        else:
            #get the default stop
            exit_time = root_activity.get_stop(root_activity)
            if exit_time:
                #get the occurrence of the root activity
                occurrence = self.env['extraschool.activityoccurrence'].search([('activityid.id', '=',root_activity.id),
                                                                                ('occurrence_date', '=', self.date_of_the_day),
                                                                                ('place_id.id', '=', last_prestation_time.placeid.id)])
                #add missing exit presta
                activity_occurrence_obj.add_presta(occurrence, self.child_id.id, None,True,False,False,True)
                #return presta added
                prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.id == root_activity.id)  
                prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)  
                return prestation_times_rs[len(prestation_times_rs)-1]
            else:
                self._add_comment("Unable to define an entry")
                return False
         
            
    def _occu_start_stop_completion(self,start_time,stop_time,occurrence,down,from_occurrence):
        print "->_occu_start_stop_completion"
        print occurrence.activityname
        occurrence_obj = self.env['extraschool.activityoccurrence']
        cr,uid = self.env.cr, self.env.user.id
        
        #init used to avoid adding presta in parent if not needed
        prest_from = -1
        prest_to = -1
        
        looked_activity = None
        #if start occurrence than entry is OK so do something ONLY if it's not entry occurrence
        if not start_time.activity_occurrence_id.id == occurrence.id:
            "this is NOT the start occurrence"
            if not down: #"UP"
                #if we are going up, start is exit of the occurrence that we are coming from
                prest_from = from_occurrence.prest_to
            else:
                prest_from = occurrence.prest_from
            #add entry presta
            occurrence_obj.add_presta(occurrence,self.child_id.id,None, True, False, True, False,prest_from)
        
        #if stop occurrence than exit is OK so do something ONLY if it's not exit occurrence
        if not stop_time.activity_occurrence_id.id == occurrence.id:
            "this is NOT the exit occurrence"
            if not down: #"UP"
                #in we are not in the root
                if occurrence.activityid.id != occurrence.activityid.root_id.id:
                    prest_to = occurrence.prest_to
                else:
                    #we are in the root and the exit is in an other occurrence so the exit is the entry of first occurrence in the way to the exit occurrence
                    #go up from exit occurrence until the last occurrence just before the root"
                    looked_activity = stop_time.activity_occurrence_id.activityid.parent_id
                    while looked_activity.parent_id.id != looked_activity.root_id.id:
                        looked_activity = looked_activity.parent_id
                                   
                    prest_to = looked_activity.prest_from                
            else:
                prest_to = occurrence.prest_to
                
            #add exit presta
            occurrence_obj.add_presta(occurrence,self.child_id.id,None, True, False, False, True,None,prest_to)
            
          
        #add parent entry and exit if needed
        if down and occurrence.activityid.id != occurrence.activityid.root_id.id and from_occurrence: #Down and Not in root 
            #if level >=2
            if occurrence.activityid.parent_id and occurrence.activityid.parent_id.id != occurrence.activityid.root_id.id:
                
                occurrence_obj.add_presta(from_occurrence,self.child_id.id,None, True, False, True if prest_to > 0 else False, True if prest_from > 0 else False,prest_to,prest_from) #from & to are inverted it's normal it's for parent 
            else: #just under the root level 1
                if not looked_activity:
                    looked_activity = stop_time.activity_occurrence_id.activityid.parent_id
                    while looked_activity.parent_id.id != looked_activity.root_id.id:
                        looked_activity = looked_activity.parent_id 
                if occurrence.id !=looked_activity.id:       
                    occurrence_obj.add_presta(from_occurrence,self.child_id.id,None, True, False, True if prest_to > 0 else False, True if prest_from > 0 else False,prest_to,prest_from) #from & to are inverted it's normal it's for parent             

        print "<-_occu_start_stop_completion"
        
        
    def _occu_completion(self,start_time,stop_time,occurrence,down,from_occurrence):
        if not occurrence:
            #first call of the fct .... Here we are .... let's go
            down = True
            occurrence = start_time.activity_occurrence_id
        self._occu_start_stop_completion(start_time,stop_time,occurrence,down,from_occurrence)
        
        #compute entry before going down
        if start_time.activity_occurrence_id.id == occurrence.id:
            #"this is the start"
            prest_from = start_time.prestation_time
        else:#
            if not down:
                #if we are going up, start is exit of the occurrence that we are comming from
                prest_from = from_occurrence.prest_to
            else:
                #to do check if entry presta exist in occurrence, check it with from_to
                prest_from = from_occurrence.prest_from

        #compute exit before going down
        if stop_time.activity_occurrence_id.id == occurrence.id:
            #"this is almost the end, we have reached the last occurrence"
            prest_to = stop_time.prestation_time
        else:     
            #to do check if EXIT exist in occurrence and check from_to     
            prest_to = occurrence.prest_to if occurrence.prest_to <= stop_time.prestation_time else stop_time.prestation_time
        
        print "down"
        #get child occurrence starting after current occu
        from_occurrence_id = from_occurrence.id if from_occurrence else -1
        child_occurrences = self.env['extraschool.activityoccurrence'].search([('activityid.id', 'in',occurrence.activityid.activity_child_ids.ids),
                                                                               ('activityid.id', '!=',from_occurrence_id),
                                                                            ('occurrence_date', '=', self.date_of_the_day),
                                                                            ('place_id.id', '=', occurrence.place_id.id),
                                                                            ('prest_from', '>=', prest_from),
                                                                            ('prest_to', '<=', prest_to)])
        for child_occurrence in child_occurrences:
            self._occu_completion(start_time,stop_time,child_occurrence,True,occurrence)

        # try to go up     
        # if entry and exit is in the current occurrence STOP
        if occurrence.id != start_time.activity_occurrence_id.id or occurrence.id != stop_time.activity_occurrence_id.id:
            if (from_occurrence == None and occurrence.activityid.parent_id) or (from_occurrence and occurrence.activityid.parent_id and occurrence.activityid.parent_id.id != from_occurrence.activityid.id):
                from_occurrence_id = from_occurrence.id if from_occurrence else -1
                parent_occurrences = self.env['extraschool.activityoccurrence'].search([('activityid.id', '=',occurrence.activityid.parent_id.id),
                                                                                   ('activityid.id', '!=',from_occurrence_id),
                                                                                ('occurrence_date', '=', self.date_of_the_day),
                                                                                ('place_id.id', '=', occurrence.place_id.id),
                                                                                ])
                
                self._occu_completion(start_time,stop_time,parent_occurrences,False,occurrence)
        else:
            return self      
        
        return self
          
    def check(self):
        print "_check presta of the day" 
        prestation_times_obj = self.env['extraschool.prestationtimes']
        cr,uid = self.env.cr, self.env.user.id
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
                print "child = " + self.child_id.name  
                print "date = " + str(self.date_of_the_day)
                start_time.verified = True
                print "start_time:" + start_time.childid.name + " " + start_time.activity_occurrence_id.activityname + " " + str(start_time.prestation_time) + " " + str(start_time.verified) 
                
            stop_time = self._completion_exit(root_activity)
            if stop_time :
                print "stop_time:" + str(stop_time.prestation_time)
                
            print "<-----<----"
            
            if start_time and stop_time:
                print "go"
                #delete all occurrence presta but not stop_time presta
 #               prestation_times_obj.unlink(cr,uid,self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.root_id.id == root_activity.id and r.id != start_time.id and r.id != stop_time.id).ids)
                start_time.verified = True
                stop_time.verified = True
                self._occu_completion(start_time,stop_time,None,True,None)
                
            else:
                #an error has been found and added to comment field
                self.verified = False
                
        return self
                
            

extraschool_prestation_times_of_the_day()   
