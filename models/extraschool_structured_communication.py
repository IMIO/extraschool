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
    _description = 'Structured communication'

    def name_get(self):
        res = []
        for digits in self:
            res.append(self.get_formatted())
        return res

    parent_id = fields.Many2one("extraschool.parent", "structured_communications")
    digits = fields.Char(size=12)

    def get_formatted(self):
        return "+++{}/{}/{}+++".format(self[0:3], self[3:7], self[7:12])

    def get_prefix(self):
        return self.digits[0:3]
