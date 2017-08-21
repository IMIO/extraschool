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
import lbutils
from openerp.exceptions import except_orm, Warning, RedirectWarning

class extraschool_parent_fusion_wizard(models.TransientModel):
    _name = 'extraschool.parent_fusion_wizard'
    _description = 'Parent fusion wizard'
    
    parent_id = fields.Many2one('extraschool.parent', 'Parent')
    parent_ids = fields.Many2many('extraschool.parent','extraschool_parent_fusion_rel', 'parent_fusion_id', 'parent_id','Parent_fusion')
    fusion_child_ids = fields.One2many('extraschool.parent_fusion_child', 'parent_fusion_wizard_id','childs')
    comment = fields.Char(default="The parent that will be deleted has one or more unpaid invoices. Make sure the parent knows about it (resend the invoice).", readonly=True)
    show_comment = fields.Boolean(default=False)

    @api.onchange('parent_ids')
    @api.one
    def _on_change_parent_ids(self):
        self.fusion_child_ids = [(5, 0, 0)]
        tmp_childs = []
        for parent in self.parent_ids:
            for child in parent.child_ids:
                tmp_childs.append((0,0,{'parent_fusion_wizard_id': self.id,
                                        'fusion_wizard_parent_id': self.parent_id.id,
                                        'child_id': child.id,}))

            if self.env['extraschool.invoice'].search([('parentid', '=', parent.id)]).filtered('balance'):
                self.show_comment = True
            else:
                self.show_comment = False
        
        self.fusion_child_ids = tmp_childs

    @api.multi
    def fusion(self):
        print "# Let the fusion begins........"
        for child in self.fusion_child_ids:
            #child doesn't exist on parent origin
            if not child.dest_child_id:
                child.child_id.parentid = self.parent_id.id
            #child exist on parent origin
            else:
                self.env['extraschool.pdaprestationtimes'].search([('childid', '=',child.child_id.id)]).write({'childid': child.dest_child_id.id})
                self.env['extraschool.prestationtimes'].search([('childid', '=',child.child_id.id)]).write({'childid': child.dest_child_id.id})
                self.env['extraschool.child_registration_line'].search([('child_id', '=',child.child_id.id)]).write({'child_id': child.dest_child_id.id})
                self.env['extraschool.invoicedprestations'].search([('childid', '=',child.child_id.id)]).write({'childid': child.dest_child_id.id})
                self.env['extraschool.prestation_times_of_the_day'].search([('child_id', '=',child.child_id.id)]).write({'child_id': child.dest_child_id.id})
                self.env['extraschool.prestation_times_manuel'].search([('child_id', '=',child.child_id.id)]).write({'child_id': child.dest_child_id.id})

        #delete child 
        child_to_delete_ids = self.env['extraschool.child'].search([('id', 'in', [r.child_id.id for r in self.fusion_child_ids.filtered(lambda r: r.dest_child_id)])]).ids
        if len(child_to_delete_ids):
            print "## Deleting childs."
            sql_delete_child = """delete from extraschool_child
                                  where id in (""" + ','.join(map(str, child_to_delete_ids))+ """)                             
                                """
            self.env.cr.execute(sql_delete_child)

        for parent in self.parent_ids:
            self.env['extraschool.invoice'].search([('parentid', '=', parent.id)]).write(
                {'parentid': self.parent_id.id})
            self.env['extraschool.payment'].search([('parent_id', '=', parent.id)]).write(
                {'parent_id': self.parent_id.id})
            self.env['extraschool.reminder'].search([('parentid', '=', parent.id)]).write(
                {'parentid': self.parent_id.id})


        if len(self.parent_ids.ids):
            print "## Deleting parents."
            sql_delete_parent = """delete from extraschool_parent
                                   where id in (""" + ','.join(map(str, self.parent_ids.ids))+ """)                             
                                """
            self.env.cr.execute(sql_delete_parent)


class extraschool_parent_fusion_child(models.TransientModel):
    _name = 'extraschool.parent_fusion_child'
    _description = 'Parent fusion child'
    
    parent_fusion_wizard_id = fields.Many2one('extraschool.parent_fusion_wizard', 'Parent fusion wizard')
    fusion_wizard_parent_id = fields.Many2one('extraschool.parent')                  
    child_id = fields.Many2one('extraschool.child', 'Child')
    
    dest_child_id = fields.Many2one('extraschool.child', 'Destination child', domain="[('parentid','=',fusion_wizard_parent_id)]")
    
