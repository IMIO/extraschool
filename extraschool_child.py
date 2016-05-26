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
from datetime import date
import datetime


class extraschool_child(models.Model):
    _name = 'extraschool.child'
    _description = 'Child'

    name = fields.Char(compute='_name_compute',string='FullName', search='_search_fullname', size=100)
    childtypeid = fields.Many2one('extraschool.childtype', 'Type',required=True, ondelete='restrict')
    rn = fields.Char('RN')
    firstname = fields.Char('FirstName', size=50, required=True)
    lastname = fields.Char('LastName', size=50 , required=True)
    schoolimplantation = fields.Many2one('extraschool.schoolimplantation', 'School implantation',required=True)
    levelid = fields.Many2one('extraschool.level', 'Level', required=True)
    classid = fields.Many2one('extraschool.class', 'Class', required=False)
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=True, ondelete='RESTRICT', select=True)
    birthdate = fields.Date('Birthdate', required=True)
    last_import_date = fields.Datetime('Import date', readonly=True)
    modified_since_last_import = fields.Boolean('Modified since last import')    
    tagid = fields.Char('Tag ID', size=50)
    otherref = fields.Char('Other ref', size=50)
    isdisabled = fields.Boolean('Disabled')             

    _sql_constraints = [
        ('firstname_name_uniq', 'unique(lastname,firstname)',
            'Name and firstname must be unique !'),
    ]   
    
    def _search_fullname(self, operator, value):
        return ['|',('firstname', operator, value),('lastname', operator, value)]
    
    
    @api.depends('firstname','lastname')
    def _name_compute(self):
        for record in self:
            record.name = '%s %s'  % (record.lastname, record.firstname)        

    def onchange_name(self, cr, uid, ids, lastname,firstname):
        v={}        
        if lastname:
            if firstname:
                v['name']='%s %s' % (lastname, firstname)
            else:
                v['name']=lastname
        return {'value':v}
    
    @api.one    
    def action_gentagid(self):   
        if not self.tagid :
            config = self.env['extraschool.mainsettings'].browse([1])
            self.tagid = config.lastqrcodenbr = config.lastqrcodenbr + 1
        
        return long(self.tagid)
    
    @api.multi
    def write(self, vals):
        fields_to_find = set(['firstname',
                              'lastname'])
        
        if fields_to_find.intersection(set([k for k,v in vals.iteritems()])):
            vals['modified_since_last_import'] = True
                    
        return super(extraschool_child,self).write(vals)
            
    @api.one
    def unlink(self):
        self.isdisabled = True

extraschool_child()

