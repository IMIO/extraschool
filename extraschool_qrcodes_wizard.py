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

class extraschool_qrcodes_wizard(models.TransientModel):
    _name = 'extraschool.qrcodes_wizard'


    quantity = fields.Integer('Quantity to print')
    name = fields.Char('File Name', size=16, readonly=True)
    qrcodes = fields.Binary('File', readonly=True)
    state = fields.Selection([('init', 'Init'),
                             ('print_qrcodes', 'Print QRCodes')],
                            'State', required=True, default='init'
                            )



    def action_print_qrcodes(self):
#         obj_config = self.pool.get('extraschool.mainsettings')
#         config=obj_config.read(cr, uid, [1],['lastqrcodenbr','qrencode','tempfolder','templatesfolder'])[0]             
#         form = self.read(cr,uid,ids,)[-1]
#         files=[]
#         for i in range(config['lastqrcodenbr']+1,config['lastqrcodenbr']+form['quantity']+1):            
#             os.system(config['qrencode']+' -o '+config['tempfolder']+str(i)+'.png -s 4 -l Q '+str(i))        
#             files.append({'fname':config['tempfolder']+str(i)+'.png'})
#         try:
#             os.remove(config['tempfolder']+'codes.pdf')
#         except:
#             pass
#         renderer = appy.pod.renderer.Renderer(config['templatesfolder']+'qrcodes.odt',{'files':files,}, config['tempfolder']+'codes.pdf')                
#         renderer.run()     
#         for i in range(config['lastqrcodenbr']+1,config['lastqrcodenbr']+form['quantity']+1):            
#             os.remove(config['tempfolder']+str(i)+'.png')
#         mainsettings_id = obj_config.write(cr, uid, [1], {'lastqrcodenbr':config['lastqrcodenbr']+form['quantity']+1}, context=context)           
#         outfile = open(config['tempfolder']+'codes.pdf','r').read()
#         out=base64.b64encode(outfile)
#         
#        return self.write(cr, uid, ids, {'state':'print_qrcodes', 'qrcodes':out, 'name':'qrcodes.pdf'}, context=context)
        #to do refactoring new report
        return True
    
extraschool_qrcodes_wizard()

