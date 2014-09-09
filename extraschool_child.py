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

class extraschool_child(osv.osv):
    _name = 'extraschool.child'
    _description = 'Child'
    def _name_compute(self, cr, uid, ids, fieldname, other, context=None):

        res = dict.fromkeys(ids, '')

        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = str(obj.lastname).encode('utf-8')+' '+str(obj.firstname).encode('utf-8')

        return res
    def onchange_name(self, cr, uid, ids, lastname,firstname):
        v={}        
        if lastname:
            if firstname:
                v['name']='%s %s' % (lastname, firstname)
            else:
                v['name']=lastname
        return {'value':v}
        
    def return_action_to_open(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current child """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'extraschool', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_child_id': ids[0]})
            res['domain'] = [('child_id','=', ids[0])]
            return res
        return False
    
    def action_gentagid(self, cr, uid, ids, context=None):             
        form = self.read(cr,uid,ids,)[-1]
        if not form['tagid']:
            obj_config = self.pool.get('extraschool.mainsettings')
            config=obj_config.read(cr, uid, [1],['lastqrcodenbr'])[0]
            mainsettings_id = obj_config.write(cr, uid, [1], {'lastqrcodenbr':config['lastqrcodenbr']+1}, context=context) 
            return self.write(cr, uid, ids,{'tagid' : config['lastqrcodenbr']+1,}, context=context)
        else:
            return False
    
    _columns = {
        'name' : fields.char('FullName', size=100),
        'childtypeid' : fields.many2one('extraschool.childtype', 'Type',required=True),
        'firstname' : fields.char('FirstName', size=50, required=True),
        'lastname' : fields.char('LastName', size=50 , required=True),
        'schoolimplantation' : fields.many2one('extraschool.schoolimplantation', 'School implantation',required=True),
        'levelid' : fields.many2one('extraschool.level', 'Level', required=True),
        'classid' : fields.many2one('extraschool.class', 'Class', required=False),
        'parentid' : fields.many2one('extraschool.parent', 'Parent', required=True),
        'birthdate' : fields.date('Birthdate', required=True),
        'tagid' : fields.char('Tag ID', size=50),
        'otherref' : fields.char('Other ref', size=50),
        'isdisabled' : fields.boolean('Disabled'),
        'oldid' : fields.integer('oldid'),
        'toto' : fields.char('toto'),                
    }
    
    def create(self, cr, uid, vals, *args, **kw):
        child_obj = self.pool.get('extraschool.child')
        child_ids=child_obj.search(cr, uid, [('firstname', 'ilike', vals['firstname'].strip()),('lastname', 'ilike', vals['lastname'].strip()),('birthdate', '=', vals['birthdate'])])
        if len(child_ids) >0:
            raise osv.except_osv('Erreur','Cet enfant a deja ete encode !!!'+vals['firstname']+' '+vals['lastname'])
        return super(extraschool_child, self).create(cr, uid, vals)

    def test(self, cr, uid, context=None):
        print '***************************************************************'
        print '***************************************************************'
        self.write(cr,uid,[1],{'toto':'tutu',})

    def unlink(self, cr, uid, ids, context=None):
        prestationtimes_obj = self.pool.get('extraschool.prestationtimes')
        prestation_ids=prestationtimes_obj.search(cr, uid, [('childid', '=', ids[0])])
        if len(prestation_ids) >0:
            raise osv.except_osv('Error', 'You can not delete a child with prestations.')
            return False
        return super(extraschool_child, self).unlink(cr, uid, ids)

extraschool_child()

