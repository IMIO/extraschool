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
import math

class extraschool_guardianprestationtimes_wizard(osv.osv_memory):
    _name = 'extraschool.guardianprestationtimes_wizard'
    _description = 'Guardian Prestation Times Wizard'
    
    _columns = {        
        'guardianid' : fields.many2one('extraschool.guardian', 'Guardian', required=True),
        'prestations_from' : fields.date('Prestations from', required=True),
        'prestations_to' : fields.date('Prestations to', required=True),   
        'name': fields.char('File Name', 16, readonly=True),
        'prestationsreport': fields.binary('File', readonly=True),
        'state' : fields.selection(
            [('init', 'Init'),('compute_guardianprestationtimes', 'Compute prestations report')],
            'State', required=True
        ),
    }

    _defaults = {
        'state' : lambda *a: 'init'
    }

    def action_compute_guardianprestationtimes(self, cr, uid, ids, context=None):        
        form = self.read(cr,uid,ids,)[-1]
        obj_guardian = self.pool.get('extraschool.guardian')          
        guardian = obj_guardian.read(cr, uid, [form['guardianid'][0]],['name'])[0]
        lines=[]
        obj_guardianprest = self.pool.get('extraschool.guardianprestationtimes')
        #prestids=obj_guardianprest.search(cr,uid,[('guardianid', '=', form['guardianid'][0]),('prestation_date', '>=', form['prestations_from']),('prestation_date', '<=', form['prestations_to'])],order='prestation_date,prestation_time')
        
        cr.execute('select * from extraschool_guardianprestationtimes where guardianid = %s and prestation_date >= %s and prestation_date <= %s order by prestation_date,prestation_time', (form['guardianid'][0],form['prestations_from'],form['prestations_to']))
        
        #prestobjs = obj_guardianprest.read(cr, uid,prestids,['prestation_date','prestation_time','ES'])
        prestobjs = cr.dictfetchall()
        currentdate=''
        line=''
        for prestobj in prestobjs:            
            if currentdate <> prestobj['prestation_date']:
                lines.append(' ')
                lines.append(line)
                line=prestobj['prestation_date']+':'
                currentdate = prestobj['prestation_date']                
            strhour=str(int(math.floor(prestobj['prestation_time'])))
            strmin=str(int((prestobj['prestation_time']-math.floor(prestobj['prestation_time']))*60))
            if len(strhour)==1:
                strhour='0'+strhour
            if len(strmin)==1:
                strmin='0'+strmin
            hprest=strhour+':'+strmin
            line=line+' ['+prestobj['ES']+']'+hprest
        lines.append(' ')
        lines.append(line)
        obj_config = self.pool.get('extraschool.mainsettings')
        config=obj_config.read(cr, uid, [1],['lastqrcodenbr','qrencode','tempfolder','templatesfolder'])[0] 
        try:
            os.remove(config['tempfolder']+'prestacc.pdf')                   
        except:
            pass
        renderer = appy.pod.renderer.Renderer(config['templatesfolder']+'prestacc.odt', {'guardianname':guardian['name'],'lines':lines}, config['tempfolder']+'prestacc.pdf')                
        renderer.run() 
        outfile = open(config['tempfolder']+'prestacc.pdf','r').read()
        out=base64.b64encode(outfile)
        return self.write(cr, uid, ids,{'state' : 'compute_guardianprestationtimes','name':'prestacc.pdf','prestationsreport':out}, context=context)
extraschool_guardianprestationtimes_wizard()
