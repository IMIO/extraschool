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
    _order = 'prestation_date,prestation_time,activity_occurrence_id,es'

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
          
    _columns = {
        'placeid' : fields.many2one('extraschool.place', 'Schoolcare Place', required=False),
        'activitycategoryid' : fields.many2one('extraschool.activitycategory', 'Activity Category', required=False),
        'childid' : fields.many2one('extraschool.child', 'Child', domain="[('isdisabled','=',False)]", required=False, select=True),
        'prestation_date' : fields.date('Date', select=True),
        'prestation_time' : fields.float('Time', select=True, required=True),
        'es' : fields.selection((('E','In'), ('S','Out')),'es' , select=True),  
        'exit_all' : fields.boolean('Exit all'),
        'manualy_encoded' : fields.boolean('Manualy encoded', readonly=True),   
        'verified' : fields.boolean('Verified'),
        'activityid' : fields.many2one('extraschool.activity', 'Activity', required=False),  
        'error_msg' : fields.char('Error', size=255),
        'activity_occurrence_id' : fields.many2one('extraschool.activityoccurrence', 'Activity occurrence'),  
        'activity_name' : fields.related('activity_occurrence_id', 'activityname', type='char', string='Activity Name'),
        'prestation_times_of_the_day_id' : fields.many2one('extraschool.prestation_times_of_the_day', 'Prestation of the day'),  
              
    }
    
    _defaults = {
        'exit_all' : lambda *a: False,
        'verified' : lambda *a: False,
    }    
    def create(self, cr, uid, vals, *args, **kw):        
        if (not vals['childid']) or (not vals['placeid']) or (not vals['activitycategoryid']):  
            raise osv.except_osv('Child, Place and Category must be filled')
        
        prestation_times_of_the_day_obj = self.pool.get('extraschool.prestation_times_of_the_day')
        prestation_times_obj = self.pool.get('extraschool.prestationtimes')
        
        #check if presta allready exist
        print "------------------"
        print str(vals)
        print "------------------"
        prestaion_times_ids = prestation_times_obj.search(cr,uid,[('placeid.id', '=',vals['placeid']),
                                                                 ('childid.id', '=',vals['childid']),
                                                                 ('activitycategoryid.id', '=',vals['activitycategoryid']),
                                                                 ('prestation_date', '=',vals['prestation_date']),
                                                                 ('prestation_time', '=',vals['prestation_time']),
                                                                 ('es', '=',vals['es']),
                                                                 ])
            
        
        prestation_times_of_the_day_ids = prestation_times_of_the_day_obj.search(cr,uid,[('child_id.id', '=', vals['childid']),
                                                                                ('date_of_the_day', '=', vals['prestation_date']),
                                                                                ])
        if not prestation_times_of_the_day_ids:
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_obj.create(cr,uid,{'child_id' : vals['childid'],
                                                           'date_of_the_day' : vals['prestation_date'],
                                                           'verified' : False,
                                                           })
        else :
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_ids[0]

        if prestaion_times_ids: #if same presta exist than update
            if 'exit_all' in vals :
                if vals['exit_all'] == False:
                    presta_to_update = prestation_times_obj.browse(cr,uid,prestaion_times_ids[0])
                    if presta_to_update.exit_all:
                        vals['exit_all'] = True
            
            return super(extraschool_prestationtimes, self).write(cr, uid, prestaion_times_ids, vals)
        else:
            return super(extraschool_prestationtimes, self).create(cr, uid, vals)

    
    def write(self, cr, uid, ids, vals, context=None):
#            vals['verified'] = False
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


