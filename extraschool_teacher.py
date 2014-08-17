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

class extraschool_teacher(osv.osv):
    _name = 'extraschool.teacher'
    _description = 'Teacher'

    def onchange_name(self, cr, uid, ids, lastname,firstname):
        v={}        
        if lastname:
            if firstname:
                v['name']='%s %s' % (lastname, firstname)
            else:
                v['name']=lastname
        return {'value':v}

    _columns = {
        'name' : fields.char('Fullname', size=100),
        'firstname' : fields.char('FirstName', size=50, required=True),
        'lastname' : fields.char('LastName', size=50 , required=True),
        'copiercodes' : fields.one2many('extraschool.copiercode', 'teacherid','Copier Codes'),        
        'oldid' : fields.integer('oldid'),
    }
    
    def create(self, cr, uid, vals, *args, **kw):
        teacher_obj = self.pool.get('extraschool.teacher')
        teacher_ids=teacher_obj.search(cr, uid, [('firstname', 'ilike', vals['firstname'].strip()),('lastname', 'ilike', vals['lastname'].strip())])
        if len(teacher_ids) >0:
            raise osv.except_osv('Erreur','Cet enseignant a deja ete encode !!!')
        return super(extraschool_teacher, self).create(cr, uid, vals)

extraschool_teacher()

