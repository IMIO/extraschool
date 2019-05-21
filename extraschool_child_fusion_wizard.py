# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
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

        # Delete POTD with the same prestation date.
        self.delete_potd(self.child_id.id)


        # List of childs to delete.
        child_to_delete_ids = self.env['extraschool.child'].search(
            [('id', 'in', [child.id for child in self.child_ids])])

        # Delete childs
        if len(child_to_delete_ids):
            print "## Deleting childs."
            sql_delete_child = """delete from extraschool_child
                                  where id in (""" + ','.join(map(str, child_to_delete_ids.ids)) + """)                             
                                """
            self.env.cr.execute(sql_delete_child)

    @api.multi
    def delete_potd(self, child_id):
        """
        Fusion and delete potd with the same date.
        :param child_id: id of the child to keep
        :return: None
        """
        previous_date = '0-0-0000'
        self.last_potd_id = 0
        potd_to_delete = []
        for potd in self.env['extraschool.prestation_times_of_the_day'].search(
                [('child_id', '=', child_id)]).filtered('date_of_the_day'):
            if potd.date_of_the_day == previous_date:
                self.fusion_potd(potd.id, potd.date_of_the_day, child_id)
                potd_to_delete.append(self.last_potd_id)
                self.last_potd_id = 0
            previous_date = potd.date_of_the_day
            self.last_potd_id = potd.id

        # Delete empty potd.
        if potd_to_delete:
            self.env['extraschool.prestation_times_of_the_day'].search(
                [('id', '=', potd_to_delete)]).unlink()

    @api.multi
    def fusion_potd(self,potd_id, date_of_the_day, child_id):
        """
        Fusion of potd with the same child id and prestation date.
        :param potd_id: New id of POTD
        :param date_of_the_day: date used for the domain
        :param child_id: id used for the domain
        :return: None
        """
        self.env['extraschool.prestationtimes'].search([('childid', '=', child_id), ('prestation_date', '=', date_of_the_day)]).write(
            {'prestation_times_of_the_day_id': potd_id})
        self.env['extraschool.pdaprestationtimes'].search([('childid', '=', child_id), ('prestation_date', '=', date_of_the_day)]).write(
            {'prestation_times_of_the_day_id': potd_id})
