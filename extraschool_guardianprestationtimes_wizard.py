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
        'guardianid' : fields.many2one('extraschool.guardian', 'Guardian'),
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
        if form['guardianid']:
            cr.execute('select * from extraschool_guardian where id = %s', (form['guardianid'][0],))
        else:
            cr.execute('select * from extraschool_guardian order by name')
        guardianobjs=cr.dictfetchall()
        guardians=[]
        for guardianobj in guardianobjs:
            lines=[]
            cr.execute('select * from extraschool_guardianprestationtimes where guardianid = %s and prestation_date >= %s and prestation_date <= %s order by prestation_date,prestation_time', (guardianobj['id'],form['prestations_from'],form['prestations_to']))
            prestobjs = cr.dictfetchall()
            currentdate=''
            line=''
            for prestobj in prestobjs:            
                if currentdate <> prestobj['prestation_date']:
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
            lines.append(line)
            lines.append(' ')
            guardians.append({'guardianname':guardianobj['name'],'lines':lines})
        obj_config = self.pool.get('extraschool.mainsettings')
        config=obj_config.read(cr, uid, [1],['lastqrcodenbr','qrencode','tempfolder','templatesfolder'])[0] 
        try:
            os.remove(config['tempfolder']+'prestacc.pdf')                   
        except:
            pass
        renderer = appy.pod.renderer.Renderer(config['templatesfolder']+'prestacc.odt', {'guardians':guardians,}, config['tempfolder']+'prestacc.pdf')                
        renderer.run() 
        outfile = open(config['tempfolder']+'prestacc.pdf','r').read()
        out=base64.b64encode(outfile)
        return self.write(cr, uid, ids,{'state' : 'compute_guardianprestationtimes','name':'prestacc.pdf','prestationsreport':out}, context=context)
extraschool_guardianprestationtimes_wizard()
