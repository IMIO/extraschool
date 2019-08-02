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
import logging

_logger = logging.getLogger(__name__)


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
        return self.env['extraschool.config_smartphone'].search([])[-1].activitycategory_id.ids

    def _get_last_transmission(self):
        for rec in self:
            last_transmission_date = self.env['extraschool.pda_transmission'].search([('smartphone_id', '=', rec.id)],
                                                                   order='transmission_date_from DESC', limit=1).transmission_date_from
            rec.lasttransmissiondate = last_transmission_date


    name = fields.Char('Name', size=50)
    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place', required=True)
    activitycategories_ids = fields.Many2many('extraschool.activitycategory',
                                              'extraschool_smartphone_activitycategory_rel', 'smartphone_id',
                                              'activitycategory_id', 'Activity categories',
                                              default=_get_activity_category_id, readonly=True)


    lasttransmissiondate = fields.Datetime('Last Transmission Date', compute=_get_last_transmission, store=False, readonly=True)
    softwareurl_v9 = fields.Char('Software url', size=100, readonly=True, default='https://static.imio.be/aes/aesmobile.apk')
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
    smartphone_log_ids = fields.One2many('extraschool.smartphone_log', 'smartphone_id')
    smartphone_detail_log_ids = fields.One2many('extraschool.smartphone_detail_log', 'smartphone_id')

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

        value = self.softwareurl_v9
        barcode = createBarcodeImageInMemory(
                'QR', value=value, format='png', width=400, height=400,
                humanReadable = 0
            )
        vals['qrdownload'] = base64.b64encode(barcode)

    @api.one
    def get_currenttime(self):
        print str(datetime.today())
        return datetime.today()

    @api.multi
    def update_app_version(self, version):
        version = str(version)
        if version:
            self.softwareversion = version
        else:
            self.softwareversion = "Aucune info"

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

##############################################################################
#
#    AESMobile
#    Copyright (C) 2018
#    Colicchia Michaël & Delaere Olivier - Imio (<http://www.imio.be>).
#
##############################################################################

    @api.multi
    def set_smartphone_error(self, smartphone_id, error, string_error):

        type = "Children" if error == 1 else "Guardians"

        _logger.error( "Smartphone id: " + smartphone_id + "Error number: " + type + "Error message: " + string_error)

    @staticmethod
    def set_error(cr, uid, smartphone_id, error, string_error, context=None):
        """
        :param cr, uid, context needed for a static method
        :param smartphone_id: Id of the smartphone that contact us.
        :return: Dictionnary of children {id: , nom: , prenom:, tagid:}
        """
        # Declare new Environment.
        env = api.Environment(cr, uid, context={})

        extraschool_smartphone.set_smartphone_error(env['extraschool.smartphone'], smartphone_id, error,
                                                    string_error)

        return True

class extraschool_pda_transmission(models.Model):
    _name = 'extraschool.pda_transmission'
    _description = 'PDA pda_transmission'

    transmission_date_from = fields.Datetime('Date from')
    transmission_date_to = fields.Datetime('Date to')
    smartphone_id = fields.Many2one('extraschool.smartphone', 'Smartphone')
    pda_prestation_times_ids = fields.One2many('extraschool.pdaprestationtimes', 'pda_transmission_id')
    state = fields.Selection([('init', 'Init'),
                              ('in_progress', 'In progress'),
                              ('warning', 'Warning'),
                              ('error', 'error'),
                              ('pending', 'Pending'),
                              ('ended', 'Ended')],
                              'validated', default='init'
                              )

class extraschool_smartphone_log(models.Model):
    _name = 'extraschool.smartphone_log'
    _description = 'Log pour smartphones'

    title = fields.Char('Transmission')
    date_of_transmission = fields.Datetime('Date de transmission', default=datetime.now())
    time_of_transmission = fields.Char('Temps d\'éxécution')
    smartphone_id = fields.Many2one('extraschool.smartphone', 'smartphone_id')


class extraschool_smartphone_detail_log(models.Model):
    _name = 'extraschool.smartphone_detail_log'
    _description = 'Log détaillé pour smartphones'

    text = fields.Text('Texte', readonly=True)
    date_of_transmission = fields.Datetime('Date de transmission', default=datetime.now(), readonly=True)
    level = fields.Char('Niveau', readonly=True)
    smartphone_id = fields.Many2one('extraschool.smartphone', 'smartphone_id', readonly=True)

    @api.multi
    def print_log(self, message, smartphone_id):
        for line in message['logs']:
            try:
                date = datetime.strptime(str(line['datetime']), '%Y%m%dT%H%M%S')
            except:
                date = 'Could not format date: {}'.format(line['timestamp'])

            error_message = "Error message for Smartphone logs"
            message_decode = line['message']
            imei = line['phone_imei']
            try:
                imei = imei.encode('utf-8')
            except :
                imei = 'Error decode'
            try:
                message_decode.encode('utf-8')
            except:
                message_decode = "Error encoding message log"
            try:
                message_log = '{} Smartphone id: {} version: {} logger: {} message: {} ###### serial: {} imei: {}'.format(
                    str(date),
                    smartphone_id,
                    message["app_version"],
                    line['logger'],
                    message_decode,
                    line['phone_serial'],
                    imei,
                )
            except:
                message_log = "There has been an error on the construction of the log message"
            if "INFO" in line['level']:
                try:
                    _logger.info(message_log)
                except:
                    _logger.error(error_message)

            elif "WARN" in line['level']:
                try:
                    _logger.warning(message_log)
                except:
                    _logger.error(error_message)
            else:
                try:
                    _logger.error(message_log)
                except:
                    _logger.error(error_message)

        if "app_version" in message:
            app_version = message["app_version"]
        else:
            app_version = False

        smartphone_obj = self.env['extraschool.smartphone'].search([('id', '=', smartphone_id)])
        smartphone_obj.update_app_version(app_version)


    @staticmethod
    def send_log(cr, uid, message, smartphone_id, context=None):
        """
        :param cr, uid, context needed for a static method
        :param smartphone_id: Id of the smartphone that contact us.
        :return: Dictionnary of children {id: , nom: , prenom:, tagid:}
        """
        # Declare new Environment.
        env = api.Environment(cr, uid, context={})
        extraschool_smartphone_detail_log.print_log(env['extraschool.smartphone_detail_log'], message, smartphone_id)

        return True

