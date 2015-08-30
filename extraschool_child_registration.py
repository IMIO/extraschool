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


class extraschool_child_registration(models.Model):
    _name = 'extraschool.child_registration'
    _description = 'Child registration'

    school_implantation_id = fields.Many2one('extraschool.schoolimplantation', required=True)
    class_id = fields.Many2one('extraschool.class', required=True, domain="[('schoolimplantation','=',school_implantation_id)]")
    place_id = fields.Many2one('extraschool.place', required=True, domain="[('schoolimplantation_ids','in',school_implantation_id)]")
    activity_id = fields.Many2one('extraschool.activity', required=True, domain="[('placeids','in',place_id)]")
    week = fields.Integer('Week', required=True)
    date_from = fields.Date('Date from', required=True)
    date_to = fields.Date('Date to', required=True)
    child_registration_line_ids = fields.One2many('extraschool.child_registration_line','child_registration_id',copy=True)
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
        

        monday,sunday = self.get_week_days(2015, self.week)
        print "week days : %s - %s" % (monday,sunday)
        print "monday : %s" % (monday)
        print "sunday : %s" % (sunday)
        self.date_from = monday
        self.date_to = sunday
    
    @api.one
    def update_child_list(self):
        print "update_child_list"
        childs = self.env['extraschool.child'].search([('schoolimplantation.id', '=', self.school_implantation_id.id),
                                                       ('classid.id', '=',self.class_id.id)])
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
        print "validate"
        if self.state == 'draft':
            self.state = 'to_validate'
        elif self.state == 'to_validate':
            self.state = 'validated'
            
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
                                occu.add_presta(occu, line.child_id.id, None,False)
                        
                        
#         childs = self.env['extraschool.child'].search([('schoolimplantation.id', '=', self.school_implantation_id.id),
#                                                        ('classid.id', '=',self.class_id.id)])
#         self.child_registration_line_ids.unlink()
#         #clear child list
#         self.child_registration_line_ids = [(5, 0, 0)]
#         child_reg = []
#         print "clear child list done"
#         for child in childs:
#             print "add child : %s" % (child)
#             child_reg.append((0,0,{'child_id': child,
#                                    }))
#         self.child_registration_line_ids = child_reg
            
        
    
class extraschool_child_registration_line(models.Model):
    _name = 'extraschool.child_registration_line'
    _description = 'Child registration line'
    
    child_registration_id = fields.Many2one('extraschool.child_registration', required=True, ondelete="cascade")
    child_id = fields.Many2one('extraschool.child', required=True)
    monday = fields.Boolean('Monday')
    tuesday = fields.Boolean('Tuesday')
    wednesday = fields.Boolean('Wednesday')
    thursday = fields.Boolean('Thursday')
    friday = fields.Boolean('Friday')
    saturday = fields.Boolean('Saturday')
    sunday = fields.Boolean('Sunday')


