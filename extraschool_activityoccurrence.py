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

from openerp.osv import osv, fields
from openerp import api, modules
from datetime import date, datetime, timedelta as td

class extraschool_activityoccurrence(osv.osv):
    _name = 'extraschool.activityoccurrence'
    _description = 'activity occurrence'

    _columns = {
        'occurence_date' : fields.date('Date'),
        'activityid' : fields.many2one('extraschool.activity', 'Activity'),
        'activityname' : fields.related('activityid', 'name', type='char', string='name'),
        'prest_from' : fields.related('activityid', 'prest_from', type='float', string='prest_from'),
        'prest_to' : fields.related('activityid', 'prest_to', type='float', string='prest_to'),
        'date_start' : fields.datetime('Date start', store=True),
        
    }
    @api.depends('occurence_date', 'prest_from')
    def _compute_date_start(self):
        for record in self:
            hour = record.prest_from.floor
            minute = (record.prest_from - hour) * 100
            record.date_start = datetime.strptime(record.occurrence_date + ' ' + str(hour) + ':' + str(minute), '%Y-%m-%d %I:%M')        
        
    

extraschool_activityoccurrence()
