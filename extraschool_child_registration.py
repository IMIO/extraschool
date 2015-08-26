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
from datetime import date
import datetime


class extraschool_child_registration(models.Model):
    _name = 'extraschool.child_registration'
    _description = 'Child registration'

    school_id = fields.Many2one('extraschool.school', required=True)
    class_id = fields.Many2one('extraschool.class', required=True)
    place_id = fields.Many2one('extraschool.place', required=True)
    activity_id = fields.Many2one('extraschool.activity', required=True)
    week = fields.Integer('Week', required=True)
    date_from = fields.Date('Date from', required=True)
    date_to = fields.Date('Date to', required=True)
    child_registration_line_ids = fields.One2many('extraschool.child_registration_line','child_registration_id')
    
class extraschool_child_registration_line(models.Model):
    _name = 'extraschool.child_registration_line'
    _description = 'Child registration line'
    
    child_registration_id = fields.Many2one('extraschool.child_registration', required=True)
    child_id = fields.Many2one('extraschool.child', required=True)
    monday = fields.Boolean('Monday')
    tuesday = fields.Boolean('Tuesday')
    wednesday = fields.Boolean('Wednesday')
    thursday = fields.Boolean('Thursday')
    friday = fields.Boolean('Friday')
    saterday = fields.Boolean('Saterday')
    sunday = fields.Boolean('Sunday')

    

