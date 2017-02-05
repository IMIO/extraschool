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
import cStringIO
import base64
import os
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschool_prestation_times_of_the_day_wizard(models.TransientModel):
    _name = 'extraschool.prestation_times_of_the_day_wizard'

    query_sql = fields.Text('Query Sql')
    
    @api.multi
    def reset(self):        
        for reg in self.env['extraschool.prestation_times_of_the_day'].browse(self._context.get('active_ids')):
            reg.reset()
        
        return True

    @api.multi
    def check(self):  
        self.merge_pod_dup()      
        for reg in self.env['extraschool.prestation_times_of_the_day'].search([('id', 'in', self._context.get('active_ids')),]):
            reg.check()
        
        return True

    @api.multi
    def last_check_entry_exit(self):        
        for reg in self.env['extraschool.prestation_times_of_the_day'].browse(self._context.get('active_ids')):
            reg.last_check_entry_exit()
        
        return True
    
    
    @api.multi
    def execute_sql(self):
        self.env.cr.execute(self.query_sql)
        
    @api.multi
    def del_pod_doublon(self):
        pda_doublon = """
                        select id, activity_category_id, date_of_the_day, child_id
                        from extraschool_prestation_times_of_the_day
                        where ('' || CASE WHEN activity_category_id is NULL 
                                THEN ''
                                ELSE activity_category_id::text END || to_char(date_of_the_day,'YYYY-MM-DD') || child_id) in ( 
                        select ('' || CASE WHEN activity_category_id is NULL 
                                THEN ''
                                ELSE activity_category_id::text END || to_char(date_of_the_day,'YYYY-MM-DD') || child_id) as zz
                        from extraschool_prestation_times_of_the_day
                        where date_of_the_day > '2016-02-01' 
                        group by zz
                        having count(*) > 1);
                    """                    
        self.env.cr.execute(pda_doublon)
        
        prestation_times_of_the_day_obj = self.env['extraschool.prestation_times_of_the_day']
        prestation_times_obj = self.env['extraschool.prestationtimes']
        pdaprestation_times_obj = self.env['extraschool.pdaprestationtimes']
        
        doublons = self.env.cr.dictfetchall()
        saved_activity_category_id = ''
        saved_date = ''
        saved_child = ''
        for doublon in doublons:
            if saved_activity_category_id != doublon['activity_category_id'] or saved_date != doublon['date_of_the_day'] or saved_child != doublon['child_id']:                 
                saved_activity_category_id = doublon['activity_category_id']
                saved_date = doublon['date_of_the_day']
                saved_child = doublon['child_id']    
            else:
                prestation_times_obj.search([('prestation_times_of_the_day_id', '=',doublon['id'])]).unlink()
                pdaprestation_times_obj.search([('prestation_times_of_the_day_id', '=',doublon['id'])]).unlink()
                prestation_times_of_the_day_obj.search([('id', '=',doublon['id'])]).unlink()
    
    @api.multi
    def merge_pod_dup(self):
        self.env['extraschool.prestation_times_of_the_day'].merge_duplicate_pod()
            
    @api.multi
    def reset_verified_pod_with_non_verified_presta(self):       
        pod_error = """
                        select distinct(prestation_times_of_the_day_id) as id
                        from extraschool_prestationtimes p
                        left join extraschool_prestation_times_of_the_day pod on pod.id = p.prestation_times_of_the_day_id
                        where p.verified = False and pod.verified = False;
                    """                    
        self.env.cr.execute(pod_error)

        pod_errors = self.env.cr.dictfetchall()
        pod_error_ids = [doublon['id'] for doublon in pod_errors]   
        
        self.env['extraschool.prestation_times_of_the_day'].browse(pod_error_ids).reset()    
        