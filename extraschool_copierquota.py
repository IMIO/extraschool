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

class extraschool_copierquota(osv.osv):
    _name = 'extraschool.copierquota'
    _description = 'Copier Quota'
    
    def _compute_quota (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            try:
                cr.execute('select sum(quotaadjustment) from extraschool_quotaadjustment where copierquotaid=%s',(record.id,))
                adjustment=cr.fetchall()[0][0]
                if not adjustment:
                    adjustment=0
            except:
                adjustment=0
            try:
                to_return[record.id] = round(((float(record.nbchilds * 500) / 24) * record.nbperiods) + adjustment)
            except:
                to_return[record.id] = 0

        return to_return
    
    def _compute_remainingcopies (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            try:
                to_return[record.id] = record.totalquota - record.nbcopiesdone
            except:
                to_return[record.id] = 0
        return to_return

    _columns = {
        'copiercodeid' : fields.many2one('extraschool.copiercode', 'Copier Code',required=True,ondelete='cascade'),
        'schoolimplantationid' : fields.many2one('extraschool.schoolimplantation', 'School implantation',required=True),
        'nbperiods' : fields.integer('Number of periods'),
        'nbchilds' : fields.integer('Number of childs'),
        'nbcopiesdone' : fields.integer('Number of Copies done'),
        'quotaadjustments' : fields.one2many('extraschool.quotaadjustment', 'copierquotaid','Quota adjustments'),            
        'totalquota' : fields.function(_compute_quota, method=True, type="integer", string="Total quota"),
        'remainingcopies' : fields.function(_compute_remainingcopies, method=True, type="integer", string="Remaining copies"),
        'oldid' : fields.integer('oldid'),
    }
extraschool_copierquota()
