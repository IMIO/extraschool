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
import appy.pod.renderer
import os
from pyPdf import PdfFileWriter, PdfFileReader
import math

class extraschool_guardianprestationtimes_wizard(models.TransientModel):
    _name = 'extraschool.guardianprestationtimes_wizard'
    _description = 'Guardian Prestation Times Wizard'
    
    guardianid = fields.Many2one('extraschool.guardian', 'Guardian')
    prestations_from = fields.Date('Prestations from', required=True)
    prestations_to = fields.Date('Prestations to', required=True)   
    name = fields.Char('File Name', size=16, readonly=True)
    prestationsreport = fields.Binary('File', readonly=True)
    state = fields.Selection([('init', 'Init'),
                              ('compute_guardianprestationtimes', 'Compute prestations report')],
                             'State', required=True, default='init'
                             )

    @api.multi  
    def action_compute_guardianprestationtimes(self):        
        #to do refactoring
        cr, uid = self.env.cr, self.env.user.id
        
extraschool_guardianprestationtimes_wizard()
