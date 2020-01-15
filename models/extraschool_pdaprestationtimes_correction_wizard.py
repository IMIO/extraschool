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

from odoo import models, api, fields, _


class extraschool_pdaprestationtimes_correction_wizard(models.TransientModel):
    _name = 'extraschool.pdaprestationtimes_correction_wizard'
    _description = 'pda prestation wizard'

    es = fields.Selection((('E','In'), ('S','Out')),'es' , index=True)
    prestation_time = fields.Float('Time', index=True, required=True)

    @api.multi
    def correction(self):
        if len(self._context.get('active_ids')):
            self.env['extraschool.pdaprestationtimes'].search([('id', 'in',self._context.get('active_ids'))]).write({'es': self.es,
                                                              'prestation_time': self.prestation_time})
            for presta in self.env['extraschool.pdaprestationtimes'].search([('id', 'in',self._context.get('active_ids'))]):
                presta.prestation_times_of_the_day_id.reset()
                presta.prestation_times_of_the_day_id.check()

        return True




