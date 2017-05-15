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
    username = fields.Char('User name')
    userpassword = fields.Char('User password')
    scanmethod = fields.Selection((('Tag','Tag'),('QR','QR')),'Scan method')
    transfertmethod = fields.Selection((('WIFI','WIFI'),('3G','3G')),'Transfert method')
    qrdownload = fields.Binary('QR Download')
    qrconfig = fields.Binary('QR Config')
    oldversion = fields.Boolean('Old version')
    manualok = fields.Boolean('Authorize manual encoding')
    cfgpassword = fields.Char('Config password', required=True,default='1234')
    maxtimedelta = fields.Integer('Max time delta')
    pda_transmission_ids = fields.One2many('extraschool.pda_transmission', 'smartphone_id')
    softwareversion = fields.Char('Software version')
    
    @api.one
    def update_qr_code(self,vals):
        print "smartphone.update_qr_code"
        value='cfg;' + str(self.id) + ';' + self.transmissiontime + ';' + self.serveraddress + ';' + self.databasename + ';' + self.username + ';' + self.userpassword + ';' + self.scanmethod + ';' + self.transfertmethod+ ';' + self.cfgpassword+ ';'
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
        
        
    @api.one
    def get_currenttime(self):
        print str(datetime.today())
        return datetime.today()
    
    @api.model
    def create(self,vals):
        res = super(extraschool_smartphone, self).create(vals)
        res.write({})
        return res       

    @api.multi
    def write(self,vals):
        #transmission is finished
        if 'lasttransmissiondate' in vals:
            #reset presta of the day if needed
            for smartphone in self:
                if smartphone.pda_transmission_ids:
                    pod_to_check_ids = []
                    for presta in smartphone.pda_transmission_ids.sorted(key=lambda r: r.transmission_date_from)[-1].pda_prestation_times_ids:
                        if presta.prestation_times_of_the_day_id.id not in pod_to_check_ids:
                            pod_to_check_ids.append(presta.prestation_times_of_the_day_id.id)
                    pdb.set_trace()
                    self.env['extraschool.prestation_times_of_the_day'].browse(pod_to_check_ids).reset()
                                                
            return super(extraschool_smartphone, self).write(vals)
        
        print "smartphone.write"
        super(extraschool_smartphone, self).write(vals)  
        print "call self.update_qr_code"             
        self.update_qr_code(vals)
        return super(extraschool_smartphone, self).write(vals)               

    @api.multi
    def copy(self,vals):
        res = super(extraschool_smartphone, self).copy(vals)               
        res.write({})
        return res  

    @api.model
    def ws_verif_transmition(self):
        return_dict = {'return_state': 1,
                       'return_log': ''}
        smartphone_error = self.search([('lasttransmissiondate', '<', (datetime.today() - timedelta(1)).strftime("%Y-%m-%d 00:00:00"))])
        if len(smartphone_error):
            return_dict['return_state'] = 0
            for smartphone in smartphone_error:
                return_dict['return_log'] += "%s-%s\n" % (smartphone.name, smartphone.lasttransmissiondate)
        
        return return_dict            
        
class extraschool_pda_transmission(models.Model):
    _name = 'extraschool.pda_transmission'
    _description = 'PDA pda_transmission'
    
    transmission_date_from = fields.Datetime('Date from')
    transmission_date_to = fields.Datetime('Date to')
    smartphone_id = fields.Many2one('extraschool.smartphone', 'Smartphone')
    pda_prestation_times_ids = fields.One2many('extraschool.pdaprestationtimes','pda_transmission_id')
    state = fields.Selection([('init', 'Init'),
                              ('in_progress', 'In progress'),
                              ('warning', 'Warning'),
                              ('error', 'error'),
                              ('pending', 'Pending'),
                              ('ended', 'Ended')],
                              'validated', default='init'
                              )        
        

