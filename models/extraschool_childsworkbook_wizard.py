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
from odoo.api import Environment
import cStringIO
import base64
import os
from pyPdf import PdfFileWriter, PdfFileReader

class extraschool_childsworkbook_wizard(models.TransientModel):
    _name = 'extraschool.childsworkbook_wizard'

    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place')
    child_id = fields.Many2one('extraschool.child', 'Child')
    name = fields.Char('File Name', size=16, readonly=True)
    childsworkbook = fields.Binary('File', readonly=True)
    state = fields.Selection([('init', 'Init'),
                              ('print_childsworkbook', 'Print Childs Workbook')],
                              'State', required=True, default='init'
                              )

    @api.multi  
    def action_print_childsworkbook(self, ids):
        #to do refactoring avec browse
        cr, uid = self.env.cr, self.env.user.id

extraschool_childsworkbook_wizard()
