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

class extraschool_pdaprestationtimes(models.Model):
    _name = 'extraschool.pdaprestationtimes'
    _description = 'PDA Prestation Times'
        
    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place', required=True)
    activitycategoryid = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=False)
    childid = fields.Many2one('extraschool.child', 'Child', required=False)
    prestation_date = fields.Date('Date')
    prestation_time = fields.Float('Time')
    es = fields.Selection((('E','In'),
                           ('S','Out')),'ES' )    
    prestation_times_of_the_day_id = fields.Many2one('extraschool.prestation_times_of_the_day', 'Prestation of the day')           


    @api.model
    def create(self,vals):               
        prestation_times_of_the_day_obj = self.env['extraschool.prestation_times_of_the_day']
        prestation_times_obj = self.env['extraschool.prestationtimes']
        
        prestation_times_of_the_day_ids = prestation_times_of_the_day_obj.search([('child_id.id', '=', vals['childid']),
                                                                                ('date_of_the_day', '=', vals['prestation_date']),
                                                                                ])
        if not prestation_times_of_the_day_ids:
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_obj.create({'child_id' : vals['childid'],
                                                           'date_of_the_day' : vals['prestation_date'],
                                                           }).id
        else :
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_ids.id
        
        prestation_times_obj.create(vals)
        return super(extraschool_pdaprestationtimes, self).create(vals)    
    
extraschool_pdaprestationtimes()
