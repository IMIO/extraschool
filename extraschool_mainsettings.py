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
from openerp.exceptions import Warning

class extraschool_mainsettings(models.Model):
    _name = 'extraschool.mainsettings'
    _description = 'Main Settings'

    lastqrcodenbr = fields.Integer('lastqrcodenbr')
    qrencode = fields.Char('qrencode', size=80)
    tempfolder = fields.Char('tempfolder', size=80)
    templatesfolder = fields.Char('templatesfolder', size=80)
    codasfolder = fields.Char('codasfolder', size=80)
    processedcodasfolder = fields.Char('processedcodasfolder', size=80)
    emailfornotifications = fields.Char('Email for notifications', size=80)
        
    @api.one
    def update(self):
        self.write({'lastqrcodenbr':self.lastqrcodenbr, 'qrencode':self.qrencode, 'tempfolder':self.tempfolder,'templatesfolder':self.templatesfolder, 'codasfolder':self.codasfolder,'processedcodasfolder':self.processedcodasfolder})

        raise Warning('record saved!')
        
    def initdef(self):
        pass
    
extraschool_mainsettings()
