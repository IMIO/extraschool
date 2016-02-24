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
import cStringIO
import base64
import os

class extraschool_qrcodes_wizard(models.TransientModel):
    _name = 'extraschool.qrcodes_wizard'

    
    quantity = fields.Integer('Quantity to print')
    print_type = fields.Selection((('qrcode','Qr Code'),('logo','Logo'),),'Print Type', required=True)
    last_id = fields.Integer('Last id')
    name = fields.Char('File Name', size=16, readonly=True)
    print_value = fields.Boolean('Print QrCode value')
    logo = fields.Binary()
    format = fields.Selection([('extraschool.tpl_qrcodes_wizard_report', 'Standard'),
                             ('extraschool.tpl_qrcodes_precut_wizard_report', 'Precut')],
                            'Format', required=True, default='extraschool.tpl_qrcodes_wizard_report'
                            )  
    state = fields.Selection([('init', 'Init'),
                             ('print_qrcodes', 'Print QRCodes')],
                            'State', required=True, default='init'
                            )


    @api.multi
    def action_print_qrcodes(self):
        
        report = self.env['report']._get_report_from_name('extraschool.tpl_qrcodes_wizard_report')
        config = self.env['extraschool.mainsettings'].browse([1])
        #get last qrcode value from config
        self.last_id = config.lastqrcodenbr + 1

        #SET last qrcode value to config
        config.lastqrcodenbr = config.lastqrcodenbr + self.quantity

        datas = {
        'ids': self.ids,
        'model': report.model, 
        }
        
        return {
               'type': 'ir.actions.report.xml',
               'report_name': self.format,
               'datas': datas,
               'report_type': 'qweb-pdf',
           }        

