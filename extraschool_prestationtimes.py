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

class extraschool_prestationtimes(osv.osv):
    _name = 'extraschool.prestationtimes'
    _description = 'Prestation Times'

    def editprestation(self, cr, uid, ids, context=None):     
        view_obj = self.pool.get('ir.ui.view')
        extraschool_prestationtimes_form2 = view_obj.search(cr, uid, [('model', '=', 'extraschool.prestationtimes'), \
                                 ('name', '=', 'prestationtimes.form2')])
        return {
        'type': 'ir.actions.act_window',
        'name': 'View and Edit',
        'view_mode': 'form',
        'view_type': 'form',
        'res_model': 'extraschool.prestationtimes',
        'res_id': ids[0],
        'view_id': extraschool_prestationtimes_form2,
        'context': context,
        'target': 'new',
        'nodestroy': True,
        }

    def deleteprestation(self, cr, uid, ids, context=None): 
        obj_prestation = self.pool.get('extraschool.prestationtimes')
        deletedid = obj_prestation.unlink(cr, uid, ids[0], context=context)
        return True
        
    def saveprestation(self, cr, uid, ids, context=None):
        obj_prestation = self.pool.get('extraschool.prestationtimes')
        form = self.read(cr,uid,ids,)[-1]
        prestation_id = obj_prestation.write(cr, uid, ids[0], {'childid':form['childid'][0],'prestation_date':form['prestation_date'],'prestation_time':form['prestation_time'],'ES':form['ES'],'manualy_encoded':True}, context=context)
        return {'warning': {'title': 'Record saved','message': 'record saved!',}}
   
    def _compute_date_from (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):            
            to_return[record.id]= str(datetime.datetime(int(record.prestation_date[0:4]),int(record.prestation_date[5:7]),int(record.prestation_date[8:10]),int(math.floor(record.prestation_time)),int((record.prestation_time-math.floor(record.prestation_time))*60)))
        return to_return

        
    _columns = {
        'placeid' : fields.many2one('extraschool.place', 'Schoolcare Place', required=False),
        'activitycategoryid' : fields.many2one('extraschool.activitycategory', 'Activity Category', required=False),
        'childid' : fields.many2one('extraschool.child', 'Child', domain="[('isdisabled','=',False)]", required=False, select=True),
        'prestation_date' : fields.date('Date', select=True),
        'prestation_time' : fields.float('Time', select=True, required=True),
        'date_from' : fields.function(_compute_date_from, method=True, type="datetime", string="Date from"),      
        'ES' : fields.selection((('E','In'), ('S','Out')),'ES' , select=True, required=True),   
        'manualy_encoded' : fields.boolean('Manualy encoded', readonly=True),   
        'verified' : fields.boolean('Verified'),
        'activityid' : fields.many2one('extraschool.activity', 'Activity', required=False),        
    }
    
    def create(self, cr, uid, vals, *args, **kw):
        if (not vals['childid']) or (not vals['placeid']) or (not vals['activitycategoryid']):  
            raise osv.except_osv('Child, Place and Category must be filled')
        return super(extraschool_prestationtimes, self).create(cr, uid, vals)

    
    def write(self, cr, uid, ids, vals, context=None):
            vals['verified'] = False
            return super(extraschool_prestationtimes, self).write(cr, uid, ids, vals, context=context)
            
    def unlink(self, cr, uid, ids, context=None):        
        prestationtimes_obj = self.pool.get('extraschool.prestationtimes')  
        thisprest = prestationtimes_obj.read(cr,uid,ids,['prestation_date','childid'])
        if thisprest:
            try:
                prestation_ids=prestationtimes_obj.search(cr, uid, [('childid', '=', thisprest[0]['childid'][0]),('prestation_date', '=', thisprest[0]['prestation_date'])])
                res = prestationtimes_obj.write(cr,uid,prestation_ids,{'verified':False})
            except:
                pass
            return super(extraschool_prestationtimes, self).unlink(cr, uid, ids)
extraschool_prestationtimes()
