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
from datetime import datetime


class extraschool_smartphone(models.Model):
    _name = 'extraschool.smartphone'
    _description = 'Smartphone'

    name = fields.Char('Name', size=50)         
    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place', required=True)
    activitycategories_ids = fields.Many2many('extraschool.activitycategory','extraschool_smartphone_activitycategory_rel', 'smartphone_id', 'activitycategory_id','Activity categories')
    lasttransmissiondate = fields.Datetime('Last Transmission Date')
    softwareurl = fields.Char('Software url', size=100, readonly=True, default='http://intranet.la-bruyere.be/garderies/V3-1/AESAndroid.apk')
    transmissiontime = fields.Char('Transmission time', size=5)    
    serveraddress = fields.Char('Server address', size=50)
    databasename = fields.Char('Database name', size=30)
    username = fields.Char('User name', size=30)
    userpassword = fields.Char('User password', size=40)
    scanmethod = fields.Selection((('Tag','Tag'),('QR','QR')),'Scan method')
    transfertmethod = fields.Selection((('WIFI','WIFI'),('3G','3G')),'Transfert method')
    qrdownload = fields.Binary('QR Download')
    qrconfig = fields.Binary('QR Config')
    oldversion = fields.Boolean('Old version')
    manualok = fields.Boolean('Authorize manual encoding')
    cfgpassword = fields.Char('Config password', required=True,default='1234')
    maxtimedelta = fields.Integer('Max time delta')
    pda_transmission_ids = fields.One2many('extraschool.pda_transmission', 'smartphone_id')
    
    @api.one
    def get_currenttime(self):
        print str(datetime.today())
        return datetime.today()
    
    @api.multi
    def write(self,vals):
        value='cfg;' + str(self.ids[0]) + ';' + self.transmissiontime + ';' + self.serveraddress + ';' + self.databasename + ';' + self.username + ';' + self.userpassword + ';' + self.scanmethod + ';' + self.transfertmethod+ ';' + self.cfgpassword+ ';'
        if self.manualok:
            value=value+'1'
        else:
            value=value+'0'
        barcode = createBarcodeImageInMemory(
                'QR', value=value, format='png', width=400, height=400,
                humanReadable = 0
            )        
        vals['qrconfig'] = base64.b64encode(barcode)
        value = self.softwareurl
        barcode = createBarcodeImageInMemory(
                'QR', value=value, format='png', width=400, height=400,
                humanReadable = 0
            )        
        vals['qrdownload'] = base64.b64encode(barcode)
      
        self = super(extraschool_smartphone, self).write(vals)        

        return self
        
class extraschool_pda_transmission(models.Model):
    _name = 'extraschool.pda_transmission'
    _description = 'PDA pda_transmission'
    
    transmission_date_from = fields.Datetime('Date from', required=True)
    transmission_date_to = fields.Datetime('Date to', required=True)
    smartphone_id = fields.Many2one('extraschool.smartphone', 'Smartphone', required=True)
    pda_prestation_times_ids = fields.One2many('extraschool.pdaprestationtimes','pda_transmission_id')
    state = fields.Selection([('init', 'Init'),
                              ('in_progress', 'In progress'),
                              ('warning', 'Warning'),
                              ('error', 'error'),
                              ('pending', 'Pending'),
                              ('ended', 'Ended')],
                              'validated', required=True, default='init'
                              )        
        

