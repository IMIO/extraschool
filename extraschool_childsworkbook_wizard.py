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

from openerp.osv import osv, fields
import cStringIO
import base64
import appy.pod.renderer
import os
from pyPdf import PdfFileWriter, PdfFileReader

class extraschool_childsworkbook_wizard(osv.osv_memory):
    _name = 'extraschool.childsworkbook_wizard'

    _columns = {
        'placeid' : fields.many2one('extraschool.place', 'Schoolcare Place'),
        'child_id' : fields.many2one('extraschool.child', 'Child'),
        'name': fields.char('File Name', 16, readonly=True),
        'childsworkbook': fields.binary('File', readonly=True),
        'state' : fields.selection(
            [('init', 'Init'),('print_childsworkbook', 'Print Childs Workbook')],
            'State', required=True
        ),
    }

    _defaults = {
        'state' : lambda *a: 'init'
    }


    def action_print_childsworkbook(self, cr, uid, ids, context=None):
        obj_config = self.pool.get('extraschool.mainsettings')
        config=obj_config.read(cr, uid, [1],['lastqrcodenbr','qrencode','tempfolder','templatesfolder'])[0]             
        form = self.read(cr,uid,ids,)[-1]
        childrecords=[]
        tagids=[]
        
        obj_childs = self.pool.get('extraschool.child')    
        obj_parents = self.pool.get('extraschool.parent')
        if form['child_id']:
            child_ids=[form['child_id'][0]]
        else:    
            obj_place = self.pool.get('extraschool.place')
            schoolimplantationids=obj_place.read(cr, uid, [form['placeid'][0]],['schoolimplantation_ids'])[0]    
            child_ids=obj_childs.search(cr, uid, [('schoolimplantation', 'in', schoolimplantationids['schoolimplantation_ids'])], order='name')        
        childs = obj_childs.read(cr, uid, child_ids,context=context)
                
        for child in childs:
            if child['tagid']:
                childparent =  obj_parents.read(cr, uid, [child['parentid'][0]],context=context)[0]
                os.system(config['qrencode']+' -o '+config['tempfolder']+str(child['tagid'])+'.png -s 4 -l Q '+str(child['tagid']))        
                tagids.append(config['tempfolder']+str(child['tagid'])+'.png')
                if childparent['housephone']:
                    parenthousephone = childparent['housephone']
                else:
                    parenthousephone = ''
                if childparent['workphone']:
                    parentworkphone = childparent['workphone']
                else:
                    parentworkphone=''
                if childparent['gsm']:
                    parentgsm = childparent['gsm']
                else:
                    parentgsm = ''
                childclass=''
                if child['classid']:
                    childclass=child['classid'][1]
            
                childrecords.append({'name':child['name'],
                    'qrcode':config['tempfolder']+str(child['tagid'])+'.png',
                    'class':childclass,
                    'parentname':childparent['name'],
                    'parenthousephone':parenthousephone,
                    'parentworkphone':parentworkphone,
                    'parentgsm':parentgsm,
                    })
        
        try:
            os.remove(config['tempfolder']+'farde.pdf')
        except:
            pass
        renderer = appy.pod.renderer.Renderer(config['templatesfolder']+'farde.odt',{'childs':childrecords,}, config['tempfolder']+'farde.pdf')                
        renderer.run()     
        
        for tagid in tagids:            
            os.remove(tagid)        
        outfile = open(config['tempfolder']+'farde.pdf','r').read()
        out=base64.b64encode(outfile)        
        return self.write(cr, uid, ids, {'state' : 'print_childsworkbook', 'childsworkbook':out, 'name':'classeur.pdf'}, context=context)
extraschool_childsworkbook_wizard()
