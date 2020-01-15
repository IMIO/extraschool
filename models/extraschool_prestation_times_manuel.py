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


class extraschool_prestation_times_manuel(models.Model):
    _name = 'extraschool.prestation_times_manuel'
    _description = 'prestation times manuel'

    child_id = fields.Many2one('extraschool.child', domain="[('isdisabled', '=', False)]", required=True)
    prestation_times_encodage_manuel_id = fields.Many2one('extraschool.prestation_times_encodage_manuel', 'encodage manuel')
    prestation_time_entry = fields.Float('Entry Time')
    prestation_time_exit = fields.Float('Exit Time')
    comment = fields.Text()

    @api.model
    def create(self, vals):
        # Check Validity Date & Hour.
        res = super(extraschool_prestation_times_manuel, self).create(vals)
        if res:
            id_encodage = self.env['extraschool.prestation_times_encodage_manuel'].search(
                [('id', '=', res['prestation_times_encodage_manuel_id'].id)])
            if id_encodage.prestation_time_all_entry:
                res['prestation_time_entry'] = id_encodage.prestation_time_all_entry
            if id_encodage.prestation_time_all_exit:
                res['prestation_time_exit'] = id_encodage.prestation_time_all_exit
        return res

