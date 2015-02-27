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
import lbutils
from pyPdf import PdfFileWriter, PdfFileReader

class extraschool_remindersjournal(models.Model):
    _name = 'extraschool.remindersjournal'
    _description = 'Reminders journal'

    name = fields.Char('Name', size=80, required=True)
    activitycategoryid = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=True)
    remindertype = fields.Many2one('extraschool.remindertype', 'Reminder type', required=True)
    concernedbillers = fields.Many2many('extraschool.biller','extraschool_remindersjournal_biller_rel', 'remindersjournal_id', 'biller_id','Concerned billers', required=True)
    minamount = fields.Float('Minimum amount', required=True)
    transmissiondate = fields.Date('Transmission date', required=True)
    term = fields.Date('Term', required=True)
    filename = fields.Char('File Name', size=16, readonly=True)
    reminders = fields.Binary('File', readonly=True)
    oldid = fields.Integer('oldid') 
 
    @api.model
    def create(self, vals):
#         obj_config = self.env['extraschool.mainsettings']
#         obj_activitycategory = self.env['extraschool.activitycategory']
#         obj_parent = self.env['extraschool.parent']
#         obj_remindersjournal = self.env['extraschool.remindersjournal']
#         config=obj_config.browse([1])   
#         reminderfiles=[]
#         paymentids = []
#         rejectids = []                
#         activitycategory_obj = self.env['extraschool.activitycategory']
#         invoice_obj = self.env['extraschool.invoice']
#         reminder_obj = self.env['extraschool.reminder']
#         
#         cr.execute("select * from extraschool_invoice where (biller_id in ("+str(vals['concernedbillers'][0][2]).replace('[','').replace(']','').strip()+")) and (balance >= " + str(vals['minamount'])+' and balance <> 0) order by parentid')                
#         invoices = cr.dictfetchall()
#         if len(invoices) > 0:
#             currentparentid=invoices[0]['parentid']
#             currentinvoice=invoices[0]
#             amount=0.0
#             concernedinvoiceids = []
#             remindersjournalid = super(extraschool_remindersjournal, self).create(cr, uid,{'name':vals['name'],'activitycategoryid': vals['activitycategoryid'],'remindertype': vals['remindertype'],'concernedbillers': vals['concernedbillers'],'minamount': vals['minamount'],'transmissiondate': vals['transmissiondate'],'term': vals['term']})
#             for invoice in invoices:
#                 if invoice['parentid'] != currentparentid:
#                     amount=amount+remindertype['fees']
#                     if amount > vals['minamount']:
#                         
#                         activitycat=obj_activitycategory.read(cr, uid, [vals['activitycategoryid']],['remindercomstructprefix','reminderlastcomstruct'])[0]
#                         comstruct=activitycat['remindercomstructprefix']
#                         numstruct=activitycat['reminderlastcomstruct']
#                         if numstruct==None:
#                             numstruct=1
#                         numstruct=numstruct+1
#                         nbz=7-len(str(numstruct))
#                         for i in range(0,nbz):
#                             comstruct=comstruct+'0'
#                         comstruct=comstruct+str(numstruct)
#                         numverif=str(int(comstruct) % 97)
#                         if (int(numverif)==0):
#                             numverif='97'
#                         if (len(numverif)==1):
#                             numverif='0'+numverif
#                         comstruct=comstruct+numverif
#                         reminderid = reminder_obj.create(cr, uid,{'remindersjournalid':remindersjournalid,'parentid':currentparentid,'amount':amount,'structcom':comstruct,'schoolimplantationid':currentinvoice['schoolimplantationid'],'concernedinvoices':[(6,0,concernedinvoiceids)]})
#                         childparent=obj_parent.read(cr, uid, [currentinvoice['parentid']],['name','street','zipcode','city','remindersendmethod'])[0]
#                         cr.execute("select number,to_char(payment_term,'DD/MM/YYYY') as term, balance,period_from,period_to from extraschool_invoice left join extraschool_biller on extraschool_invoice.biller_id = extraschool_biller.id where extraschool_invoice.id in (select invoice_id from extraschool_reminder_invoice_rel where reminder_id=%s)  order by payment_term",(reminderid,))
#                         concernedinvoices=cr.dictfetchall()
#                         tmpreminder={'name':vals['name'],'date':lbutils.strdate(vals['transmissiondate']),'term':lbutils.strdate(vals['term']),'parentname':childparent['name'],'parentstreet':childparent['street'],'parentzipcode':childparent['zipcode'],'parentcity':childparent['city'],'structcom':comstruct[0:3]+'/'+comstruct[3:7]+'/'+comstruct[7:12],'amount':'%.2f' % round(amount, 2),'fees': '%.2f' % round(remindertype['fees'],2),'schoolimplantationid':currentinvoice['schoolimplantationid']}
#                         renderer = appy.pod.renderer.Renderer(config['templatesfolder']+remindertype['template'], {'reminder':tmpreminder,'invoices': concernedinvoices}, config['tempfolder']+'rem'+str(reminderid)+'.pdf')                
#                         renderer.run()
#                         
#                         outfile = open(config['tempfolder']+'rem'+str(reminderid)+'.pdf','r').read()
#                         out=base64.b64encode(outfile)
#                         objid=reminder_obj.write(cr, uid, [reminderid],{'filename':'rem'+str(reminderid)+'.pdf','reminder_file':out})
#                         obj_activitycategory.write(cr, uid, [vals['activitycategoryid']],{'reminderlastcomstruct':numstruct})
#                         if (childparent['remindersendmethod'] == 'emailandmail') or (childparent['remindersendmethod'] == 'onlybymail'):
#                             reminderfiles.append(config['tempfolder']+'rem'+str(reminderid)+'.pdf')
#                         else:
#                             os.remove(config['tempfolder']+'rem'+str(reminderid)+'.pdf')
#                     currentparentid=invoice['parentid']
#                     amount=0.0
#                     concernedinvoiceids = []
#                 amount=amount+invoice['balance']                
#                 concernedinvoiceids.append(invoice['id'])
#                 currentinvoice=invoice
#             amount=amount+remindertype['fees']
#             if amount > vals['minamount']:
#                 activitycat=obj_activitycategory.read(cr, uid, [vals['activitycategoryid']],['remindercomstructprefix','reminderlastcomstruct'])[0]
#                 comstruct=activitycat['remindercomstructprefix']
#                 numstruct=activitycat['reminderlastcomstruct']
#                 if numstruct==None:
#                     numstruct=1
#                 numstruct=numstruct+1
#                 nbz=7-len(str(numstruct))
#                 for i in range(0,nbz):
#                     comstruct=comstruct+'0'
#                 comstruct=comstruct+str(numstruct)
#                 numverif=str(int(comstruct) % 97)
#                 if (int(numverif)==0):
#                     numverif='97'
#                 if (len(numverif)==1):
#                     numverif='0'+numverif
#                 comstruct=comstruct+numverif
#                 reminderid = reminder_obj.create(cr, uid,{'remindersjournalid':remindersjournalid,'parentid':currentparentid,'amount':amount,'structcom':comstruct,'schoolimplantationid':invoice['schoolimplantationid'],'concernedinvoices':[(6,0,concernedinvoiceids)]})
#                 childparent=obj_parent.read(cr, uid, [invoice['parentid']],['name','street','zipcode','city','remindersendmethod'])[0]
#                 cr.execute("select number,to_char(payment_term,'DD/MM/YYYY') as term, balance,period_from,period_to from extraschool_invoice left join extraschool_biller on extraschool_invoice.biller_id = extraschool_biller.id where extraschool_invoice.id in (select invoice_id from extraschool_reminder_invoice_rel where reminder_id=%s) order by payment_term",(reminderid,))
#                 concernedinvoices=cr.dictfetchall()
#                 tmpreminder={'name':vals['name'],'date':lbutils.strdate(vals['transmissiondate']),'term':lbutils.strdate(vals['term']),'parentname':childparent['name'],'parentstreet':childparent['street'],'parentzipcode':childparent['zipcode'],'parentcity':childparent['city'],'structcom':comstruct[0:3]+'/'+comstruct[3:7]+'/'+comstruct[7:12],'amount':'%.2f' % round(amount, 2),'fees': '%.2f' % round(remindertype['fees'],2),'schoolimplantationid':invoice['schoolimplantationid']}                
#                 renderer = appy.pod.renderer.Renderer(config['templatesfolder']+remindertype['template'], {'reminder':tmpreminder,'invoices': concernedinvoices}, config['tempfolder']+'rem'+str(reminderid)+'.pdf')                
#                 renderer.run()
#                 outfile = open(config['tempfolder']+'rem'+str(reminderid)+'.pdf','r').read()
#                 out=base64.b64encode(outfile)
#                 objid=reminder_obj.write(cr, uid, [reminderid],{'filename':'rem'+str(reminderid)+'.pdf','reminder_file':out})
#                 obj_activitycategory.write(cr, uid, [vals['activitycategoryid']],{'reminderlastcomstruct':numstruct})
#                 if (childparent['remindersendmethod'] == 'emailandmail') or (childparent['remindersendmethod'] == 'onlybymail'):
#                     reminderfiles.append(config['tempfolder']+'rem'+str(reminderid)+'.pdf')
#                 else:
#                     os.remove(config['tempfolder']+'rem'+str(reminderid)+'.pdf')
#             blank_page = PdfFileReader(file(config['templatesfolder']+'blank.pdf','rb')).pages[0]
#             dest = PdfFileWriter()
#             for reminderfile in reminderfiles:
#                 PDF = PdfFileReader(file(reminderfile,'rb'))
#                 for page in PDF.pages:
#                     dest.addPage(page)
#                 os.remove(reminderfile)
#                 if PDF.numPages % 2: 
#                     dest.addPage(blank_page)
#             outfile = file(config['tempfolder']+"reminders.pdf","wb")
#             dest.write(outfile)
#             outfile.close()
#             outfile = open(config['tempfolder']+"reminders.pdf","r").read()
#             out=base64.b64encode(outfile)
#             obj_remindersjournal.write(cr, uid, [remindersjournalid],{'filename':'reminders.pdf','reminders':out})
#             return remindersjournalid
#         else:
#             return False
        #to do refactoring new report
        return True
        
extraschool_remindersjournal()


        
