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

class extraschool_timecorrection_wizard(osv.osv_memory):
    _name = 'extraschool.timecorrection_wizard'

    def _get_places(self, cr, uid, ids, field_names, arg=None, context=None):
        result = {ids[0]: self._placeids, 'nodestroy': True}
        return result

    def _set_places(self, cr, uid, ids, field_names, value, arg=None, context=None):
        self._placeids=value[0][2]

    _columns = {
        'placeid' : fields.function(fnct=_get_places,fnct_inv=_set_places, method=True, type='many2many', relation='extraschool.place', string='Places'), 
        'datefrom' : fields.date('Date from', required=True),
        'dateto' : fields.date('Date to', required=True),
        'correctiontype' : fields.selection((('add','Add'), ('remove','Remove')),'Correction type', required=True ),
        'correctiontime' : fields.float('Time', required=True),        
        'state' : fields.selection(
            [('init', 'Init'),('compute_correction', 'Compute correction')],
            'State', required=True
        ),
    }

    _defaults = {
        'state' : lambda *a: 'init'
    }

    def action_compute_correction(self, cr, uid, ids, context=None):
        form = self.read(cr,uid,ids,)[-1]
        prestation_obj = self.pool.get('extraschool.prestationtimes')
        pdaprestation_obj = self.pool.get('extraschool.pdaprestationtimes')
        for placeid in self._placeids:
            cr.execute('select * from "extraschool_pdaprestationtimes"  where placeid=%s and "prestation_date">=%s and "prestation_date"<=%s', (placeid,form['datefrom'],form['dateto']))
            prestationspda = cr.dictfetchall()
            for prestationpda in prestationspda:                
                if form['correctiontype'] == 'add':
                    pdaprestation_obj.write(cr,uid,[prestationpda['id']],{'prestation_time':prestationpda['prestation_time']+form['correctiontime']})
                elif form['correctiontype'] == 'remove':
                    pdaprestation_obj.write(cr,uid,[prestationpda['id']],{'prestation_time':prestationpda['prestation_time']-form['correctiontime']})
                cr.execute('select * from "extraschool_prestationtimes"  where childid=%s and "es"=%s and placeid=%s and "prestation_date"=%s and "prestation_time" between %s and %s', (prestationpda['childid'],prestationpda['ES'],prestationpda['placeid'],prestationpda['prestation_date'],prestationpda['prestation_time']-0.0000000001,prestationpda['prestation_time']+0.0000000001))
                prestations = cr.dictfetchall()
                for prestation in prestations:
                    if form['correctiontype'] == 'add':
                        prestation_obj.write(cr,uid,[prestation['id']],{'prestation_time':prestation['prestation_time']+form['correctiontime']})
                    elif form['correctiontype'] == 'remove':
                        prestation_obj.write(cr,uid,[prestation['id']],{'prestation_time':prestation['prestation_time']-form['correctiontime']})
            

