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


class extraschool_prestationtimes(models.Model):
    _name = 'extraschool.prestationtimes'
    _description = 'Prestation Times'
    _order = 'prestation_date,prestation_time,activity_occurrence_id,es'
               
    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place', required=False)
    childid = fields.Many2one('extraschool.child', 'Child', domain="[('isdisabled','=',False)]", required=False, select=True, ondelete='RESTRICT')
    prestation_date = fields.Date('Date', select=True)
    prestation_time = fields.Float('Time', select=True, required=True)
    es = fields.Selection((('E','In'), ('S','Out')),'es' , select=True)  
    exit_all = fields.Boolean('Exit all',default=False)
    manualy_encoded = fields.Boolean('Manualy encoded', readonly=True)   
    verified = fields.Boolean('Verified',default=False)
    error_msg = fields.Char('Error', size=255)
    activity_occurrence_id = fields.Many2one('extraschool.activityoccurrence', 'Activity occurrence')  
    activity_name = fields.Char(related='activity_occurrence_id.activityname')
    prestation_times_of_the_day_id = fields.Many2one('extraschool.prestation_times_of_the_day', 'Prestation of the day')  
             
    @api.model
    def create(self, vals):        
        if (not vals['childid']) or (not vals['placeid']):  
            raise Warning('Child and Place must be filled')
        
        prestation_times_of_the_day_obj = self.env['extraschool.prestation_times_of_the_day']
        prestation_times_obj = self.env['extraschool.prestationtimes']
        

        prestaion_times_ids = prestation_times_obj.search([('placeid.id', '=',vals['placeid']),
                                                                 ('childid.id', '=',vals['childid']),
                                                                 ('prestation_date', '=',vals['prestation_date']),
                                                                 ('prestation_time', '=',vals['prestation_time']),
                                                                 ('es', '=',vals['es']),
                                                                 ])
            
        if not 'prestation_times_of_the_day_id' in vals:
            prestation_times_of_the_day_ids = prestation_times_of_the_day_obj.search([('child_id.id', '=', vals['childid']),
                                                                                    ('date_of_the_day', '=', vals['prestation_date']),
                                                                                    ])
            if not prestation_times_of_the_day_ids:
                vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_obj.create({'child_id' : vals['childid'],
                                                               'date_of_the_day' : vals['prestation_date'],
                                                               'verified' : False,
                                                               }).id
            else :
                vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_ids.id

        if prestaion_times_ids: #if same presta exist than update
            if 'exit_all' in vals :
                if vals['exit_all'] == False:
                    if prestaion_times_ids.exit_all:
                        vals['exit_all'] = True
            
            return prestaion_times_ids.write(vals)
        else:
            return super(extraschool_prestationtimes, self).create(vals)

    @api.multi
    def write(self, vals):
#            vals['verified'] = False
            return super(extraschool_prestationtimes, self).write(vals)
            
    def unlink(self):        
        for record in self:
                linked_prestation=self.search([('childid', '=', record.childid),('prestation_date', '=', self.prestation_date)])
                res = linked_prestation.write({'verified':False})
        return super(extraschool_prestationtimes, self).unlink(self.ids)
        
extraschool_prestationtimes()


