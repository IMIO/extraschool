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
import lbutils
import re

class extraschool_biller(osv.osv):
    _name = 'extraschool.biller'
    _description = 'Biller'

    def deletebiller(self, cr, uid, ids, context=None):             
        obj_biller = self.pool.get('extraschool.biller')        
        res = obj_biller.unlink(cr, uid, ids)        
        return True

    def _compute_total (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            cr.execute('select sum(amount_total) from extraschool_invoice where biller_id=%s',(record.id,))
            to_return[record.id] = cr.fetchall()[0][0]
        return to_return

    def _compute_received (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            cr.execute('select sum(amount_received) from extraschool_invoice where biller_id=%s',(record.id,))
            to_return[record.id] = cr.fetchall()[0][0]
        return to_return
    
    def _compute_balance (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            cr.execute('select sum(balance) from extraschool_invoice where biller_id=%s',(record.id,))
            to_return[record.id] = cr.fetchall()[0][0]
        return to_return
    
    def _compute_novalue (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            cr.execute('select sum(no_value) from extraschool_invoice where biller_id=%s',(record.id,))
            to_return[record.id] = cr.fetchall()[0][0]
        return to_return

    def _compute_nbinvoices (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            cr.execute('select count(id) from extraschool_invoice where biller_id=%s',(record.id,))
            to_return[record.id] = cr.fetchall()[0][0]
        return to_return

    def sendmails(self, cr, uid, ids, context=None):                     
        mail_mail = self.pool.get('mail.mail')
        ir_attachment = self.pool.get('ir.attachment')
        invoice_obj = self.pool.get('extraschool.invoice')
        parent_obj  = self.pool.get('extraschool.parent')
        biller_obj  = self.pool.get('extraschool.biller')
        activitycategory_obj  = self.pool.get('extraschool.activitycategory')
        mail_ids = []
        invoice_ids = invoice_obj.search(cr, uid, [('biller_id','=',ids[0])])
        biller=biller_obj.read(cr, uid, ids,['activitycategoryid'])[0]
        activitycat=activitycategory_obj.read(cr, uid, [biller['activitycategoryid'][0]],['invoiceemailtext','invoiceemailsubject','invoiceemailaddress'])[0]
        for invoice_id in invoice_ids:
            invoice = invoice_obj.read(cr, uid, [invoice_id],['parentid','filename','invoice_file'])[0]            
            parent = parent_obj.read(cr,uid,[invoice['parentid'][0]],['email','invoicesendmethod'])[0]
            if parent['invoicesendmethod'] != 'onlybymail':
                emails = str(parent['email']).split(';')
                for email in emails:
                    email = email.strip()
                    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:                    
                        mail_id = mail_mail.create(cr, uid, {
                            'email_from': activitycat['invoiceemailaddress'],
                            'email_to': email,
                            'subject': activitycat['invoiceemailsubject'],
                            'body_html': '<pre>%s</pre>' % activitycat['invoiceemailtext']}, context=context)
                        attachment_data = {
                            'name': invoice['filename'],
                            'datas_fname': invoice['filename'],
                            'datas': invoice['invoice_file'],
                            'res_model': mail_mail._name,
                            'res_id': mail_id,
                            }
                        attachment_id = ir_attachment.create(cr, uid, attachment_data, context=context)
                        mail_mail.write(cr, uid, mail_id, {'attachment_ids': [(6, 0, [attachment_id])]}, context=context)                    
                        mail_mail.send(cr, uid, [mail_id], context=context)
                        ir_attachment.unlink(cr, uid, [attachment_id])
                        mail_mail.unlink(cr, uid, [mail_id])
        return False

    def _compute_paymentsstats (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):     
            strhtml='<HTML><TABLE border=1 width=80%><TD>Implantation</TD><TD>Nb Factures</TD><TD>Nb Paiements</TD><TD>Total paiements</TD><TD>Total factures</TD></TR>'
            cr.execute("select schoolimplantationid,extraschool_schoolimplantation.name as implantationname,count(extraschool_invoice) as nbinvoices from extraschool_invoice left join extraschool_schoolimplantation on schoolimplantationid=extraschool_schoolimplantation.id where biller_id=%s group by schoolimplantationid,extraschool_schoolimplantation.name", (record.id,))
            schoolimplantations=cr.dictfetchall()
            for schoolimplantation in schoolimplantations:
                cr.execute("select count(extraschool_payment.id) as nbpayments,sum(extraschool_payment.amount) as amount from extraschool_payment left join extraschool_invoice on concernedinvoice=extraschool_invoice.id where biller_id=%s and schoolimplantationid=%s", (record.id,schoolimplantation['schoolimplantationid']))                
                paymentstats=cr.dictfetchall()[0]
                cr.execute("select sum(amount_total) from extraschool_invoice where biller_id=%s and schoolimplantationid=%s", (record.id,schoolimplantation['schoolimplantationid']))                
                totinvoices=cr.fetchall()[0][0]
                strhtml=strhtml+'<TR><TD>'+str(lbutils.genstreetcode(schoolimplantation['implantationname']))+'</TD><TD>'+str(schoolimplantation['nbinvoices'])+'</TD><TD>'+str(paymentstats['nbpayments'])+'</TD><TD>'+str(paymentstats['amount'])+'</TD><TD>'+str(totinvoices)+'</TD></TR>'
            strhtml=strhtml+'</TABLE></HTML>'
            to_return[record.id]=strhtml
        return to_return


    _columns = {
        'name' : fields.char('Name', size=20),
        'activitycategoryid' : fields.many2one('extraschool.activitycategory', 'Activity Category'),
        'period_from' : fields.date('Period from'),
        'period_to' : fields.date('Period to'),
        'payment_term' : fields.date('Payment term'),
        'invoices_date' : fields.date('Invoices date'),        
        'invoice_ids' : fields.one2many('extraschool.invoice', 'biller_id','invoices'),
        'total' : fields.function(_compute_total, method=True, type="float", string="Total"),
        'received' : fields.function(_compute_received, method=True, type="float", string="Received"),
        'novalue' : fields.function(_compute_novalue, method=True, type="float", string="No Value"),
        'balance' : fields.function(_compute_balance, method=True, type="float", string="Balance"),
        'nbinvoices': fields.function(_compute_nbinvoices, method=True, type="integer", string="Nb of invoices"),
        'paymentsstats' : fields.function(_compute_paymentsstats, method=True, type="text", string="Payments stats"),
        'filename' : fields.char('filename', size=20,readonly=True),
        'biller_file' : fields.binary('File', readonly=True),
        'oldid' : fields.integer('oldid'),      
    }
    _defaults = {
        'name' : lambda *a: 'Facturier'
    }
extraschool_biller()

