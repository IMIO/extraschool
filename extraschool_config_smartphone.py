# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014 
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

from openerp import models, api, fields, _
from openerp.api import Environment
from reportlab.graphics.barcode import createBarcodeImageInMemory
import cStringIO
import base64
import os
from datetime import datetime, timedelta
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschool_config_smartphone(models.Model):
    _name = 'extraschool.config_smartphone'
    _description = 'Configuration of Smartphone'

    def _get_activity_category_id(self):
        return self.env['extraschool.activitycategory'].search([]).filtered('id').id

    activitycategory_id = fields.Many2one('extraschool.activitycategory', 'Activity category', required=True,
                                       default=_get_activity_category_id)
    start_transmissiontime = fields.Char('Transmission time', size=5, default='22:00', required=True)
    serveraddress = fields.Char('Server address', size=50, default='https://', required=True)
    databasename = fields.Char('Database name', size=30, required=True)
    username = fields.Char('User name', required=True)
    userpassword = fields.Char('User password', required=True)
    scanmethod = fields.Selection((('Tag','Tag'),('QR','QR')),'Scan method', required=True)
    oldversion = fields.Boolean('Old version')
    manualok = fields.Boolean('Authorize manual encoding')
    cfgpassword = fields.Char('Config password',default='1234', required=True)
    maxtimedelta = fields.Integer('Max time delta')
    transfertmethod = fields.Selection((('WIFI', 'WIFI'), ('3G', '3G')), 'Transfert method')

    @api.one
    def generate(self):
        vals = {}   # Create dictionnary.
        for placeid in self.env['extraschool.place'].search([]):
            # Put placeid and name for the smartphone in the dictionnary because we don't need it in this model.
            # So We create it.
            vals = {'placeid': placeid.id,
                    'name': placeid.name,
                    }

            self.env['extraschool.smartphone'].create(vals)

    @api.model
    def create(self, vals):
        # Make sure there is only 1 configuration to avoid mixup.
        if len(self.env['extraschool.config_smartphone'].search([])) >= 1:
            raise Warning(_("You can only do 1 configuration."))
        else:
            res = super(extraschool_config_smartphone, self).create(vals)
            res.write({})
            return res

    @api.multi
    def write(self, vals):
        smartphone_obj = self.env['extraschool.smartphone']
        # Check if we change the transmissiontime.
        if 'start_transmissiontime' in vals:
            new_vals = {}                                               # New dictionnary to avoid error when we pass start_transmissiontime to smartphone object when the object doesn't have that value.
            vals['transmissiontime'] = vals['start_transmissiontime']
            new_vals['transmissiontime'] = vals['transmissiontime']     # We only put the transmissiontime in the dictionnary.
            for smartphone in smartphone_obj.search([]):
                smartphone_obj.browse(smartphone.id).write(new_vals)
                # Add 5 minutes for the next smartphone.
                new_vals['transmissiontime'] = datetime.strptime(new_vals['transmissiontime'], "%H:%M") + timedelta(minutes=5)
                new_vals['transmissiontime'] = new_vals['transmissiontime'].strftime("%H:%M")
        else:
            # Else use the normal write.
            for smartphone in smartphone_obj.search([]):
                smartphone_obj.browse(smartphone.id).write(vals)

        return super(extraschool_config_smartphone, self).write(vals)