# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
#    Jenny Pans - Imio (<http://www.imio.be>).
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

from openerp import models, api, fields, _


class extraschool_structured_communication(models.Model):
    _name = "extraschool.structured_communication"
    _description = "Structured communication"

    parent_id = fields.Many2one("extraschool.parent", string="Parent", readonly=True)
    digits = fields.Char(size=12, readonly=True)
    formatted = fields.Char(compute="_compute_formatted", string="Structured communication")
    activity_category_id = fields.Many2one("extraschool.activitycategory", string="Activity category", required=True, readonly=True)

    @staticmethod
    def format(structured_communication):
        if len(structured_communication) != 12:
            raise Warning(_("Wrong structured communication (not 12 digits)"))
        return "+++{}/{}/{}+++".format(structured_communication[0:3],
                                       structured_communication[3:7],
                                       structured_communication[7:12])

    @api.multi
    def _compute_formatted(self):
        for rec in self:
            rec.formatted = self.format(rec.digits)

    def get_prefix(self):
        return self.digits[0:3]
