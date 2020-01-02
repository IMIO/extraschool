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
from odoo.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
import datetime
from odoo.exceptions import Warning


class extraschool_prestation_times_encodage_manuel(models.Model):
    _name = 'extraschool.prestation_times_encodage_manuel'
    _inherit = 'mail.thread'

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []

        res=[]
        for presta in self.browse(cr, uid, ids,context=context):
            res.append((presta.id, presta.place_id.name + ' - ' + datetime.datetime.strptime(presta.date_of_the_day, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y")  ))

        return res

    date_of_the_day = fields.Date(required=True, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    place_id = fields.Many2one('extraschool.place', required=True, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    levelid = fields.Many2one('extraschool.level', 'Level', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]},)
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=False, track_visibility='onchange')
    prestationtime_ids = fields.One2many('extraschool.prestation_times_manuel','prestation_times_encodage_manuel_id',copy=True, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    comment = fields.Text(track_visibility='onchange')
    prestation_time_all_entry = fields.Float('Entry Time for all')
    prestation_time_all_exit = fields.Float('Exit Time for all')
    schoolimplantation = fields.Many2one('extraschool.schoolimplantation', 'School implantation',
                                         track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'),
                              ('validated', 'Validated')],
                              'State', required=True, default='draft', track_visibility='onchange'
                              )
    warning_biller = fields.Char('WARNING', default="WARNING, Il y a un facturier à cette date. ", readonly=True)
    warning_visibility = fields.Boolean(track_visibility='onchange')

    @api.multi
    def unlink(self):
        if self.state == 'validated':
            raise Warning(_("You cannot remove this subscription because it is not draft"))

        res = super(extraschool_prestation_times_encodage_manuel, self).unlink()
        return res

    @api.onchange('prestation_time_all_entry','prestation_time_all_exit')
    @api.one
    def onchange_hours(self):
        for prestation in self.prestationtime_ids:
            prestation.prestation_time_entry = self.prestation_time_all_entry
            prestation.prestation_time_exit = self.prestation_time_all_exit


    @api.onchange('date_of_the_day')
    @api.multi
    def check_date(self):
        if self.env['extraschool.biller'].search([('period_to', '>=', self.date_of_the_day)]):
            self.warning_visibility = True
        else:
            self.warning_visibility = False

    @api.one
    def update_child_list(self):
        if self.levelid:
            list_level = []
            for level in self.levelid:
                list_level.append(level.id)

            childs = self.env['extraschool.child'].search(
                [('schoolimplantation.id', '=', self.schoolimplantation.id),
                 ('levelid.id', 'in', list_level),
                 ('isdisabled', '=', False),
                 ])
        else:
            if self.schoolimplantation :
                childs = self.env['extraschool.child'].search(
                    [('schoolimplantation.id', '=', self.schoolimplantation.id),
                     ('isdisabled', '=', False),
                     ])
            else :
                raise Warning('Il faut choisir au moins une implantation scolaire')
        self.prestationtime_ids.unlink()
        # clear child list
        self.prestationtime_ids = [(5, 0, 0)]
        child_reg = []

        for child in childs:
            child_reg.append((0, 0, {'child_id': child,
                                     }))
        self.prestationtime_ids = child_reg

    @api.one
    def validate(self):
        if self.env.context == None:
            self.env.context = {}

        presta_obj = self.env['extraschool.pdaprestationtimes']

        if self.state == 'draft' or self.env.user.id == 1:
            pod_allready_reseted_ids = []
            for presta in self.prestationtime_ids:
                if presta.prestation_time_entry > 0:
                    new_presate = presta_obj.create({'activitycategoryid': self.activity_category_id.id,
                                       'placeid': self.place_id.id,
                                       'childid': presta.child_id.id,
                                       'prestation_date': self.date_of_the_day,
                                       'prestation_time': presta.prestation_time_entry,
                                       'type': 'manuel',
                                       'prestation_times_encodage_manuel_id': self.id,
                                       'es': 'E'})
                    if new_presate.prestation_times_of_the_day_id.id not in pod_allready_reseted_ids:
                        pod_allready_reseted_ids.append(new_presate.prestation_times_of_the_day_id.id)
                        new_presate.prestation_times_of_the_day_id.reset()
                        new_presate.prestation_times_of_the_day_id.checked = False
                        new_presate.prestation_times_of_the_day_id.check()

                if presta.prestation_time_exit > 0:
                    new_presate = presta_obj.create({'activitycategoryid': self.activity_category_id.id,
                                       'placeid': self.place_id.id,
                                       'childid': presta.child_id.id,
                                       'prestation_date': self.date_of_the_day,
                                       'prestation_time': presta.prestation_time_exit,
                                       'type': 'manuel',
                                       'prestation_times_encodage_manuel_id': self.id,
                                       'es': 'S'})
                    if new_presate.prestation_times_of_the_day_id.id not in pod_allready_reseted_ids:
                        pod_allready_reseted_ids.append(new_presate.prestation_times_of_the_day_id.id)
                        new_presate.prestation_times_of_the_day_id.reset()
                        new_presate.prestation_times_of_the_day_id.checked = False
                        new_presate.prestation_times_of_the_day_id.check()

        if self.state == 'draft':
            self.state = 'validated'

    @api.multi
    def set_to_draft(self):
        """
        A manual registration implies lots of things. Going back implies also a lot of things.
        We need to remove the pda prestation, reset, check and if needed remove the prestation times of the day
        :return:
        """
        if self.state == 'validated':
            # Get all pdaprestationtimes
            pda_prestation_ids = self.env['extraschool.pdaprestationtimes'].search([('prestation_times_encodage_manuel_id', '=', self.id)])

            ptotd_list = []

            # First part is to unlink all pda_prestation.
            for pda_prestation_id in pda_prestation_ids:
                # Lets' get the prestation times of the day
                prestation_time_of_the_day = pda_prestation_id.prestation_times_of_the_day_id

                if not prestation_time_of_the_day in ptotd_list:
                    ptotd_list.append(prestation_time_of_the_day)

                pda_prestation_id.unlink()

            # Second reset and unlink if need be prestation time of the day.
            for ptotd in ptotd_list:
                # Reset will solve problems but most importantly, it will tell us if we need to remove ptotd
                ptotd.reset()

                if not ptotd.pda_prestationtime_ids and not ptotd.prestationtime_ids:
                    ptotd.unlink()
                else:
                    ptotd.check()

        self.state = 'draft'
