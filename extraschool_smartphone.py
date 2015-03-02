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
    userpassword = fields.Char('User password', size=20)
    scanmethod = fields.Selection((('Tag','Tag'),('QR','QR')),'Scan method')
    transfertmethod = fields.Selection((('WIFI','WIFI'),('3G','3G')),'Transfert method')
    qrdownload = fields.Binary('QR Download')
    qrconfig = fields.Binary('QR Config')
    oldversion = fields.Boolean('Old version')
    maxtimedelta = fields.Integer('Max time delta')
    
    @api.multi
    def write(self,vals):
        value='cfg;' + str(self.ids[0]) + ';' + self.transmissiontime + ';' + self.serveraddress + ';' + self.databasename + ';' + self.username + ';' + self.userpassword + ';' + self.scanmethod + ';' + self.transfertmethod
        barcode = createBarcodeImageInMemory(
                'QR', value=value, format='png', width=400, height=400,
                humanReadable = 0
            )        
        vals['qrconfig'] = base64.b64encode(barcode)
        #config = self.env['extraschool.mainsettings'].browse(1)
        #os.system(config.qrencode + ' -o ' + config.tempfolder + 'qrdownload.png -s 4 -l Q ' + self.softwareurl)                
        #qrfile = open(config.tempfolder + 'qrdownload.png','r').read()        
        #vals['qrdownload'] = base64.b64encode(qrfile)        
        self = super(extraschool_smartphone, self).write(vals)        
        #os.system(config.qrencode + ' -o ' + config.tempfolder + 'qrconfig.png -s 4 -l Q "cfg;' + str(self.ids[0]) + ';' + self.transmissiontime + ';' + self.serveraddress + ';' + self.databasename + ';' + self.username + ';' + self.userpassword + ';' + self.scanmethod + ';' + self.transfertmethod + '"')                
        #qrfile = open(config['tempfolder']+'qrconfig.png','r').read()        
        #vals['qrconfig'] = base64.b64encode(qrfile)
        return self
        
extraschool_smartphone()
