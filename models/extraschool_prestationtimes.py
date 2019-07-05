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
from odoo.api import Environment
from odoo.exceptions import except_orm, Warning, RedirectWarning
import logging

_logger = logging.getLogger(__name__)


class extraschool_prestationtimes(models.Model):
    _name = 'extraschool.prestationtimes'
    _description = 'Prestation Times'
    _order = 'prestation_date,prestation_time,activity_occurrence_id,es'
    _order = 'prestation_date desc'

    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place', required=False, Index=True)
    childid = fields.Many2one('extraschool.child', 'Child', domain="[('isdisabled','=',False)]", required=False, select=True, ondelete='restrict')
    parent_id = fields.Many2one(related='childid.parentid', store=True, select=True)
    prestation_date = fields.Date('Date', select=True, Index=True)
    prestation_time = fields.Float('Time', select=True, Index=True, required=True)
    es = fields.Selection((('E','In'), ('S','Out')),'es' , select=True)
    exit_all = fields.Boolean('Exit all',default=False)
    manualy_encoded = fields.Boolean('Manualy encoded', readonly=True)
    verified = fields.Boolean('Verified',default=False, select=True)
    error_msg = fields.Char('Error', size=255)
    activity_occurrence_id = fields.Many2one('extraschool.activityoccurrence', 'Activity occurrence', select=True)
    activity_name = fields.Char(related='activity_occurrence_id.activityname')
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=True, select=True)
    prestation_times_of_the_day_id = fields.Many2one('extraschool.prestation_times_of_the_day', 'Prestation of the day',ondelete='restrict')
    invoiced_prestation_id = fields.Many2one('extraschool.invoicedprestations', string='Invoiced prestation', Index="True")

    @api.model
    def create(self, vals):
        if (not vals['childid']) or (not vals['placeid']):
            _logger.error(vals)
            raise Warning('Create Prestation time - Child and Place must be filled')

        prestation_times_of_the_day_obj = self.env['extraschool.prestation_times_of_the_day']
        prestation_times_obj = self.env['extraschool.prestationtimes']


        prestaion_times_ids = prestation_times_obj.search([('placeid.id', '=',vals['placeid']),
                                                                 ('childid.id', '=',vals['childid']),
                                                                 ('prestation_date', '=',vals['prestation_date']),
                                                                 ('prestation_time', '=',vals['prestation_time']),
                                                                 ('es', '=',vals['es']),
                                                                 ])

        if not 'prestation_times_of_the_day_id' in vals:
            prestation_times_of_the_day_ids = prestation_times_of_the_day_obj.search([
                # ('activity_category_id.id', '=', vals['activity_category_id']),
                                                                                      ('child_id.id', '=', vals['childid']),
                                                                                      ('date_of_the_day', '=', vals['prestation_date']),
                                                                                    ])
            if not prestation_times_of_the_day_ids:
                vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_obj.create({
                    # 'activity_category_id' : vals['activity_category_id'],
                                                                                                 'child_id' : vals['childid'],
                                                                                                 'date_of_the_day' : vals['prestation_date'],
                                                                                                 'verified' : False,
                                                               }).id
            else :
                vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_ids.id

        if prestaion_times_ids: #if same presta exist than update
            if 'exit_all' in vals :
                if vals['exit_all'] == False:
                    if prestaion_times_ids.exit_all:
                        vals['exit_all'] = True
            prestaion_times_ids.write(vals)
            return prestaion_times_ids
        else:
            return super(extraschool_prestationtimes, self).create(vals)

    @api.multi
    def write(self, vals):
        return super(extraschool_prestationtimes, self).write(vals)

    @api.multi
    def unlink(self, backdoor=False):
        if backdoor:
            logging.info("Unlink in progress...")
            super(extraschool_prestationtimes, self).unlink()
        else:
            if len(self.filtered(lambda r: r.invoiced_prestation_id.id is not False).ids):
                raise Warning(_("It's not allowed to delete invoiced presta !!!"))

            seen = set()
            seen_add = seen.add
            pod_ids = [presta.prestation_times_of_the_day_id for presta in self if not (presta.prestation_times_of_the_day_id in seen or seen_add(presta.prestation_times_of_the_day_id))]

            for pod in pod_ids:
                pod.prestationtime_ids.write({'verified':False})

            return super(extraschool_prestationtimes, self).unlink()

    @api.multi
    def invert_es(self):
        if not self.invoiced_prestation_id:
            if self.es == 'E':
                self.es = 'S'
            else:
                self.es = 'E'



