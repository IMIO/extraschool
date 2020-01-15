# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
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

from odoo import models, api, fields
import os

class extraschool_initupdate_wizard(models.TransientModel):
    _name = 'extraschool.initupdate_wizard'
    _description = 'init update'
    _columns = {

    }

    _defaults = {
    }

    @api.model
    def initdefaultvalues(self):
        obj_config = self.env['extraschool.mainsettings']

        config=obj_config.search([('id','=','1')])
        if not config:
            obj_config.create({'id':1,
                               'lastqrcodenbr':0,
                               'qrencode':'/opt/qrencode/qrencode',
                               'tempfolder':'/opt/garderies/appytemp/',
                               'templatesfolder':'/opt/garderies/templates/'
                               })
    @api.model
    def updateapplication(self):
        os.system('/opt/garderies/extraschool/update.sh')
