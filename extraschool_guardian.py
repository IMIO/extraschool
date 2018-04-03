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

from openerp import models, api, fields, _
from openerp.api import Environment
import cStringIO
import base64
from openerp.exceptions import except_orm, Warning, RedirectWarning
import os

class extraschool_guardian(models.Model):
    _name = 'extraschool.guardian'
    _description = 'Guardian'
    _inherit = 'mail.thread'
    
    name = fields.Char(compute='_name_compute',string='FullName', size=100, store=True)
    firstname = fields.Char('FirstName', size=50)
    lastname = fields.Char('LastName', size=50 , required=True)
    tagid = fields.Char('Tag ID', size=50, track_visibility='onchange')
    otherref = fields.Char('Other ref')
    weekly_schedule = fields.Float('Horaire hebdomadaire')
    oldid = fields.Integer('oldid')
    isdisabled = fields.Boolean('Disabled', track_visibility='onchange')

    @api.depends('firstname','lastname')
    def _name_compute(self):
        for record in self:
            record.name = '%s %s'  % (record.lastname, record.firstname)

    @api.one
    def unlink(self):
        self.isdisabled = True

    @api.one    
    def action_gentagid(self):   
        if not self.tagid :
            config = self.env['extraschool.mainsettings'].browse([1])
            self.tagid = config.lastqrcodenbr = config.lastqrcodenbr + 1
        
        return self.tagid
        # return long(self.tagid)

    @api.one    
    def get_qr_logo(self):   
        config = self.env['extraschool.mainsettings'].browse([1])
        logo = config.logo
        
        return logo

    @api.multi
    def get_presta(self):

        return {'name': 'Présences',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.guardianprestationtimes',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('guardianid', '=', self.id), ]
                }


extraschool_guardian()

class extraschool_horaire_guardian_wizard_form(models.TransientModel):
    _name = 'extraschool.horaire_guardian_wizard'

    validity_from = fields.Date('Date from')
    validity_to = fields.Date('Date to')
    guardian_ids = fields.Many2many('extraschool.guardian', 'extraschool_guardian_wizard_rel', 'guardian_id', 'wizard_id',
                                 'ID Guardians')
    horaire_ids = fields.Many2many('extraschool.guardianprestationtimes', 'extraschool_horaire_wizard_rel', 'guardian_id',
                                    'horaire_id',
                                    'ID Horaire')

    @api.multi
    def generate_horaire(self):
        report = self.env['report']._get_report_from_name('extraschool.tpl_guardian_horaire_wizard_report')
        '''import ipdb; ipdb.set_trace()'''
        horaire_list = []

        if self.validity_from > self.validity_to :
            raise Warning(_("La date de fin doit être plus grande que la date de début !"))
        
        vals = {'guardian_ids': [[6, 0, self._context.get('active_ids')]],
                }
        # self.env['extraschool.horaire_guardian_wizard'].browse(self.id).write(vals)
        # for guardian in self.env['extraschool.guardian'].browse(self._context.get('active_ids')):
        #     print "là"
        #     prestation_ids = self.env['extraschool.guardianprestationtimes'].search([('guardianid', '=', guardian.id),('prestation_date','>=',self.validity_from),('prestation_date','<=',self.validity_to)])
        #     if prestation_ids :
        #         for prestation in prestation_ids :
        #             horaire_list.append(prestation.id)
        #
        #             vals_horaire = {'horaire_ids': [[6, 0, horaire_list]],
        #                     }
        #             self.env['extraschool.horaire_guardian_wizard'].browse(self.id).write(vals_horaire)
        #
        # active_id = self._context.get('active_ids')

        datas = {
            'ids': self.ids,
            'model': report.model,
        }

        print datas
        print "self.ids", self.ids
        print "self._context.get('active_ids')" , self._context.get('active_ids')

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'extraschool.tpl_guardian_horaire_wizard_report',
            'datas': datas,
            'report_type': 'qweb-pdf',
        }
