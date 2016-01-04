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


class extraschool_activity_occurrence_correction_wizard(models.TransientModel):
    _name = 'extraschool.activity_occurrence_correction_wizard'

    date_from = fields.Date('Date from', required=True)
    date_to = fields.Date('Date to', required=True)     
    state = fields.Selection([('init', 'Init'),
                             ('redirect', 'Redirect'),],
                            'State', required=True, default='init'
                            )

    @api.multi
    def reset_populate(self):        
        for activity in self.env['extraschool.activity'].browse(self._context.get('active_ids')):
            occurrences = self.env['extraschool.activityoccurrence'].search([('activityid', '=', activity.id),
                                                                              ('occurrence_date', '>=', self.date_from),
                                                                              ('occurrence_date', '<=', self.date_to),
                                                                              ])
            print "delete occu !!!!"
            occurrences.unlink()
            activity.populate_occurrence(self.date_from, self.date_to)
        
        return True



    
