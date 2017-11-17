# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014 
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot - Imio (<http://www.imio.be>).
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
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
from datetime import date
import datetime


class extraschool_prestation_times_encodage_manuel(models.Model):
    _name = 'extraschool.prestation_times_encodage_manuel'
    _inherit = 'mail.thread'

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        
        res=[]
        for presta in self.browse(cr, uid, ids,context=context):
            res.append((presta.id, presta.place_id.name + ' - ' + datetime.datetime.strptime(presta.date_of_the_day, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y")  ))    
    
        print str(res)

        return res      

    def _get_activity_category_id(self):
        return self.env['extraschool.activitycategory'].search([]).filtered('id').id

    date_of_the_day = fields.Date(required=True, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    place_id = fields.Many2one('extraschool.place', required=True, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    levelid = fields.Many2one('extraschool.level', 'Level', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]},)
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=False, track_visibility='onchange', default=_get_activity_category_id)
    prestationtime_ids = fields.One2many('extraschool.prestation_times_manuel','prestation_times_encodage_manuel_id',copy=True, readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    comment = fields.Text(track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'),
                              ('validated', 'Validated')],
                              'State', required=True, default='draft', track_visibility='onchange'
                              )

    @api.one
    def update_child_list(self):
        print "update_child_list"

        if self.levelid:
            childs = self.env['extraschool.child'].search(
                [('schoolimplantation.id', '=', self.place_id.id),
                 ('levelid.id', '=', self.levelid.id),
                 ('isdisabled', '=', False),
                 ])
        else:
            childs = self.env['extraschool.child'].search(
                [('schoolimplantation.id', '=', self.place_id.id),
                 ('isdisabled', '=', False),
                 ])

        self.prestationtime_ids.unlink()
        # clear child list
        self.prestationtime_ids = [(5, 0, 0)]
        child_reg = []
        print "clear child list done"
        for child in childs:
            print "add child : %s" % (child)
            child_reg.append((0, 0, {'child_id': child,
                                     }))
        self.prestationtime_ids = child_reg

    @api.one
    def validate(self):
        print "validate"

        if self.env.context == None:
            self.env.context = {}
        
#         if "wizard" not in self.env.context:
#             self.env.context["wizard"]= False
            
        presta_obj = self.env['extraschool.pdaprestationtimes']
        
        if self.state == 'draft' or self.env.user.id == 1:
            print "validate !!"
            pod_allready_reseted_ids = []
            for presta in self.prestationtime_ids:
                if presta.prestation_time_entry > 0:
                    print "presta in %s" % (presta)
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
                        
                if presta.prestation_time_exit > 0:
                    print "presta out %s" % (presta)                    
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
                        
        if self.state == 'draft':
            self.state = 'validated'

    @api.one
    def set_to_draft(self):
        if self.state == 'validated':
            self.state = 'draft'
            presta_obj = self.env['extraschool.pdaprestationtimes']
            presta_obj.search([('prestation_times_encodage_manuel_id', '=', self.id)]).unlink()
    