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

class extraschool_activityexclusiondates(models.Model):
    _name = 'extraschool.activityexclusiondates'
    _description = 'Activity exclusion dates'

    def name_get(self):
        res=[]
        for exc_date in self:
            res.append((exc_date.id, exc_date.date_from + ' - ' + exc_date.date_to))    
    
        return res     
    
    name = fields.Char('Name', required=True, default='***')        
    date_from = fields.Date('Date from', required=True, index=True)
    date_to = fields.Date('Date to', required=True, index=True)

extraschool_activityexclusiondates()
