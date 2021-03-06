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
    prestation_ids = fields.One2many('extraschool.guardianprestationtimes', 'guardianid')
    comment = fields.Text('Comment', track_visibility='onchange')

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

    def _get_guardians(self):
        return self.env['extraschool.guardian'].search([('id', '=', self._context.get('active_ids'))])

    validity_from = fields.Date('Date from')
    validity_to = fields.Date('Date to')
    guardian_ids = fields.Many2many('extraschool.guardian',
                                    'extraschool_guardian_wizard_rel',
                                    'guardian_id',
                                    'wizard_id',
                                    'ID Guardians',
                                    default=_get_guardians)

    @api.multi
    def generate_horaire(self):
        if self.validity_from > self.validity_to :
            raise Warning(_("La date de fin doit être plus grande que la date de début !"))

        datas = {
            'ids': self.guardian_ids.ids,
            'model': 'extraschool.horaire_guardian_wizard',
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'extraschool.tpl_guardian_horaire_wizard_report',
            'datas': datas,
            'report_type': 'qweb-pdf',
        }