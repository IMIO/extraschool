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

class extraschool_timecorrection_wizard(models.TransientModel):
    _name = 'extraschool.timecorrection_wizard'

    placeid = fields.Many2many(comodel_name='extraschool.place',
                               relation='extraschool_timecorrection_wizard_place_rel',
                               column1='prestationscheck_wizard_id',
                               column2='place_id')
    datefrom = fields.Date('Date from', required=True)
    dateto = fields.Date('Date to', required=True)
    correctiontype = fields.Selection((('add','Add'), ('remove','Remove')),'Correction type', required=True )
    correctiontime = fields.Float('Time', required=True)        
    state = fields.Selection([('init', 'Init'),
                              ('compute_correction', 'Compute correction')],
                              'State', required=True,default='init'
    )

    def action_compute_correction(self):
        prestation_obj = self.env['extraschool.prestationtimes']
        pdaprestation_obj = self.env['extraschool.pdaprestationtimes']
        for placeid in self.placeid:
            prestationspda = pdaprestation_obj.search([('placeid', '=', placeid.id),
                                      ('prestation_date', '>=', self.datefrom),
                                      ('prestation_date', '<=', self.dateto)])
            for prestationpda in prestationspda:                
                if self.correctiontype == 'add':
                    prestationpda.prestation_time = prestationpda.prestation_time + self.correctiontime
                elif self.correctiontype == 'remove':
                    prestationpda.prestation_time = prestationpda.prestation_time - self.correctiontime
                #to do vérifier que ce qui est en dessous est compatible avec le nouveau process de check
#                 cr.execute('select * from "extraschool_prestationtimes"  where childid=%s and "es"=%s and placeid=%s and "prestation_date"=%s and "prestation_time" between %s and %s', (prestationpda['childid'],prestationpda['ES'],prestationpda['placeid'],prestationpda['prestation_date'],prestationpda['prestation_time']-0.0000000001,prestationpda['prestation_time']+0.0000000001))
#                 prestations = cr.dictfetchall()
#                 for prestation in prestations:
#                     if form['correctiontype'] == 'add':
#                         prestation_obj.write(cr,uid,[prestation['id']],{'prestation_time':prestation['prestation_time']+form['correctiontime']})
#                     elif form['correctiontype'] == 'remove':
#                         prestation_obj.write(cr,uid,[prestation['id']],{'prestation_time':prestation['prestation_time']-form['correctiontime']})
            

