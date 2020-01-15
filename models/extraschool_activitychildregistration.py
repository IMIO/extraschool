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

from odoo import models, api, fields


class extraschool_activitychildregistration(models.Model):
    _name = 'extraschool.activitychildregistration'
    _description = 'activity child registration'

    child_id = fields.Many2one('extraschool.child', 'Child', required=True)
    place_id = fields.Many2one('extraschool.place', 'Place', required=True)
    activity_id = fields.Many2one('extraschool.activity', 'Activity')
    registration_from = fields.Date('Registration from', required=True)
    registration_to = fields.Date('Registration to', required=True)

    @api.multi
    def name_get(self):
        res=[]
        for reg in self:
            res.append((reg.id, reg.child_id.name + ' - ' + reg.place_id.name))

        return res

extraschool_activitychildregistration()
