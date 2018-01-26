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
from datetime import date, datetime
import time


class extraschool_child(models.Model):
    _name = 'extraschool.child'
    _description = 'Child'
    _inherit = 'mail.thread'

    def _get_activity_category_id(self):
        return self.env['extraschool.activitycategory'].search([]).filtered('id')

    activitycategoryid = fields.Many2one('extraschool.activitycategory', 'Activity Category',
                                         track_visibility='onchange', default=_get_activity_category_id)
    name = fields.Char(compute='_name_compute',string='FullName', search='_search_fullname', size=100)
    childtypeid = fields.Many2one('extraschool.childtype', 'Type',required=True, ondelete='restrict', help='Ce champs permet de définir si l\'enfant a le droit à un tarif préférentiel (ex: enfants du CPAS, enfants de la croix rouge, enfants des accueillantes,...)')
    rn = fields.Char('RN')
    firstname = fields.Char('FirstName', size=50, required=True, track_visibility='onchange')
    lastname = fields.Char('LastName', size=50 , required=True, track_visibility='onchange')
    schoolimplantation = fields.Many2one('extraschool.schoolimplantation', 'School implantation',required=True, track_visibility='onchange')
    levelid = fields.Many2one('extraschool.level', 'Level', required=True, track_visibility='onchange')
    classid = fields.Many2one('extraschool.class', 'Class', required=False, domain="[('schoolimplantation','=',schoolimplantation)]", track_visibility='onchange')
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=True, ondelete='RESTRICT', select=True, track_visibility='onchange')
    birthdate = fields.Date('Birthdate', required=True, track_visibility='onchange')
    last_import_date = fields.Datetime('Import date', readonly=True)
    modified_since_last_import = fields.Boolean('Modified since last import')    
    tagid = fields.Char('Tag ID', help='Numéro contenu dans le QR Code', track_visibility='onchange')
    otherref = fields.Char('Other ref', size=50, track_visibility='onchange')
    isdisabled = fields.Boolean('Disabled', track_visibility='onchange')
    comment = fields.Text('Comment', track_visibility='onchange')

    def get_age(self):
        date_of_birth = datetime.strptime(self.birthdate,'%Y-%m-%d')
        return datetime.today().year - date_of_birth.year - (
        (datetime.today().month, datetime.today().day) < (date_of_birth.month, date_of_birth.day))

    @api.multi
    def wizard_action(self):
        return {
            'name': 'My Window',
            'domain': [],
            'res_model': 'extraschool.child_fusion_wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {},
            'target': 'new',
        }

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
        
        # return long(self.tagid)
        return self.tagid

    @api.multi
    def write(self, vals):
        fields_to_find = set(['firstname',
                              'lastname'])
        
        if fields_to_find.intersection(set([k for k,v in vals.iteritems()])):
            vals['modified_since_last_import'] = True
                    
        return super(extraschool_child,self).write(vals)

    @api.multi
    def get_presta(self): 
 
        return {'name': 'Présences',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.prestation_times_of_the_day',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,     
                'target': 'current',
                'limit': 50000,                                    
                'domain': [('child_id', '=',self.id),]
            }  
                    
    @api.one
    def unlink(self):
        self.isdisabled = True

extraschool_child()

