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
from datetime import datetime, date, time, timedelta
import pdb
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschool_smartphone(models.Model):
    _name = 'extraschool.smartphone'
    _description = 'Smartphone'

    # We had to put these methods here so we can use default=_get_default_* in the definition of the fields.
    # search([])[-1] get the last smartphone created based on it's ID.
    def _get_default_username(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].username

    def _get_default_serveraddress(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].serveraddress

    def _get_default_databasename(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].databasename

    def _get_default_userpassword(self):
        if len(self.env['extraschool.config_smartphone'].search([])) == 0:
            raise Warning(_("Ther is no configuration for create smartphone"))
        else :
            return self.env['extraschool.config_smartphone'].search([])[-1].userpassword

    def _get_default_maxtimedelta(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].maxtimedelta

    def _get_default_oldversion(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].oldversion

    def _get_default_transmissiontime(self):
        smartphone_obj = self.env['extraschool.smartphone']
        # If it's the first smartphone.
        if (not smartphone_obj.search([])):
            return self.env['extraschool.config_smartphone'].search([])[-1].start_transmissiontime
        # Else we take the last transmissiontime and we add 5 minutes to it.
        else:
            last_transmission = smartphone_obj.search([], order='transmissiontime DESC', limit=1).transmissiontime
            last_transmission = datetime.strptime(last_transmission, "%H:%M") + timedelta(minutes = 5)
            return last_transmission.strftime("%H:%M")

    def _get_default_scanmethod(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].scanmethod

    def _get_default_manualok(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].manualok

    def _get_default_cfgpassword(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].cfgpassword

    def _get_default_transfertmethod(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].transfertmethod

    def _get_activity_category_id(self):
        return self.env['extraschool.config_smartphone'].search([])[-1].activitycategory_id


    name = fields.Char('Name', size=50)
    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place', required=True)
    activitycategories_ids = fields.Many2many('extraschool.activitycategory',
                                              'extraschool_smartphone_activitycategory_rel', 'smartphone_id',
                                              'activitycategory_id', 'Activity categories',
                                              default=_get_activity_category_id, readonly=True)


    lasttransmissiondate = fields.Datetime('Last Transmission Date', readonly=True)
    softwareurl = fields.Char('Software url', size=100, readonly=True, default='http://intranet.la-bruyere.be/garderies/V3-1/AESAndroid.apk')
    transmissiontime = fields.Char('Transmission time', size=5, default=_get_default_transmissiontime)
    serveraddress = fields.Char('Server address', size=50, default=_get_default_serveraddress, readonly=True)
    databasename = fields.Char('Database name', size=30, default=_get_default_databasename, readonly=True)
    username = fields.Char('User name', default=_get_default_username, readonly=True)
    userpassword = fields.Char('User password', default=_get_default_userpassword, readonly=True)
    scanmethod = fields.Selection((('Tag','Tag'),('QR','QR')),'Scan method', default=_get_default_scanmethod, readonly=True)
    transfertmethod = fields.Selection((('WIFI','WIFI'),('3G','3G')),'Transfert method', default=_get_default_transfertmethod)
    qrdownload = fields.Binary('QR Download', readonly=True)
    qrconfig = fields.Binary('QR Config', readonly=True)
    oldversion = fields.Boolean('Old version', default=_get_default_oldversion)
    manualok = fields.Boolean('Authorize manual encoding', default=_get_default_manualok)
    cfgpassword = fields.Char('Config password', required=True, default=_get_default_cfgpassword, readonly=True)
    maxtimedelta = fields.Integer('Max time delta', default=_get_default_maxtimedelta)
    pda_transmission_ids = fields.One2many('extraschool.pda_transmission', 'smartphone_id')
    softwareversion = fields.Char('Software version', readonly=True)

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
        # Todo: See if we still need this.
        if 'lasttransmissiondate' in vals:
            #reset presta of the day if needed
            for smartphone in self:
                if smartphone.pda_transmission_ids:
                    pod_to_check_ids = []
                    for presta in smartphone.pda_transmission_ids.sorted(key=lambda r: r.transmission_date_from)[-1].pda_prestation_times_ids:
                        if presta.prestation_times_of_the_day_id.id not in pod_to_check_ids:
                            pod_to_check_ids.append(presta.prestation_times_of_the_day_id.id)
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
        

