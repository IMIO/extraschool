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
from math import ceil

available_levels = (('M', 'Maternelle'), ('P', 'Primaire'), ('A', 'Autre'))


class extraschool_stat_activity(models.Model):
    _name = 'extraschool.stat_activity'
    _description = 'activity statistique'

    date = fields.Date(string='Date', index=True)
    activity_id = fields.Many2one('extraschool.activity', string='Activity', index=True)
    place_id = fields.Many2one('extraschool.place', string='Place', index=True)
    level = fields.Selection(available_levels, string='Level')
    nbr_child = fields.Integer(string='Nbr childs')
    child_id = fields.Many2one('extraschool.child', string='Child', index=True)
    es = fields.Char('es')

    def convert_time(self, time):
        return '{0:02.0f}:{1:02.0f}'.format(*divmod(time * 60, 60))

    @api.model
    def compute(self):
        period_range = 0.25
        # delete all records
        print "Running: activity Statistics"
        print"#Unlink activity Statistics"
        self.search([]).unlink()

        for activity in self.env['extraschool.activity'].search([('autoaddchilds', '=', False)]):
            insert_querry = """
                            insert into extraschool_stat_activity
                                (date, activity_id, place_id, level, nbr_child, child_id, es)                                    
                                select prestation_date, %s, placeid, level, count(*), child_id, es
                                from 
                                (select prestation_date, activityid, placeid, prestation_time, es, level, child_id
                                    from
                                    (select activityid, placeid, childid AS child_id, prestation_date, prestation_time, es, l.leveltype as level
                                    from extraschool_prestationtimes p
                                    left join extraschool_activityoccurrence o on o.id = p.activity_occurrence_id 
                                    left join extraschool_child c on c.id = p.childid
                                    left join extraschool_level l on l.id = c.levelid
                                    where o.activityid = %s AND p.es = 'E'
                                    ) zz
                                ) qq
                                group by activityid, placeid, prestation_date, level, child_id, es
                            """

            self.env.cr.execute(insert_querry, (
            activity.id, activity.id))
            self.env.invalidate_all()
        print "### END: Prestation Statistics ###"