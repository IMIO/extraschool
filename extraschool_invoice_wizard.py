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
from datetime import date
import datetime
import calendar
import cStringIO
import base64
import appy.pod.renderer
import os
import math
import xlrd
import lbutils
import re
from math import *
from pyPdf import PdfFileWriter, PdfFileReader

class extraschool_invoice_wizard(osv.osv_memory):
    _name = 'extraschool.invoice_wizard'
    _schoolimplantationids = []

    def _get_schoolimplantations(self, cr, uid, ids, field_names, arg=None, context=None):
        result = {ids[0]: self._schoolimplantationids, 'nodestroy': True}
        return result

    def _set_schoolimplantations(self, cr, uid, ids, field_names, value, arg=None, context=None):
        self._schoolimplantationids=value[0][2]
    
    def _get_defaultfrom(self,cr, uid, ids, context=None):
        cr.execute('select max(prestation_date) as prestation_date from extraschool_invoicedprestations')
        rec=cr.dictfetchall()[0]
        try:
            fromdate=datetime.datetime.strptime(rec['prestation_date'], '%Y-%m-%d').date()
            frommonth=fromdate.month+1
            fromyear=fromdate.year
            if frommonth == 13:
                frommonth = 12
                fromyear = fromyear +1
            strfrommonth=str(frommonth)
            if len(strfrommonth) == 1:
                strfrommonth='0'+strfrommonth
            return str(fromyear)+'-'+strfrommonth+'-01'            
        except:
            return str(datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,1))
            
    def _get_defaultto(self,cr, uid, ids, context=None):
        #todate=datetime.date(2013,11,1)
        cr.execute('select max(prestation_date) as prestation_date from extraschool_invoicedprestations')
        lastdate = cr.dictfetchall()[0]['prestation_date']
        if lastdate and (lastdate < datetime.datetime.now()):
            todate=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,1)-datetime.timedelta(1)
        else:
            month=datetime.datetime.now().month
            if month == 12:
                month=1
            else:
                month=month+1
            todate=datetime.date(datetime.datetime.now().year,month,1)-datetime.timedelta(1)
            
        return str(todate)

        
    def _get_defaultinvdate(cr, uid, ids, context=None):
        invdate=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)+datetime.timedelta(1)
        return str(invdate)
    
    def _get_defaultinvterm(cr, uid, ids, context=None):
        termdate=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)+datetime.timedelta(16)
        return str(termdate)

    _columns = {        
        'schoolimplantationid' : fields.function(fnct=_get_schoolimplantations,fnct_inv=_set_schoolimplantations, method=True, type='many2many', relation='extraschool.schoolimplantation', string='School implantations'), 
        'activitycategory' : fields.many2one('extraschool.activitycategory', 'Activity category', required=True),        
        'period_from' : fields.date('Period from', required=True),
        'period_to' : fields.date('Period to', required=True),
        'invoice_date' : fields.date('invoice date', required=True),
        'invoice_term' : fields.date('invoice term', required=True),
        'name': fields.char('File Name', 16, readonly=True),
        'invoices': fields.binary('File', readonly=True),
        'state' : fields.selection(
            [('init', 'Init'),('compute_invoices', 'Compute invoices')],
            'State', required=True
        ),
    }

    _defaults = {
        'state' : lambda *a: 'init',
        #'schoolimplantationid' : lambda *a: [(6,0,[3])],
        'activitycategory' : lambda *a: 1,
        'period_from' : _get_defaultfrom,
        'period_to' : _get_defaultto,
        'invoice_date' : _get_defaultinvdate,
        'invoice_term' : _get_defaultinvterm,
    }

    def computediscount(self, cr, uid,childid,period,childtypeid,childactivities):
        amount=0.0
        if childactivities:
            cr.execute('select * from "extraschool_discount" where period = %s and id in (select discount_id from extraschool_discount_childtype_rel where childtype_id = %s) and id in (select discount_id from extraschool_discount_activity_rel where activity_id in '+str(childactivities.keys()).replace('[','(').replace(']',')')+')', (period,childtypeid,))                
            discounts=cr.dictfetchall()                  
            for discount in discounts:
                totactivities=0.0
                havediscount=False
                cr.execute('select activity_id from "extraschool_discount_activity_rel" where discount_id = %s', (discount['id'],))                
                discountactivities=cr.dictfetchall()
                discountactivitiesids=[]
                for discountactivity in discountactivities:
                    if str(discountactivity['activity_id']) in childactivities.keys():
                        discountactivitiesids.append(str(discountactivity['activity_id']))
                for childactivityid in discountactivitiesids:
                    if (havediscount == False) or (discount['wichactivities'] != 'OneOf'):
                        rulesok=True
                        cr.execute('select * from "extraschool_discountrule" where id in (select discountrule_id from extraschool_discount_discountrule_rel where discount_id = %s)', (discount['id'],))                
                        discountrules=cr.dictfetchall()
                        if discountrules:
                            for discountrule in discountrules:
                                cr.execute('select id from extraschool_child where id= %s and '+discountrule['field']+' '+discountrule['operator']+' '+discountrule['value'],(childid,))
                                rulecount = cr.dictfetchall()
                                if not rulecount:
                                    rulesok=False
                        else:
                            havediscount=True
                        if rulesok:
                            havediscount=True
                            if discount['wichactivities'] != 'Sum':
                                if discount['discounttype'] == 'sub':
                                    amount=amount+float(discount['discount'])
                                elif discount['discounttype'] == 'prc': 
                                    amount=amount+((childactivities[childactivityid] * float(discount['discount'].split('%')[0])) / 100)
                                elif discount['discounttype'] == 'max':
                                    if childactivities[childactivityid] > float(discount['discount']):
                                        amount=amount+(childactivities[childactivityid]-float(discount['discount']))
                            else:
                                totactivities=totactivities+childactivities[childactivityid]
                if discount['wichactivities'] == 'Sum':
                    if discount['discounttype'] == 'sub':
                        amount=amount+float(discount['discount'])
                    elif discount['discounttype'] == 'prc':
                        amount=amount+((totactivities * discount['discount'].split('%')[0]) / 100)
                    elif discount['discounttype'] == 'max':
                        if totactivities > float(discount['discount']):
                                amount=amount+(totactivities-float(discount['discount']))
        return amount
    
    def _compute_invoices(self, cr, uid, form, context=None):
        obj_config = self.pool.get('extraschool.mainsettings')
        obj_activitycategory = self.pool.get('extraschool.activitycategory')
        config=obj_config.read(cr, uid, [1],['lastqrcodenbr','qrencode','tempfolder','templatesfolder'])[0]         
        month_name=('','Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre')
        day_name=('Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche')
        
        inv_obj = self.pool.get('extraschool.invoice')
        obj_biller = self.pool.get('extraschool.biller')
        obj_invoicedprest = self.pool.get('extraschool.invoicedprestations')
        obj_parent = self.pool.get('extraschool.parent')
        obj_prestation_times_of_the_day = self.pool.get('extraschool.prestation_times_of_the_day')
        
        #a faire: verifier si toutes les prestations sont verifiees
                             
        #get las invoice number
        cr.execute('select max(number) as maxnum from extraschool_invoice')
        invoicefiles=[]
        invoicenum=cr.dictfetchall()[0]['maxnum']
        if invoicenum==None:
            invoicenum=0
        
        #creation of new biller
        activitycatid=form['activitycategory'][0]
        biller_id = obj_biller.create(cr, uid, {'activitycategoryid':form['activitycategory'][0],'period_from':form['period_from'],'period_to':form['period_to'],'payment_term':form['invoice_term'],'invoice_date':form['invoice_date']}, context=context)
        
        for schoolimplantationid in form['schoolimplantationid']:
            #Superb sql query to loop on parents to invoice order by classes
            cr.execute('select distinct(parentid),schoolimplantation,classid,streetcode from extraschool_child left join extraschool_parent on parentid=extraschool_parent.id where schoolimplantation=%s and extraschool_child.id in (select childid from extraschool_prestationtimes where prestation_date >=%s and prestation_date <= %s and activitycategoryid=%s) and extraschool_child.id not in (select childid from extraschool_invoicedprestations left join extraschool_activity on activityid=extraschool_activity.id where prestation_date >=%s and prestation_date <= %s and category=%s) order by classid',(schoolimplantationid,form['period_from'],form['period_to'],form['activitycategory'][0],form['period_from'],form['period_to'],form['activitycategory'][0]))
            parents=cr.dictfetchall()
            for parent in parents:
                toinvoice = False
                #get parameters of activity category
                activitycat=obj_activitycategory.read(cr, uid, [activitycatid],['invoicecomstructprefix','invoicelastcomstruct','invoicetemplate','childpositiondetermination'])[0]
                #get childs of the parent order by birthdate
                cr.execute('select * from extraschool_child where parentid=%s and isdisabled=FALSE order by birthdate',(parent['parentid'],))
                childs=cr.dictfetchall()                
                tmpchilds=[]
                discountamount = 0.0
                for child in childs:                    
                    '''
                    cr.execute('select leveltype from extraschool_level where id=%s',(child['levelid'],))
                    leveltype= cr.dictfetchall()[0]['leveltype']
                    '''
                    #loop on prestas_of_the_days
                    '''
                    cr.execute('select distinct(prestation_date) from extraschool_prestationtimes where childid=%s and prestation_date >=%s and prestation_date <= %s and activitycategoryid=%s and prestation_date not in (select prestation_date from extraschool_invoicedprestations left join extraschool_activity on activityid=extraschool_activity.id where childid=%s and prestation_date >=%s and prestation_date <= %s and category=%s) order by prestation_date',(child['id'],form['period_from'],form['period_to'],form['activitycategory'][0],child['id'],form['period_from'],form['period_to'],form['activitycategory'][0]))
                    prestation_dates=cr.fetchall()
                    '''
                    prestation_times_of_the_day_ids = obj_prestation_times_of_the_day.search(cr,uid,[('child_id.id','=',child['id'])],order = 'date_of_the_day')
                    
                    
                    childactivities = {}
                    for prestation_times_of_the_day in obj_prestation_times_of_the_day.browse(cr,uid,prestation_times_of_the_day_ids):
                        
                        
                        #child position detection to extract in a function
                        if activitycat['childpositiondetermination']=='byaddress':
                            cr.execute('select * from extraschool_child where parentid in (select id from extraschool_parent where streetcode ilike %s) and isdisabled=FALSE order by birthdate',(parent['streetcode'],))
                        elif activitycat['childpositiondetermination']=='byaddresswp':
                            cr.execute('select * from extraschool_child where parentid in (select id from extraschool_parent where streetcode ilike %s) and isdisabled=FALSE and id in (select childid from extraschool_prestationtimes where prestation_date=%s) order by birthdate',(parent['streetcode'],prestation_date))
                        elif activitycat['childpositiondetermination']=='byparent':
                            cr.execute('select * from extraschool_child where parentid=%s and isdisabled=FALSE order by birthdate',(parent['parentid'],))
                        elif activitycat['childpositiondetermination']=='byparentwp':
                            cr.execute('select * from extraschool_child where parentid=%s and isdisabled=FALSE and id in (select childid from extraschool_prestationtimes where prestation_date=%s) order by birthdate',(parent['parentid'],prestation_date))
                        childsforposition=cr.dictfetchall()
                        childpos=1
                        while child['id'] != childsforposition[childpos-1]['id']:
                            childpos = childpos+1
                        
                        
                        
                        totalday=0.0
                        
                        cr.execute('select distinc(occurrenceid) as id from extraschool_prestationtimes where prestation_date=%s and childid=%',(str(prestation_times_of_the_day.date_of_the_day),child['id']))
                        occurrences=cr.dictfetchall()
                        for occurrence in self.pool.get('extraschool.activityoccurrence').browse(cr,uid,[occu['id'] for occu in occurrences]):
                            totalactivity = 0
                            if toinvoice==False:
                                invoicenum=invoicenum+1
                                invoice_id=inv_obj.create(cr, uid, {'filename':'Facture'+str(invoicenum)+'.pdf','schoolimplantationid':schoolimplantationid,'parentid':parent['parentid'],'number':invoicenum,'biller_id':biller_id})
                                total=0
                                totalperiods=0
                                toinvoice = True
                            cr.execute("select sum(prestation_time) from extraschool_prestationstime where childid=%s and occurrenceid=%s where es='E'", (child['id'],occurrence.id))
                            sum_of_entry =cr.fetchall()[0][0] * 60
                            cr.execute("select sum(prestation_time) from extraschool_prestationstime where childid=%s and occurrenceid=%s where es='S'", (child['id'],occurrence.id))
                            sum_of_exit =cr.fetchall()[0][0] * 60
                            quantity=int(ceil((sum_of_exit-sum_of_entry)/occurrence.activity_id.period_duration))
                                                                                                                     
                            if quantity < 0:
                                quantity=0
                            if quantity > 0:
                                activity={}
                                activity['price']=2
                                if (activity['price'] > 0):
                                    totalactivity=totalactivity+(quantity*activity['price'])
                                    totalday=totalday+totalactivity
                                    total=total+(quantity*activity['price'])
                                    totalperiods=totalperiods+quantity                                           
                                    cr.execute('select * from extraschool_invoicedprestations where invoiceid=%s and childid=%s and prestation_date=%s and activityid=%s and placeid=%s',(invoice_id,child['id'],prestation_times_of_the_day.date_of_the_day,activity['id'],occurrence.place_id))
                                    invoicedprestid = cr.dictfetchall()
                                    if invoicedprestid:
                                        objid=obj_invoicedprest.write(cr, uid, [invoicedprestid[0]['id']], {'quantity':(invoicedprestid[0]['quantity']+quantity)})
                                    else:
                                        objid=obj_invoicedprest.create(cr, uid, {'invoiceid':invoice_id,'childid':child['id'],'prestation_date':prestation_times_of_the_day.date_of_the_day,'activityid':activity['id'],'quantity':quantity,'placeid':occurrence.place_id})                                    

                            if str(activity['id']) in childactivities.keys():
                                childactivities[str(activity['id'])]=childactivities[str(activity['id'])]+totalactivity
                            else:
                                childactivities[str(activity['id'])]=totalactivity
                            if str(activity['id']) in daychildactivities.keys():
                                daychildactivities[str(activity['id'])]=daychildactivities[str(activity['id'])]+totalactivity
                            else:
                                daychildactivities[str(activity['id'])]=totalactivity
                        
                        discountamount=discountamount+self.computediscount(cr,uid,child['id'],'by_day',child['childtypeid'],daychildactivities)
                    discountamount=discountamount+self.computediscount(cr,uid,child['id'],'by_invoice',child['childtypeid'],childactivities)        
                    period_from=datetime.datetime.strptime(form['period_from'], '%Y-%m-%d').date()
                    period_to=datetime.datetime.strptime(form['period_to'], '%Y-%m-%d').date()
                    start_month=period_from.month
                    end_months=(period_to.year-period_from.year)*12 + period_to.month+1
                    months=[{'year':yr, 'month':mn} for (yr, mn) in (
                        ((m - 1) / 12 + period_from.year, (m - 1) % 12 + 1) for m in range(start_month, end_months)
                        )]
                    tmpPrestations=[]
                    for month in months:
                        cr.execute('select * from "extraschool_invoicedprestations" left join extraschool_activity on activityid=extraschool_activity.id where "prestation_date">=%s and "prestation_date"<=%s and "childid"=%s order by prestation_date,prest_from', (str(month['year'])+'-'+str(month['month'])+'-01',str(month['year'])+'-'+str(month['month'])+'-'+str(calendar.monthrange(month['year'], month['month'])[1]),child['id']))
                        invoicedprestations = cr.dictfetchall()
                        cr.execute('select * from (select distinct on (short_name) short_name,prest_from from extraschool_activity where id in (select distinct(activityid) from "extraschool_invoicedprestations" where "prestation_date">=%s and "prestation_date"<=%s and "childid"=%s)) foo order by prest_from', (str(month['year'])+'-'+str(month['month'])+'-01',str(month['year'])+'-'+str(month['month'])+'-'+str(calendar.monthrange(month['year'], month['month'])[1]),child['id']))
                        invoicedactivities = cr.dictfetchall()
                        if invoicedprestations:
                            presttab=[]
                            pweeks=[]
                            pdays=None
                            pdays=[]
                            for i in range(0,5):
                                pdays.append([])
                                for i2 in range(0,8):
                                    pdays[i].append('')
                                for invoicedactivity in invoicedactivities:
                                    if len(pdays[i][1]) > 0:
                                        pdays[i][1]=pdays[i][1]+'<br />'
                                    pdays[i][1]=pdays[i][1]+invoicedactivity['short_name']
                                pdays[i][0]=day_name[i]
                            startmonth=datetime.date(month['year'],month['month'],01)
                            startweek=startmonth-datetime.timedelta(startmonth.weekday())
                            if startmonth.weekday() > 4:
                                startweek=startweek+datetime.timedelta(7)
                            endweek=startweek+datetime.timedelta(6)
                            pweeks.append(month_name[month['month']].upper())
                            pweeks.append('')
                            pweeks.append('du '+str(startweek)[8:10]+'/'+str(startweek)[5:7]+'/'+str(startweek)[0:4]+'<br />au '+str(endweek)[8:10]+'/'+str(endweek)[5:7]+'/'+str(endweek)[0:4])                    
                            for iday in range(0,5):
                                if (startweek+datetime.timedelta(iday)).month == month['month']:
                                    for invoicedactivity in invoicedactivities:
                                        qte=0
                                        cr.execute('select sum(quantity) from extraschool_invoicedprestations left join extraschool_activity on activityid=extraschool_activity.id where "prestation_date"=%s and "childid"=%s and short_name=%s', (str(startweek+datetime.timedelta(iday)),child['id'],invoicedactivity['short_name']))
                                        qte=cr.fetchall()[0][0]
                                        if qte > 0: 
                                            pdays[iday][2]=pdays[iday][2]+str(qte)
                                        pdays[iday][2]=pdays[iday][2]+'<br />'   
                                pdays[iday][2]=pdays[iday][2][0:-6]
                            
                            for i in range(3,8):
                                startweek=endweek+datetime.timedelta(1)
                                endweek=startweek+datetime.timedelta(6)
                                for iday in range(0,5):
                                    for invoicedactivity in invoicedactivities:
                                        qte=0
                                        cr.execute('select sum(quantity) from extraschool_invoicedprestations left join extraschool_activity on activityid=extraschool_activity.id where "prestation_date"=%s and "childid"=%s and short_name=%s', (str(startweek+datetime.timedelta(iday)),child['id'],invoicedactivity['short_name']))
                                        qte=cr.fetchall()[0][0]
                                        if qte > 0: 
                                            pdays[iday][i]=pdays[iday][i]+str(qte)
                                        pdays[iday][i]=pdays[iday][i]+'<br />'   
                                    pdays[iday][i]=pdays[iday][i][0:-6]
                                if (startweek.month == month['month']):
                                    pweeks.append('du '+str(startweek)[8:10]+'/'+str(startweek)[5:7]+'/'+str(startweek)[0:4]+'<br />au '+str(endweek)[8:10]+'/'+str(endweek)[5:7]+'/'+str(endweek)[0:4])
                            presttab.append(pweeks)
                            for iday in range(0,5):
                                presttab.append(pdays[iday])                    
                            tmpPrestations.append(presttab)                                                        
                        if child['classid']:
                            cr.execute('select * from "extraschool_class" where id=%s',(str(child['classid']),))
                            classname=cr.dictfetchall()[0]['name']
                        else:
                            classname=''
                        if child['childtypeid']:
                            cr.execute('select * from "extraschool_childtype" where id=%s',(str(child['childtypeid']),))
                            childtype=cr.dictfetchall()[0]['name']
                        else:
                            childtype=''
                    tmpchilds.append({'Lastname':child['lastname'],'Firstname':child['firstname'],'OtherRef':child['otherref'],'Class':classname,'ChildType':childtype,'Prestations':tmpPrestations})
                if toinvoice == True:
                    total = total - discountamount
                    if total <=0:
                        inv_obj.unlink(cr, uid, [invoice_id])
                    else:
                        comstruct=activitycat['invoicecomstructprefix']
                        numstruct=activitycat['invoicelastcomstruct']
                        if numstruct==None:
                            numstruct=1
                        numstruct=numstruct+1
                        nbz=7-len(str(numstruct))
                        for i in range(0,nbz):
                            comstruct=comstruct+'0'
                        comstruct=comstruct+str(numstruct)
                        numverif=str(int(comstruct) % 97)
                        if (int(numverif)==0):
                            numverif='97'
                        if (len(numverif)==1):
                            numverif='0'+numverif
                        comstruct=comstruct+numverif
                        childparent=obj_parent.read(cr, uid, [parent['parentid']],['name','street','zipcode','city','invoicesendmethod'])[0]
                        tmpinvoice={'date':lbutils.strdate(form['invoice_date']),'term':lbutils.strdate(form['invoice_term']),'parentname':childparent['name'],'parentstreet':childparent['street'],'parentzipcode':childparent['zipcode'],'parentcity':childparent['city'],'discount':'%.2f' % round(discountamount, 2),'structcom':comstruct[0:3]+'/'+comstruct[3:7]+'/'+comstruct[7:12],'amount_total':'%.2f' % round(total, 2),'schoolimplantationid':schoolimplantationid,'number':invoicenum,'totalperiods':totalperiods}
                        renderer = appy.pod.renderer.Renderer(config['templatesfolder']+activitycat['invoicetemplate'], {'invoice':tmpinvoice,'childs': tmpchilds}, config['tempfolder']+'fact'+str(invoice_id)+'.pdf')                
                        renderer.run()
                        if (childparent['invoicesendmethod'] == 'emailandmail') or (childparent['invoicesendmethod'] == 'onlybymail'):
                            invoicefiles.append(config['tempfolder']+'fact'+str(invoice_id)+'.pdf')
                        outfile = open(config['tempfolder']+'fact'+str(invoice_id)+'.pdf','r').read()
                        out=base64.b64encode(outfile)
                        objid=inv_obj.write(cr, uid, [invoice_id],{'discount':round(discountamount,2),'structcom':comstruct,'amount_total':round(total,2),'amount_received':0,'balance':round(total,2),'no_value':0,'invoice_file':out})
                        obj_activitycategory.write(cr, uid, [activitycatid],{'invoicelastcomstruct':numstruct})
                    total=0                    
                    toinvoice = False                
                    tmpfacture={}
        
        blank_page = PdfFileReader(file(config['templatesfolder']+'blank.pdf','rb')).pages[0]
        dest = PdfFileWriter()
        for invoicefile in invoicefiles:
            PDF = PdfFileReader(file(invoicefile,'rb'))
            for page in PDF.pages:
                dest.addPage(page)
            os.remove(invoicefile)
            if PDF.numPages % 2: 
                dest.addPage(blank_page)
        outfile = file(config['tempfolder']+"factures.pdf","wb")
        dest.write(outfile)
        outfile.close()
        outfile = open(config['tempfolder']+"factures.pdf","r").read()
        out=base64.b64encode(outfile)
        obj_biller.write(cr, uid, [biller_id],{'filename':'factures.pdf','biller_file':out})
        return {'state':'compute_invoices', 'invoices':out, 'name':'factures.pdf'}
        
    def action_compute_invoices(self, cr, uid, ids, context=None):   
        form = self.read(cr,uid,ids,)[-1] 
        form['schoolimplantationid']=self._schoolimplantationids    
        return self.write(cr, uid, ids, self._compute_invoices(cr, uid, form))


extraschool_invoice_wizard()
