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
from openerp.api import Environment
from reportlab.graphics.barcode import createBarcodeImageInMemory
import cStringIO
import base64
import os
from datetime import datetime, timedelta
import pdb


class extraschool_config_smartphone(models.Model):
    _name = 'extraschool.config_smartphone'
    _description = 'Configuration of Smartphone'

    activitycategories_ids = fields.Many2many('extraschool.activitycategory','extraschool_smartphone_config_activitycategory_rel', 'id', 'activitycategory_id','Activity categories', required=True)
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
        vals = {}
        for placeid in self.env['extraschool.place'].search([]):
            vals = {'placeid': placeid.id,
                    'name': placeid.name,
                    }

            self.env['extraschool.smartphone'].create(vals)

        

