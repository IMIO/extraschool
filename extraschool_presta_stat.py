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
class extraschool_presta_stat(models.Model):
    _name = 'extraschool.presta_stat'
    _description = 'Prestation statistique'

    date = fields.Date(string='Date', index = True) 
    activity_id = fields.Many2one('extraschool.activity', string = 'Activity', index = True)
    place_id = fields.Many2one('extraschool.place', string = 'Place', index = True)
    rancge = fields.Char(string = 'Range', index = True)
    nbr_child = fields.Integer(string = 'Nbr childs')
    
    def compute(self):
        period_range = 0.5
        #delete all records
        print"unlink presta stat"
        self.search([]).unlink()
        
        for activity in self.env['extraschool.activity'].search([('default_from_to','<>','from_to')]):
            nbr_period = int(ceil((activity.prest_to-activity.prest_from) / period_range))
            last_period = activity.prest_from 
            for period in range(0,nbr_period):
                insert_querry = """
                                insert into extraschool_presta_stat
                                    (date, activity_id, place_id, rancge, nbr_child)                                    
                                    select prestation_date, %s, placeid, %s, count(*)
                                    from 
                                    (select prestation_date, activityid, placeid, prestation_time, es
                                        from
                                        (select activityid, placeid, childid, prestation_date, prestation_time, es
                                        from extraschool_prestationtimes p
                                        left join extraschool_activityoccurrence o on o.id = p.activity_occurrence_id 
                                        where o.activityid = %s and
                                              p.prestation_time <= %s and
                                              p.prestation_time =
                                            (
                                              select max(pp.prestation_time)
                                              from extraschool_prestationtimes pp
                                              left join extraschool_activityoccurrence oo 
                                                on oo.id = pp.activity_occurrence_id
                                              where oo.activityid = %s and
                                                pp.prestation_date = p.prestation_date and
                                                pp.prestation_time <= %s and
                                                p.childid = pp.childid        
                                            )
                                        ) zz
                                        where (zz.prestation_time >= %s and zz.prestation_time <= %s) or
                                            (zz.prestation_time <= %s and es = 'E')
                                    ) qq
                                    group by activityid, placeid, prestation_date
                                """
                if activity.prest_from + (period+1)*period_range > activity.prest_to:
                    prest_to = activity.prest_to
                else:
                    prest_to = activity.prest_from + (period+1)*period_range
                    
                period_str = "%s - %s" % (last_period, prest_to)
                print insert_querry % (activity.id,period_str,activity.id,prest_to,activity.id,prest_to,last_period,prest_to,last_period)
                self.env.cr.execute(insert_querry,(activity.id,period_str,activity.id,prest_to,activity.id,prest_to,last_period,prest_to,last_period))
                last_period = prest_to
                #print "%s - %s" % (activity.name, period)
                self.env.invalidate_all()
            