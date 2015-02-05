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
from openerp import models,api


class extraschool_prestations_wizard(osv.osv_memory):
    _name = 'extraschool.prestations_wizard'

    def _get_prestations(self, cr, uid, ids, field_names, arg=None, context=None):
        obj_prestations = self.pool.get('extraschool.prestationtimes')
        wiz_obj = self.browse(cr, uid, ids)[0]
        prestations_ids=obj_prestations.search(cr, uid, [('childid', '=', wiz_obj.childid.id),('prestation_date', '=', wiz_obj.prestation_date)], order='prestation_time')        
        result = {ids[0]:prestations_ids, 'nodestroy': True}
        return result

    def _get_schoolimplantations(self, cr, uid, ids, field_names, arg=None, context=None):
        obj_place = self.pool.get('extraschool.place')
        wiz_obj = self.browse(cr, uid, ids)[0]
        schoolimplantationids=obj_place.read(cr, uid, [wiz_obj.placeid.id],['schoolimplantation_ids'])[0]
        return {ids[0]:schoolimplantationids['schoolimplantation_ids'], 'nodestroy': True}

    def _set_prestations(self, cr, uid, ids, field_names, value, arg=None, context=None):
        return True
        
    def _get_defaultcategory(cr, uid, ids, context=None):
        return 1 # to modify
    
    _columns = {
        'childid' : fields.many2one('extraschool.child', 'Child', domain="[('isdisabled','=',False)]", required=True),
        'schoolimplantationids': fields.function(fnct=_get_schoolimplantations, method=True, type='char', relation='extraschool.schoolimplantation', string='Schoolimplantaions'), 
        'placeid' : fields.many2one('extraschool.place', 'Schoolcare Place', required=True),
        'activitycategory' : fields.many2one('extraschool.activitycategory', 'Activity category'),
        'prestation_date' : fields.date('Prestation Date'),
        'prestation_time' : fields.char('Time', size=5),
        'es' : fields.selection((('E','In'), ('S','Out')),'ES' ),
        'prestations_id': fields.function(fnct=_get_prestations,fnct_inv=_set_prestations, method=True, type='one2many', relation='extraschool.prestationtimes', string='Prestations'), 
    }
    _defaults = {
        'activitycategory' : _get_defaultcategory,
        'schoolimplantationids' : [1],
    }
    
    @api.onchange('placeid')
    def onchange_placeid(self):
        if self.placeid:
            schoolimplantationids=self.env['extraschool.place'].browse(self.placeid.id)           
            return {'domain':{'childid': [('schoolimplantation', 'in', [impl.id for impl in schoolimplantationids.schoolimplantation_ids])]},}
        
    @api.onchange('prestations_id','childid','placeid')
    def onchange_prestations(self):

        cr,uid = self.env.cr,self.env.user.id
        for prestation in self.prestations_id:
            if prestation.exists():
                prestation.write()
            else:
                prestation.create()
        
    def onchange_childid(self, cr, uid, ids, childid,prestation_date):
        obj_child = self.pool.get('extraschool.child')
        obj_prestations = self.pool.get('extraschool.prestationtimes')
        v={}                
        if childid:
            #v['schoolimplantationid']=obj_child.read(cr, uid, [childid],['schoolimplantation'])[0]['schoolimplantation'][0]
            prestations_ids=obj_prestations.search(cr, uid, [('childid', '=', childid),('prestation_date', '=', prestation_date)])
            v['prestations_id']=prestations_ids
        return {'value':v}
   
    def onchange_prestation_date(self, cr, uid, ids, prestation_date,childid):
        obj_prestations = self.pool.get('extraschool.prestationtimes')
        v={}        
        prestations_ids=obj_prestations.search(cr, uid, [('childid', '=', childid),('prestation_date', '=', prestation_date)])
        v['prestations_id']=prestations_ids
        return {'value':v}

    def onchange_placeid(self, cr, uid, ids, placeid):
        if placeid:
            obj_place = self.pool.get('extraschool.place')
            v={}        
            schoolimplantationids=obj_place.read(cr, uid, [placeid],['schoolimplantation_ids'])            
            return {'domain':{'childid': [('schoolimplantation', 'in', schoolimplantationids[0]['schoolimplantation_ids'])]},}
        
    def action_save_prestation(self, cr, uid, ids, context=None):     
        obj_prestation = self.pool.get('extraschool.prestationtimes')           
        form = self.read(cr,uid,ids,)[-1]
        if form['es'] and form['prestation_time'] and form['prestation_date'] and form['childid'] and form['placeid']:
            prestation_time=form['prestation_time']
            prestation_id = obj_prestation.create(cr, uid, {'placeid':form['placeid'][0],'childid':form['childid'][0],'activitycategoryid':form['activitycategory'][0],'prestation_date':form['prestation_date'],'prestation_time':prestation_time,'ES':form['es'],'manualy_encoded':True}, context=context)           
            return self.write(cr, uid, ids,{'prestation_time' : None,'es':None,}, context=context)
        else:
            return False
extraschool_prestations_wizard()
