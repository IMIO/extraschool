# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia & Jenny Pans - Imio (<http://www.imio.be>).
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


import datetime
import logging

import pytz

from openerp import models, api, fields, _
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT)

_logger = logging.getLogger(__name__)


class extraschool_prestationscheck_wizard(models.TransientModel):
    _name = 'extraschool.prestationscheck_wizard'

    def _get_defaultfrom(self):
        # look for first oldest prest NOT verified
        prestationtimes_rs = self.env['extraschool.prestationtimes'].search([('verified', '=', False)],
                                                                            order='prestation_date ASC', limit=1)

        if prestationtimes_rs:  # If a presta not verified exist
            fromdate = datetime.datetime.strptime(prestationtimes_rs[0].prestation_date, DEFAULT_SERVER_DATE_FORMAT)
            user_time_zone = self.env.context.get('tz', False)  # self.env.user.tz si ca ne fct pas !!!
            local = pytz.timezone(user_time_zone)
            fromdate = local.localize(fromdate, is_dst=False)
            return fromdate.strftime("%Y-%m-%d")
        else:
            date_now = datetime.datetime.now()
            return str(datetime.date(date_now.year, date_now.month, 1))

    def _get_defaultto(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    period_from = fields.Date(default=_get_defaultfrom)
    period_to = fields.Date(default=_get_defaultto)
    activitycategory = fields.Many2one(comodel_name='extraschool.activitycategory')
    force = fields.Boolean(string="Force verification")
    state = fields.Selection([('init', 'Init'),
                              ('prestations_to_verify', 'Prestations to verify'),
                              ('end_of_verification', 'End of verification')],
                             'State', default='init', required=True)

    def get_prestation_activityid(self, prestation):
        return_val = {'return_code': 0,
                      'error_msg': 'Unknown Error',
                      'occurrence_id': -1}

        obj_activity_occurrence = self.env['extraschool.activityoccurrence']

        #
        # on devrait commencer par les presta avec registration ... voir plus loin c'est mal pris encompte
        #
        # voir si il ne fut pas ajouter le critère de selection en fonction de l'entree par defaut
        # si entree  on cherche les activité avec sortie par defaut ou forfaitaire
        #

        if prestation.es == 'E':
            # get occurrence of the presta day matching the time slot
            occurrence_rs = obj_activity_occurrence.search([('place_id', '=', prestation.placeid.id),
                                                            ('occurrence_date', '=', prestation.prestation_date),
                                                            ('activityid.prest_from', '<=', prestation.prestation_time),
                                                            ('activityid.prest_to', '>', prestation.prestation_time),
                                                            ('activityid.leveltype', 'like',
                                                             prestation.childid.levelid.leveltype)
                                                            ])
        else:
            # get occurrence of the presta day matching the time slot
            occurrence_rs = obj_activity_occurrence.search([('place_id', '=', prestation.placeid.id),
                                                            ('occurrence_date', '=', prestation.prestation_date),
                                                            ('activityid.prest_from', '<', prestation.prestation_time),
                                                            ('activityid.prest_to', '>=', prestation.prestation_time),
                                                            ('activityid.leveltype', 'like',
                                                             prestation.childid.levelid.leveltype)
                                                            ])

        if not occurrence_rs:
            return_val['error_msg'] = _("No matching occurrence found")
            return return_val

        occu_reg = occurrence_rs.filtered(
            lambda r: prestation.childid.id in [reg.child_id.id for reg in r.child_registration_ids])

        if occu_reg:
            return_val['return_code'] = 1
            return_val['occurrence_id'] = occu_reg[0].id
            return return_val

        # filter occurence to remove occurence with registration if "only registered"
        occurrence_no_register_rs = occurrence_rs.filtered(lambda r: not r.activityid.onlyregisteredchilds)

        # try to find a leaf matching the time slot !!! We should use occurrence__child_ids
        occurrence_leaf_rs = occurrence_no_register_rs.filtered(lambda r: not r.activityid.activity_child_ids)

        if len(occurrence_leaf_rs) > 1:  # Error more than 1 leaf occurrence found
            return_val['error_msg'] = "Plusieurs activités trouvées"
            return return_val

        if occurrence_leaf_rs:  # One occurrence found
            return_val['return_code'] = 1
            return_val['occurrence_id'] = occurrence_leaf_rs[0].id
            return return_val

        # try to find a branch matching the time slot
        occurrence_branch_rs = occurrence_no_register_rs.filtered(lambda r: r.activityid.activity_child_ids)

        if len(occurrence_branch_rs) > 1:  # Error more than 1 obranch ccurrence found
            return_val['error_msg'] = "Plusieurs activités trouvées"
            return return_val

        if occurrence_branch_rs:  # One occurrence found
            return_val['return_code'] = 1
            return_val['occurrence_id'] = occurrence_branch_rs[0].id
            return return_val

        return return_val

    def _prestation_activity_occurrence_completion(self, prestation):
        # Look for activityoccurrence maching the prestation
        res = self.get_prestation_activityid(prestation)

        if not res['return_code']:
            prestation.error_msg = res['error_msg']
        else:
            prestation.activity_occurrence_id = res['occurrence_id']

        return self

    @api.multi
    def _check(self, force=False):
        _logger.info("# Check prestations from wizards")

        if not force:
            prestation_search_domain = [('verified', '=', False), ]
        else:
            prestation_search_domain = []

        if self.activitycategory:
            prestation_search_domain.append(('activity_category_id.id', '=', self.activitycategory[0].id))
        if self.period_from:
            prestation_search_domain.append(('prestation_date', '>=', self.period_from))
        if self.period_to:
            prestation_search_domain.append(('prestation_date', '<=', self.period_to))

        obj_prestation_rs = self.env['extraschool.prestationtimes'].search(prestation_search_domain)

        prestation_ids = obj_prestation_rs.ids

        # add activity occurrence when missing
        for prestation in obj_prestation_rs.filtered(lambda r: not r.activity_occurrence_id):
            self._prestation_activity_occurrence_completion(prestation)

        # get distinc presta of the day
        obj_prestation_of_the_day_rs = self.env['extraschool.prestation_times_of_the_day'].search(
            [('prestationtime_ids', 'in', prestation_ids)])

        if force:
            obj_prestation_rs.write({'verified': False, })
            obj_prestation_of_the_day_rs.write({'verified': False, })

        total_check = len(obj_prestation_of_the_day_rs)
        _logger.info("## Total prestations to check: %s" % total_check)
        count_check = 1

        for presta_of_the_day in obj_prestation_of_the_day_rs:
            presta_of_the_day.check()
            _logger.info("### Check [%s/%s]" % (count_check, total_check))
            count_check += 1

            if len(presta_of_the_day.prestationtime_ids.filtered(lambda r: r.verified == False)) > 0:
                presta_of_the_day.verified = False
            else:
                # check duplicate ... sequence must be E S E S E S
                if len(presta_of_the_day.prestationtime_ids) % 2 == 0:
                    presta_of_the_day.verified = True
                else:
                    presta_of_the_day.verified = False

            self.env.cr.commit()

        self.state = 'end_of_verification'

        # construct domain for redirect user to unverified presta matching his selection
        prestation_search_domain = []
        if self.activitycategory:
            prestation_search_domain.append(('activity_category_id.id', '=', self.activitycategory[0].id))
        if self.period_from:
            prestation_search_domain.append(('date_of_the_day', '>=', self.period_from))
        if self.period_to:
            prestation_search_domain.append(('date_of_the_day', '<=', self.period_to))

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'extraschool.prestation_times_of_the_day',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'nodestroy': 'current',
            'domain': prestation_search_domain,
            'context': {'search_default_not_verified': 1}
        }

    @api.multi
    def action_prestationscheck(self):
        self.env['extraschool.prestation_times_of_the_day'].merge_duplicate_pod()
        return self._check(self.force)

    @api.multi
    def action_verified_without_occurrence(self, check=False):
        prestation_ids = self.env['extraschool.prestation_times_of_the_day'].search(
            [('date_of_the_day', '>=', self.period_from), ('date_of_the_day', '<=', self.period_to),
             ('verified', '=', True)])

        list_prestation_times = set()

        for prestation in prestation_ids:
            for prestation_times in prestation.prestationtime_ids:
                if not prestation_times.activity_occurrence_id:
                    list_prestation_times.add(prestation.id)

        if check:
            for prestation in list_prestation_times:
                self.env['extraschool.prestation_times_of_the_day'].browse(prestation).check()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'extraschool.prestation_times_of_the_day',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', list(list_prestation_times))],
            'nodestroy': 'current',
        }

    @api.multi
    def action_verified_without_occurrence_check(self):
        self.action_verified_without_occurrence(True)

    @api.model
    def refactor(self):
        prestation_ids = self.env['extraschool.prestation_times_of_the_day'].search([('verified', '=', False)])

        for prestation_id in prestation_ids:
            presta_ids = self.env['extraschool.prestationtimes'].search(
                [('prestation_times_of_the_day_id', '=', prestation_id.id)]).sorted(key=lambda r: r.prestation_time)
            time = 0.0
            for presta_id in presta_ids:
                if time == presta_id.prestation_time:
                    presta_id.unlink()
                else:
                    time = presta_id.prestation_time