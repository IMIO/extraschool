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

    @api.multi
    def name_get(self):
        res = []
        for child_registration in self:
            res.append((child_registration.id, _("Subscription from %s to %s") % (
            datetime.strptime(child_registration.date_from, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y"),
            datetime.strptime(child_registration.date_to, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y"))))
        return res

    school_implantation_id = fields.Many2one('extraschool.schoolimplantation', required=True, readonly=True, states={'draft': [('readonly', False)]})
    class_id = fields.Many2one('extraschool.class', readonly=True, states={'draft': [('readonly', False)]}, domain="[('schoolimplantation','=',school_implantation_id)]")
    place_id = fields.Many2one('extraschool.place', required=True, readonly=True, states={'draft': [('readonly', False)]}, domain="[('schoolimplantation_ids','in',school_implantation_id)]")
    activity_id = fields.Many2one('extraschool.activity', readonly=True, states={'draft': [('readonly', False)]}, domain="[('placeids','in',place_id)]")
    week = fields.Integer('Week', required=True, readonly=True, states={'draft': [('readonly', False)]}, help='Afin de trouver le bon numéro de semaine, Veuillez vous aider du champs situé juste en dessous afin de trouver le numéro de semaine. Une fois le numéro mis, l\'application recherchera et encodera toute seule les bonnes dates du numéro de semaine (Du lundi au vendredi)')
    date_from = fields.Date('Date from', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_to = fields.Date('Date to', required=True, readonly=True, states={'draft': [('readonly', False)]})
    child_registration_line_ids = fields.One2many('extraschool.child_registration_line','child_registration_id',copy=True, readonly=True, states={'draft': [('readonly', False)]})
    comment = fields.Char('Comment')
    day_ids = fields.Many2many('extraschool.day', 'extraschool_day_registration_rel', string='Days', help='Ceci permet de précocher pour tous les enfants, les jours que l\'on souhaite')
    error_duplicate_reg_line = fields.Boolean(string="Error", default = False)
    state = fields.Selection([('draft', 'Draft'),
                              ('to_validate', 'Ready'),
                              ('validated', 'Validated')],
                              'validated', required=True, default='draft'
                              )
    number_childs = fields.Char('Number of childs', readonly=True, default=0)
    levelid = fields.Many2one('extraschool.level', 'Level')

    @api.onchange('child_registration_line_ids')
    def compute_number_childs(self):

        self.number_childs = len(self.child_registration_line_ids)

    @api.onchange('day_ids')
    @api.one
    def onchange_day(self):
        list = []
        if not self.day_ids :
            for child in self.child_registration_line_ids:
                child.monday = False
                child.tuesday = False
                child.wednesday = False
                child.thursday = False
                child.friday = False
                child.saturday = False
                child.sunday = False
        else :
            for day in self.day_ids :
                day = day.id
                if day == 1:
                    for child in self.child_registration_line_ids:
                        child.monday = True
                elif day == 2:
                    for child in self.child_registration_line_ids:
                        child.tuesday = True
                elif day == 3:
                    for child in self.child_registration_line_ids:
                        child.wednesday = True
                elif day == 4:
                    for child in self.child_registration_line_ids:
                        child.thursday = True
                elif day == 5:
                    for child in self.child_registration_line_ids:
                        child.friday = True
                elif day == 6:
                    for child in self.child_registration_line_ids:
                        child.saturday = True
                elif day == 7:
                    for child in self.child_registration_line_ids:
                        child.sunday = True
                list.append(day)
                print list
                if 1 not in list :
                    for child in self.child_registration_line_ids:
                        child.monday = False
                if 2 not in list :
                    for child in self.child_registration_line_ids:
                        child.tuesday = False
                if 3 not in list :
                    for child in self.child_registration_line_ids:
                        child.wednesday = False
                if 4 not in list :
                    for child in self.child_registration_line_ids:
                        child.thursday = False
                if 5 not in list :
                    for child in self.child_registration_line_ids:
                        child.friday = False
                if 6 not in list :
                    for child in self.child_registration_line_ids:
                        child.saturday = False
                if 7 not in list :
                    for child in self.child_registration_line_ids:
                        child.sunday = False


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
        

        monday,sunday = self.get_week_days(datetime.now().year, self.week)
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
        if self.levelid:
            childs = self.env['extraschool.child'].search([('schoolimplantation.id', '=', self.school_implantation_id.id),
                                                           ('levelid.id', '=',self.levelid.id)])
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
        self.compute_number_childs()

    @api.multi
    def check_validity_date(self, vals):
        # Check if values has passed (create or write). If not take from parent Object.
        date_from = vals['date_from'] if 'date_from' in vals else self.date_from
        date_to = vals['date_to'] if 'date_to' in vals else self.date_to

        if date_to < date_from:
            raise Warning(_("The date from must be lower than the date to"))

    @api.multi
    def write(self,vals):
        self.check_validity_date(vals)

        res = super(extraschool_child_registration, self).write(vals)
        return res

    @api.model
    def create(self,vals):
        self.check_validity_date(vals)

        res = super(extraschool_child_registration, self).create(vals)
        return res


    def check_doublons(self):
        print "in check doublons"
        child_ids = [line.child_id for line in self.child_registration_line_ids]
        if len(set(child_ids)) != len(self.child_registration_line_ids):
            self.error_duplicate_reg_line = True
            print "!!! dup !!!"
            for line in self.child_registration_line_ids:
                dup_line_ids = self.child_registration_line_ids.filtered(lambda r: r.id != line.id and r.child_id == line.child_id)
                if len(dup_line_ids):
                    line.error_duplicate_reg_line = True
                    dup_line_ids.write({'error_duplicate_reg_line' : True})                                        
        else:
            self.error_duplicate_reg_line = False
            self.child_registration_line_ids.write({'error_duplicate_reg_line' : False})

    def check_doublons_warning(self):
        self.check_doublons()
        
        if self.error_duplicate_reg_line:
            msg = _("These childs are duplicated !!\n")
            for dup in set(self.child_registration_line_ids.filtered(lambda r: r.error_duplicate_reg_line == True)):
                msg += "%s %s\n" % (dup.child_id.firstname,dup.child_id.lastname)
            raise Warning(msg)
        
    @api.one
    def validate(self):
        if self.env.context == None:
            self.env.context = {}
        
        wizard = False
        if "wizard" in self.env.context:
            wizard = self.env.context["wizard"]
        
        if not wizard:        
            self.check_doublons_warning()

        print "validate wizard-mode : %s" % (self.env.context["wizard"])
        
        pod_to_reset = []
        
        if self.state == 'to_validate' or wizard:
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
        
        if wizard:
            self.state = 'validated'
            
        if self.state == 'validated':
            self.error_duplicate_reg_line = False
            self.child_registration_line_ids.write({'error_duplicate_reg_line' : False})                 
            
            
    @api.one
    def validate_multi(self):
        print "validate multi"
        if self.env.context == None:
            self.env.context = {}
        
        wizard = False
        if "wizard" in self.env.context:
            wizard = self.env.context["wizard"]

        if not wizard:
            print "check_dup"
            self.check_doublons_warning()           
            
        print "validate MULTI wizard-mode : %s" % (self.env.context)

        if self.state == 'to_validate' or wizard:
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
                            occu_reg_ids = occu_reg.search([('activity_occurrence_id.id', '=', occu.id),
                                                            ('child_id.id' ,'=', line.child_id.id),
                                                            ('child_registration_line_id.id', '=', line.id)])
                            if len(occu_reg_ids):
                                msg = _("Duplicated registration\n")
                                for occu_reg_id in occu_reg_ids:
                                    msg += "%s - %s -%s\n" % (occu_reg_id.child_id.name,
                                                         occu_reg_id.activity_occurrence_id.name,
                                                         line.child_registration_id
                                                        ) 
                                    raise Warning(msg)
                                
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
            
        if wizard:
            self.state = 'validated'   
            
        if self.state == 'validated':
            self.error_duplicate_reg_line = False
            self.child_registration_line_ids.write({'error_duplicate_reg_line' : False})                 

    @api.one
    def force_set_to_draft(self):
        #delete all related records
        occu_reg_obj = self.env['extraschool.activity_occurrence_child_registration']
        prestation_times_obj = self.env['extraschool.prestationtimes']
        occu_reg_ids = occu_reg_obj.search([('child_registration_line_id.child_registration_id', '=', self.id)])
        print "occu_reg_ids : %s" % (occu_reg_ids)
        for occu_reg in occu_reg_ids:
            if occu_reg.activity_occurrence_id.activityid.autoaddchilds:
                presta_ids = prestation_times_obj.search([('childid', '=', occu_reg.child_id.id),
                                             ('activity_occurrence_id', '=',occu_reg.activity_occurrence_id.id)])
                if len(presta_ids.filtered(lambda record: record.invoiced_prestation_id.id > 0)):
                    raise Warning(_("At least one registration line is already invoiced !"))
                presta_ids.unlink()
        occu_reg_ids.unlink()
        self.state = 'draft'

    @api.one
    def set_to_draft(self):
        if self.state == 'to_validate':
            self.state = 'draft'
            self.force_set_to_draft()
        elif self.state == 'validated':            
            self.force_set_to_draft()
            
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

    @api.multi
    @api.one
    def unlink(self):
        if self.state == 'validated':
            raise Warning(_("Your are not allowed to delete a validated registration !!"))
                                
        return super(extraschool_child_registration,self).unlink()                            
    
class extraschool_child_registration_line(models.Model):
    _name = 'extraschool.child_registration_line'
    _description = 'Child registration line'
    
    _order = "child_lastname,child_firstname"
    
    child_registration_id = fields.Many2one('extraschool.child_registration', required=True, ondelete="cascade", index = True)
    child_id = fields.Many2one('extraschool.child', required=True, index = True)
    child_firstname = fields.Char(related="child_id.firstname", store=True)
    child_lastname = fields.Char(related="child_id.lastname", store=True)
    child_level = fields.Char(related="child_id.levelid.name",string="Niveau", store=True)
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
    error_duplicate_reg_line = fields.Boolean(string="Error", default = False)
    
    def child_must_be_printed(self):
        if not any((self.monday_activity_id.id, self.tuesday_activity_id.id, self.wednesday_activity_id.id,
                    self.thursday_activity_id.id, self.friday_activity_id.id)) and not any((self.monday,
                                                                                           self.tuesday,
                                                                                           self.wednesday,
                                                                                           self.thursday,
                                                                                           self.friday)):
            return False
        else:
            return True
    
    

class extraschool_day(models.Model):
    _name = 'extraschool.day'

    name = fields.Char('name')
