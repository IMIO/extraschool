# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia - Imio (<http://www.imio.be>).
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
from openerp import tools
from datetime import datetime

class extraschool_guardianprestationtimes(models.Model):
    _name = 'extraschool.guardianprestationtimes'
    _description = 'Guardian Prestation Times'

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        res = []
        for presta in self.browse(cr, uid, ids, context=context):
            res.append((presta.id, presta.guardianid.name + ' - ' + datetime.strptime(presta.prestation_date, '%Y-%m-%d').strftime('%d/%m/%Y')))
        return res

    guardianid = fields.Many2one('extraschool.guardian', 'Guardian', required=False)
    prestation_date = fields.Date('Date', select=True, index=True)
    prestation_date_str = fields.Char(compute="_compute_prestation_date_str",string='Date str', store=True)
    prestation_time = fields.Float('Time')
    es = fields.Selection((('E', 'In'), ('S', 'Out')), 'ES', index=True)
    manualy_encoded = fields.Boolean('Manualy encoded')
    exported = fields.Boolean('Exported', default=False)

    @api.onchange('prestation_date')
    @api.depends('prestation_date')
    def _compute_prestation_date_str(self):
        for presta in self:
            if presta.prestation_date:
                presta.prestation_date_str = datetime.strptime(presta.prestation_date, '%Y-%m-%d').strftime('%d/%m/%Y')

class extraschool_guardian_prestation_times_report(models.Model):
    _name = 'extraschool.guardian_prestation_times_report'
    _description = 'Guardian Prestation Times Report'
    _auto = False

    guardian_id = fields.Many2one('extraschool.guardian', 'Guardian', required=False,select=True)
    prestation_date = fields.Date('Date',select=True)
    prestation_date_str = fields.Char('Date str')
    day_duration = fields.Float('day duration')
    week = fields.Char('Week',select=True)

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'extraschool_guardian_prestation_times_report')
        cr.execute("""
            CREATE view extraschool_guardian_prestation_times_report as
                select 
                    MIN(egt.id) as id,
                    egt.guardianid as guardian_id, 
                    egt.prestation_date as prestation_date,
                    to_char(egt.prestation_date,'DD/MM/YYYY') as prestation_date_str, 
                    EXTRACT(WEEK FROM egt.prestation_date) || '/' || eg.weekly_schedule as week,
                    eg.weekly_schedule as weekly_schedule,
                    (sum(case when egt.es = 'S' then egt.prestation_time else 0 end) - sum(case when egt.es = 'E' then egt.prestation_time else 0 end)) as day_duration
                from extraschool_guardianprestationtimes egt
                left join extraschool_guardian eg on eg.id = egt.guardianid
                group by 
                    guardian_id,
                    egt.prestation_date,
                    weekly_schedule
                ORDER BY
                    guardian_id,
                    egt.prestation_date
        """)
