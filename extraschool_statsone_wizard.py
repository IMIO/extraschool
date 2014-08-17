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
import datetime

class extraschool_statsone_wizard(osv.osv_memory):
    _name = 'extraschool.statsone_wizard'

    _columns = {
        'placeid' : fields.many2one('extraschool.place', 'Schoolcare Place', required=True),
        'activitycategory' : fields.many2one('extraschool.activitycategory', 'Activity category', required=True),        
        'year' : fields.integer('Year', required=True),
        'quarter' : fields.selection(((1,'1er'), (2,'2eme'), (3,'3eme'), (4,'4eme')),'Quarter', required=True ),
        'transmissiondate' : fields.date('Transmission date', required=True),
        'name': fields.char('File Name', 16, readonly=True),
        'statsone': fields.binary('File', readonly=True),
        'state' : fields.selection(
            [('init', 'Init'),('compute_statsone', 'Compute statsone')],
            'State', required=True
        ),
    }

    _defaults = {
        'state' : lambda *a: 'init'
    }

    def action_compute_statsone(self, cr, uid, ids, context=None): 
        month_names=('','Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre')
        dt=[]
        prest=[]
        form = self.read(cr,uid,ids,)[-1]
        obj_place = self.pool.get('extraschool.place')  
        year = str(form['year'])
        place = obj_place.read(cr, uid, [form['placeid'][0]],['name','street','zipcode','city'])[0]
        
        if form['quarter'] == '1':
            strperiod_from = year + '-01-01'
            strperiod_to = year + '-03-31'
            quarter = '1er trimestre '+str(form['year'])
        else:
            if form['quarter'] == '2':
                strperiod_from = year + '-04-01'
                strperiod_to = year + '-06-30'
                quarter = '2eme trimestre '+str(form['year'])
            else:
                if form['quarter'] == '3':
                    strperiod_from = year + '-07-01'
                    strperiod_to = year + '-09-30'
                    quarter = '3eme trimestre '+str(form['year'])
                else:
                    if form['quarter'] == '4':
                        strperiod_from = year + '-10-01'
                        strperiod_to = year + '-12-31'
                        quarter = '4eme trimestre '+str(form['year'])        
        period_from=datetime.datetime.strptime(strperiod_from, '%Y-%m-%d').date()
        period_to=datetime.datetime.strptime(strperiod_to, '%Y-%m-%d').date()
        start_month=period_from.month
        end_months=(period_to.year-period_from.year)*12 + period_to.month+1
        months=[{'year':yr, 'month':mn} for (yr, mn) in (
                    ((m - 1) / 12 + period_from.year, (m - 1) % 12 + 1) for m in range(start_month, end_months)
                    )]
        tmpPrestations=[]
        pdays=[]
        nchilds=[]
        totdays=[]
        totmonths=[]
        monthname=[]
        totgen=0
        totwednesdays=0
        for i in range(0,25):
            totdays.append(0)
        for i in range(0,3):
            monthname.append('')
            totmonths.append(0)
        currentdate=period_from
        cr.execute('select count(distinct(childid)) as numberofchilds from extraschool_invoicedprestations left join extraschool_child on childid=extraschool_child.id where placeid=%s and prestation_date>=%s and prestation_date<=%s and activityid in (select id from extraschool_activity where category=%s and subsidizedbyone=true) and levelid in (select id from extraschool_level where leveltype=\'P\')', (form['placeid'][0],strperiod_from,strperiod_to,form['activitycategory'][0],)) 
        totchildsP=cr.dictfetchall()[0]['numberofchilds']
        cr.execute('select count(distinct(childid)) as numberofchilds from extraschool_invoicedprestations left join extraschool_child on childid=extraschool_child.id where placeid=%s and prestation_date>=%s and prestation_date<=%s and activityid in (select id from extraschool_activity where category=%s and subsidizedbyone=true) and levelid in (select id from extraschool_level where leveltype=\'M\')', (form['placeid'][0],strperiod_from,strperiod_to,form['activitycategory'][0],)) 
        totchildsM=cr.dictfetchall()[0]['numberofchilds']
        totchildsMP=totchildsM+totchildsP
        for imonth in range(0,3):
            currentmonth=period_from.month+imonth
            pdays.append([])
            nchilds.append([])
            monthname[imonth]=month_names[currentmonth]
            for iweek in range(0,5):
                pdays[imonth].append([])
                nchilds[imonth].append([])
                if datetime.date(currentdate.year,currentdate.month,01).weekday() > 4 and iweek==0:
                    while currentdate.weekday() != 0:
                        currentdate = currentdate+datetime.timedelta(1)
                for iday in range(0,5):
                    if iday==currentdate.weekday():
                        pdays[imonth][iweek].append(str(currentdate.day))
                        cr.execute('select count(distinct(childid)) as numberofchilds from extraschool_invoicedprestations where placeid=%s and prestation_date=%s and activityid in (select id from extraschool_activity where category=%s and subsidizedbyone=true)', (form['placeid'][0],currentdate,form['activitycategory'][0],)) 
                        totchilds=cr.dictfetchall()[0]['numberofchilds']
                        if totchilds != 0:
                            nchilds[imonth][iweek].append(str(totchilds))
                            totdays[(5*iweek)+iday]=totdays[(5*iweek)+iday]+totchilds
                            totmonths[imonth]=totmonths[imonth]+totchilds
                            totgen=totgen+totchilds
                            if iday==2:
                                totwednesdays=totwednesdays+totchilds
                        else:
                            nchilds[imonth][iweek].append('')
                        nextdate = currentdate+datetime.timedelta(1)
                        if nextdate.month == currentmonth:
                            currentdate=nextdate
                    else:
                        pdays[imonth][iweek].append('')
                        nchilds[imonth][iweek].append('')                
                nextdate = currentdate+datetime.timedelta(2)
                if nextdate.month == currentmonth:
                    currentdate=nextdate
            currentdate = currentdate+datetime.timedelta(1)
                    
        obj_config = self.pool.get('extraschool.mainsettings')
        config=obj_config.read(cr, uid, [1],['lastqrcodenbr','qrencode','tempfolder','templatesfolder'])[0] 
        try:
            os.remove(config['tempfolder']+'detailstatone.pdf')                   
        except:
            pass
        renderer = appy.pod.renderer.Renderer(config['templatesfolder']+'detailstatone.odt', {'nchilds':nchilds,'pdays':pdays,'totdays':totdays,'totmonths':totmonths,'totwednesdays':totwednesdays,'totgen':totgen,'totchildsP':totchildsP,'totchildsM':totchildsM,'totchildsMP':totchildsMP,'place':place,'quarter':quarter,'monthname':monthname}, config['tempfolder']+'detailstatone.pdf')                
        renderer.run() 
        outfile = open(config['tempfolder']+'detailstatone.pdf','r').read()
        out=base64.b64encode(outfile)
        return self.write(cr, uid, ids,{'state' : 'compute_statsone','name':'rapport.pdf','statsone':out}, context=context)
extraschool_statsone_wizard()
