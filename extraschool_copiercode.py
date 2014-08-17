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

class extraschool_copiercode(osv.osv):
    _name = 'extraschool.copiercode'
    _description = 'Copier Code'

    def _compute_totalremainingcopies (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        copierquota_obj = self.pool.get('extraschool.copierquota')
        for record in self.browse(cr, uid, ids):
            try:
                copierquota_ids=copierquota_obj.search(cr, uid, [('copiercodeid', '=', record.id)])
                copierquotas=copierquota_obj.read(cr,uid,copierquota_ids,['remainingcopies',])
                totalremainingcopies=0
                for copierquota in copierquotas:
                    totalremainingcopies=totalremainingcopies+copierquota['remainingcopies']
                to_return[record.id] = totalremainingcopies
            except:
                to_return[record.id] = 0
        return to_return

    _columns = {
        'name': fields.char('Code', size=7),
        'pin': fields.char('Pin', size=7),
        'teacherid' : fields.many2one('extraschool.teacher', 'Teacher',ondelete='cascade'),
        'copierquotas' : fields.one2many('extraschool.copierquota', 'copiercodeid','Copier Quotas'),        
        'totalremainingcopies' : fields.function(_compute_totalremainingcopies, method=True, type="integer", string="Remaining copies"),
        'oldid' : fields.integer('oldid'),
    }
extraschool_copiercode()

