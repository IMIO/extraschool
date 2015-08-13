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

    name = fields.Char(compute='_name_compute',string='FullName', size=100)
    childtypeid = fields.Many2one('extraschool.childtype', 'Type',required=True)
    firstname = fields.Char('FirstName', size=50, required=True)
    lastname = fields.Char('LastName', size=50 , required=True)
    schoolimplantation = fields.Many2one('extraschool.schoolimplantation', 'School implantation',required=True)
    levelid = fields.Many2one('extraschool.level', 'Level', required=True)
    classid = fields.Many2one('extraschool.class', 'Class', required=False)
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=True, ondelete='RESTRICT')
    birthdate = fields.Date('Birthdate', required=True)
    tagid = fields.Char('Tag ID', size=50)
    otherref = fields.Char('Other ref', size=50)
    isdisabled = fields.Boolean('Disabled')
    oldid = fields.Integer('oldid')             

    _sql_constraints = [
        ('firstname_name_uniq', 'unique(lastname,firstname)',
            'Name and firstname must be unique !'),
    ]   
     
    @api.depends('firstname','lastname')
    def _name_compute(self):
        for record in self:
            record.name = str(record.lastname).encode('utf-8') + ' ' + str(record.firstname).encode('utf-8')

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

extraschool_child()

