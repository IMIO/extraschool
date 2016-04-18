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

from openerp import models, api, fields, _
from openerp.api import Environment
from openerp.exceptions import except_orm, Warning, RedirectWarning


from datetime import date, datetime, timedelta as td

from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)


class extraschool_child_registration(models.Model):
    _name = 'extraschool.child_registration'
    _description = 'Child registration'

    school_implantation_id = fields.Many2one('extraschool.schoolimplantation', required=True, readonly=True, states={'draft': [('readonly', False)]})
    class_id = fields.Many2one('extraschool.class', readonly=True, states={'draft': [('readonly', False)]}, domain="[('schoolimplantation','=',school_implantation_id)]")
    place_id = fields.Many2one('extraschool.place', required=True, readonly=True, states={'draft': [('readonly', False)]}, domain="[('schoolimplantation_ids','in',school_implantation_id)]")
    activity_id = fields.Many2one('extraschool.activity', readonly=True, states={'draft': [('readonly', False)]}, domain="[('placeids','in',place_id)]")
    week = fields.Integer('Week', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_from = fields.Date('Date from', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_to = fields.Date('Date to', required=True, readonly=True, states={'draft': [('readonly', False)]})
    child_registration_line_ids = fields.One2many('extraschool.child_registration_line','child_registration_id',copy=True, readonly=True, states={'draft': [('readonly', False)]})
    comment = fields.Char('Comment')
    state = fields.Selection([('draft', 'Draft'),
                              ('to_validate', 'Ready'),
                              ('validated', 'Validated')],
                              'validated', required=True, default='draft'
                              )

    def get_week_days(self,year, week):
        d = date(year,1,1)
        if(d.weekday()>3):
            d = d+td(7-d.weekday())
        else:
            d = d - td(d.weekday())
        dlt = td(days = (week-1)*7)
        return d + dlt,  d + dlt + td(days=6)    
    
    @api.onchange('week')
    def onchange_week(self):
        print "onchange_week"
        if self.week > 53:
            self.week = 53
        if self.week < 1:
            self.week = 1
        

        monday,sunday = self.get_week_days(2016, self.week)
        print "week days : %s - %s" % (monday,sunday)
        print "monday : %s" % (monday)
        print "sunday : %s" % (sunday)
        self.date_from = monday
        self.date_to = sunday
    
    @api.one
    def update_child_list(self):
        print "update_child_list"
        
        if self.class_id:
            childs = self.env['extraschool.child'].search([('schoolimplantation.id', '=', self.school_implantation_id.id),
                                                           ('classid.id', '=',self.class_id.id)])
        else:
            childs = self.env['extraschool.child'].search([('schoolimplantation.id', '=', self.school_implantation_id.id),
                                                           ])
            
            
        self.child_registration_line_ids.unlink()
        #clear child list
        self.child_registration_line_ids = [(5, 0, 0)]
        child_reg = []
        print "clear child list done"
        for child in childs:
            print "add child : %s" % (child)
            child_reg.append((0,0,{'child_id': child,
                                   }))
        self.child_registration_line_ids = child_reg

    @api.one
    def validate(self):
        if self.env.context == None:
            self.env.context = {}
        
        if "wizard" not in self.env.context:
            self.env.context["wizard"]= False
            
        print "validate wizard-mode : %s" % (self.env.context["wizard"])
        
        pod_to_reset = []
        
        if self.state == 'to_validate' or self.env.context["wizard"]:
            print "validate - registration"
            line_days = [self.child_registration_line_ids.filtered(lambda r: r.monday),
                         self.child_registration_line_ids.filtered(lambda r: r.tuesday),
                         self.child_registration_line_ids.filtered(lambda r: r.wednesday),
                         self.child_registration_line_ids.filtered(lambda r: r.thursday),
                         self.child_registration_line_ids.filtered(lambda r: r.friday),
                         self.child_registration_line_ids.filtered(lambda r: r.saturday),
                         self.child_registration_line_ids.filtered(lambda r: r.sunday),
                         ] 

            d1 = datetime.strptime(self.date_from, DEFAULT_SERVER_DATE_FORMAT)
            d2 = datetime.strptime(self.date_to, DEFAULT_SERVER_DATE_FORMAT)

            delta = d2 - d1
            
            occu = self.env['extraschool.activityoccurrence']
            occu_reg = self.env['extraschool.activity_occurrence_child_registration']
            for day in range(delta.days + 1):
                current_day_date = d1 + td(days=day)
                if str(current_day_date.weekday()) in self.activity_id.days:
                    occu = occu.search([('activityid','=', self.activity_id.id),
                                           ('place_id','=', self.place_id.id),
                                           ('occurrence_date','=', current_day_date)])
                    if len(occu) == 1:
                        for line in line_days[current_day_date.weekday()]:
                            print "create reg for child : %s" % (line.child_id)
                            occu_reg.create({'activity_occurrence_id': occu.id,
                                             'child_id' :line.child_id.id,
                                             'child_registration_line_id': line.id
                                             })
                            if self.activity_id.autoaddchilds:
                                pod_to_reset = list(set(pod_to_reset + occu.add_presta(occu, line.child_id.id, None,False)))
             
            for pod in self.env['extraschool.prestation_times_of_the_day'].browse(pod_to_reset):
                pod.reset()           
                        
        if self.state == 'draft':
            self.state = 'to_validate'
        elif self.state == 'to_validate':
            self.state = 'validated'
        
        if self.env.context["wizard"]:
            self.state = 'validated'
            
            
    @api.one
    def validate_multi(self):
        if self.env.context == None:
            self.env.context = {}
        
        if "wizard" not in self.env.context:
            self.env.context["wizard"]= False
            
        print "validate MULTI wizard-mode : %s" % (self.env.context)

        if self.state == 'to_validate' or self.env.context["wizard"]:
            line_days = [self.child_registration_line_ids.filtered(lambda r: r.monday_activity_id),
                         self.child_registration_line_ids.filtered(lambda r: r.tuesday_activity_id),
                         self.child_registration_line_ids.filtered(lambda r: r.wednesday_activity_id),
                         self.child_registration_line_ids.filtered(lambda r: r.thursday_activity_id),
                         self.child_registration_line_ids.filtered(lambda r: r.friday_activity_id),
                         self.child_registration_line_ids.filtered(lambda r: r.saturday_activity_id),
                         self.child_registration_line_ids.filtered(lambda r: r.sunday_activity_id),
                         ] 

            d1 = datetime.strptime(self.date_from, DEFAULT_SERVER_DATE_FORMAT)
            d2 = datetime.strptime(self.date_to, DEFAULT_SERVER_DATE_FORMAT)

            delta = d2 - d1
            
            pod_to_reset = []
            occu = self.env['extraschool.activityoccurrence']
            occu_reg = self.env['extraschool.activity_occurrence_child_registration']
            for day in range(delta.days + 1):
                current_day_date = d1 + td(days=day)
                print "day: %s" % (current_day_date)
                for line in line_days[current_day_date.weekday()]:
                    print "line id: %s" % (line.id)
                    activity_days = [line.monday_activity_id,
                                     line.tuesday_activity_id,
                                     line.wednesday_activity_id,
                                     line.thursday_activity_id,
                                     line.friday_activity_id,
                                     line.saturday_activity_id,
                                     line.sunday_activity_id,                                    
                                     ]
                    activity_id=activity_days[current_day_date.weekday()]
                    print "cd:%s in line.days:%s" % (str(current_day_date.weekday()), str(activity_id.days))
                    if str(current_day_date.weekday()) in activity_id.days:
                        print "line in activity"
                        occu = occu.search([('activityid','=', activity_id.id),
                                           ('place_id','=', self.place_id.id),
                                           ('occurrence_date','=', current_day_date)])
                        
                        if len(occu) == 1:
                            print "il y a une occu"
                            print "create reg for child : %s" % (line.child_id)
                            occu_reg.create({'activity_occurrence_id': occu.id,
                                             'child_id' :line.child_id.id,
                                             'child_registration_line_id': line.id
                                             })
                            if activity_id.autoaddchilds:
                                print "auto add child    "
                                pod_to_reset = list(set(pod_to_reset + occu.add_presta(occu, line.child_id.id, None,False)))
            for pod in self.env['extraschool.prestation_times_of_the_day'].browse(pod_to_reset):
                pod.reset()           
                        
                        
        if self.state == 'draft':
            self.state = 'to_validate'
        elif self.state == 'to_validate':
            self.state = 'validated'

    @api.one
    def set_to_draft(self):
        if self.state == 'to_validate':
            self.state = 'draft'
        elif self.state == 'validated':            
            #delete all related records
            occu_reg_obj = self.env['extraschool.activity_occurrence_child_registration']
            prestation_times_obj = self.env['extraschool.prestationtimes']
            
            occu_reg_ids = occu_reg_obj.search([('child_registration_line_id', 'in', self.child_registration_line_ids.ids)])
            for occu_reg in occu_reg_ids:
                if occu_reg.activity_occurrence_id.activityid.autoaddchilds:
                    presta_ids = prestation_times_obj.search([('childid', '=', occu_reg.child_id.id),
                                                 ('activity_occurrence_id', '=',occu_reg.activity_occurrence_id.id)])
                    if len(presta_ids.filtered(lambda record: record.invoiced_prestation_id.id > 0)):
                        raise Warning(_("At least one registration line is already invoiced !"))
        
                    presta_ids.unlink()
            occu_reg_ids.unlink()     
            self.state = 'draft'   
            
    def get_summary(self):
        print "get_summary"
        result = {}
        for line in self.child_registration_line_ids:
            zz = 0
            for day in [line.monday_activity_id,line.tuesday_activity_id,line.wednesday_activity_id,line.thursday_activity_id,line.friday_activity_id]:
                if day.id:
                    if day.name not in result:
                        result[day.name] = [0,0,0,0,0]
                    
                    result[day.name][zz] += 1
                zz+=1    
                
        return result                          
                    
                    
                
                
                
            
        
    
class extraschool_child_registration_line(models.Model):
    _name = 'extraschool.child_registration_line'
    _description = 'Child registration line'
    
    _order = "child_lastname,child_firstname"
    
    child_registration_id = fields.Many2one('extraschool.child_registration', required=True, ondelete="cascade")
    child_id = fields.Many2one('extraschool.child', required=True)
    child_firstname = fields.Char(related="child_id.firstname", store=True)
    child_lastname = fields.Char(related="child_id.lastname", store=True)
    monday = fields.Boolean('Monday')    
    monday_activity_id = fields.Many2one('extraschool.activity' ,string="Monday", domain="[('selectable_on_registration','=',True)]")
    tuesday = fields.Boolean('Tuesday')
    tuesday_activity_id = fields.Many2one('extraschool.activity',string="Tuesday", domain="[('selectable_on_registration','=',True)]")
    wednesday = fields.Boolean('Wednesday')
    wednesday_activity_id = fields.Many2one('extraschool.activity',string="Wednesday", domain="[('selectable_on_registration','=',True)]")
    thursday = fields.Boolean('Thursday')
    thursday_activity_id = fields.Many2one('extraschool.activity',string="Thursday", domain="[('selectable_on_registration','=',True)]")
    friday = fields.Boolean('Friday')
    friday_activity_id = fields.Many2one('extraschool.activity',string="Friday", domain="[('selectable_on_registration','=',True)]")
    saturday = fields.Boolean('Saturday')
    saturday_activity_id = fields.Many2one('extraschool.activity',string="Saturday", domain="[('selectable_on_registration','=',True)]")
    sunday = fields.Boolean('Sunday')
    sunday_activity_id = fields.Many2one('extraschool.activity',string="Sunday", domain="[('selectable_on_registration','=',True)]")
    
    def child_must_be_printed(self):
        if not any((self.monday_activity_id.id, self.tuesday_activity_id.id, self.wednesday_activity_id.id, self.thursday_activity_id.id, self.friday_activity_id.id)):
            return False
        else:
            return True
    
    


