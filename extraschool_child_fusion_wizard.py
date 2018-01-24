# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia - Imio (<http://www.imio.be>).
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


class extraschool_child_fusion_wizard(models.TransientModel):
    _name = 'extraschool.child_fusion_wizard'
    _description = 'Child fusion wizard'

    child_id = fields.Many2one('extraschool.child', 'Child')
    child_ids = fields.Many2many('extraschool.child', 'extraschool_child_fusion_rel', 'child_fusion_id',
                                  'child_id', 'Child_fusion')

    @api.multi
    def fusion(self):
        print "# Let the fusion begins........"
        for child in self.child_ids:
            self.env['extraschool.pdaprestationtimes'].search([('childid', '=', child.id)]).write(
                {'childid': self.child_id.id})
            self.env['extraschool.prestationtimes'].search([('childid', '=', child.id)]).write(
                {'childid': self.child_id.id})
            self.env['extraschool.child_registration_line'].search([('child_id', '=', child.id)]).write(
                {'child_id': self.child_id.id})
            self.env['extraschool.invoicedprestations'].search([('childid', '=', child.id)]).write(
                {'childid': self.child_id.id})
            self.env['extraschool.prestation_times_of_the_day'].search(
                [('child_id', '=', child.id)]).write({'child_id': self.child_id.id})
            self.env['extraschool.prestation_times_manuel'].search([('child_id', '=', child.id)]).write(
                {'child_id': self.child_id.id})
            self.env['extraschool.taxcertificate_item'].search([('child_id', '=', child.id)]).write(
                {'child_id': self.child_id.id})

        # delete child
        child_to_delete_ids = self.env['extraschool.child'].search(
            [('id', 'in', [child.id for child in self.child_ids])])

        if len(child_to_delete_ids):
            print "## Deleting childs."
            sql_delete_child = """delete from extraschool_child
                                  where id in (""" + ','.join(map(str, child_to_delete_ids.ids)) + """)                             
                                """
            self.env.cr.execute(sql_delete_child)

# class extraschool_parent_fusion_child(models.TransientModel):
#     _name = 'extraschool.parent_fusion_child'
#     _description = 'Parent fusion child'
#
#     parent_fusion_wizard_id = fields.Many2one('extraschool.parent_fusion_wizard', 'Parent fusion wizard')
#     fusion_wizard_parent_id = fields.Many2one('extraschool.parent')
#     child_id = fields.Many2one('extraschool.child', 'Child')
#
#     dest_child_id = fields.Many2one('extraschool.child', 'Destination child',
#                                     domain="[('parentid','=',fusion_wizard_parent_id)]")

