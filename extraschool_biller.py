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

from openerp import models, api, fields, _, SUPERUSER_ID
from openerp.api import Environment
import lbutils
import re
from datetime import date, datetime, timedelta as td
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
from openerp.exceptions import except_orm, Warning, RedirectWarning
import threading

import base64
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
    
import time
    

class extraschool_biller(models.Model):
    _name = 'extraschool.biller'
    _description = 'Biller'
    _inherit = 'mail.thread'

    _order = "id desc"

    def _get_activity_category_id(self):
        return self.env['extraschool.activitycategory'].search([]).filtered('id').id

    activitycategoryid = fields.Many2one('extraschool.activitycategory', 'Activity Category', track_visibility='onchange', default=_get_activity_category_id)
    period_from = fields.Date('Period from')
    period_to = fields.Date('Period to')
    payment_term = fields.Date('Payment term')
    invoices_date = fields.Date('Invoices date')        
    invoice_ids = fields.One2many('extraschool.invoice', 'biller_id','invoices')
    total = fields.Float(compute='_compute_total', string="Total", track_visibility='onchange')
    received = fields.Float(compute='_compute_received', string="Received", track_visibility='onchange')
    novalue = fields.Float(compute='_compute_novalue', string="No Value", track_visibility='onchange')
    balance = fields.Float(compute='_compute_balance', string="Balance", track_visibility='onchange')
    nbinvoices = fields.Integer(compute='_compute_nbinvoices', string="Nb of invoices", track_visibility='onchange')
    other_ref = fields.Char("Ref")
    comment = fields.Text("Comment",default="")
#    paymentsstats = fields.Text(compute='_compute_paymentsstats', string="Payments stats")
    filename = fields.Char('filename', size=20,readonly=True)
    biller_file = fields.Binary('File', readonly=True)
    pdf_ready = fields.Boolean(string="Pdf ready", default=False)
    oldid = fields.Integer('oldid')

    @api.multi
    def biller_refactor(self):
        cr = self.env.cr
        print ("Récupération des Prestation Times contenant des NULL.")
        cr.execute("SELECT DISTINCT(ep.prestation_times_of_the_day_id) "
                   "FROM extraschool_prestationtimes AS ep "
                   "WHERE prestation_date BETWEEN '2017-01-01' AND '2017-03-31' "
                   "AND invoiced_prestation_id IS NULL;"
                   )
        pod = cr.fetchall()

        arg = []

        for prestation_time_delete in pod:
            prestation_time_check = self.env['extraschool.prestationtimes'].search([
                                                                  ('prestation_times_of_the_day_id', 'in', prestation_time_delete),
                                                                  ('invoiced_prestation_id', '!=', 'Null')
                                                                  ])
            if prestation_time_check:
                to_delete = self.env['extraschool.prestationtimes'].search([
                                                                  ('prestation_times_of_the_day_id', 'in', prestation_time_delete),
                                                                  ('invoiced_prestation_id', '=', 'Null')
                                                                  ])
                print ("Suppression des Prestations: %s" % (to_delete))
                arg.append(to_delete.ids)

        self.env['extraschool.prestationtimes'].search(['id', 'in', arg]).unlink(True)

    @api.multi
    def name_get(self):            
        res=[]
        for biller in self:
            res.append((biller.id, _("Biller from %s to %s") % (datetime.strptime(biller.period_from, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y"), datetime.strptime(biller.period_to, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y"))))    

        return res   
        
    @api.depends('invoice_ids.amount_total')
    def _compute_total(self):
        for record in self:
            record.total = sum(invoice.amount_total for invoice in record.invoice_ids)
            
    @api.depends('invoice_ids.amount_received')
    def _compute_received(self):
        for record in self:
            record.received = sum(invoice.amount_received for invoice in record.invoice_ids)
            
    @api.depends('invoice_ids.balance')
    def _compute_balance(self):
        for record in self:
            record.balance = sum(invoice.balance for invoice in record.invoice_ids)
    
    @api.depends('invoice_ids.no_value')
    def _compute_novalue(self):
        for record in self:
            record.novalue = sum(invoice.no_value for invoice in record.invoice_ids)

    @api.depends('invoice_ids')
    def _compute_nbinvoices(self):
        for record in self:
            record.nbinvoices = len(self.invoice_ids)

#     @api.depends('invoice_ids')
#     def _compute_paymentsstats(self):
#         #to do check if it's not possible to use tree view on field invoice_ids
#         cr, uid = self.env.cr, self.env.user.id
# 
#         for record in self:     
#             strhtml='<HTML><TABLE border=1 width=80%><TD>Implantation</TD><TD>Nb Factures</TD><TD>Nb Paiements</TD><TD>Total paiements</TD><TD>Total factures</TD></TR>'
#             cr.execute("select schoolimplantationid,extraschool_schoolimplantation.name as implantationname,count(extraschool_invoice) as nbinvoices from extraschool_invoice left join extraschool_schoolimplantation on schoolimplantationid=extraschool_schoolimplantation.id where biller_id=%s group by schoolimplantationid,extraschool_schoolimplantation.name", (record.id,))
#             schoolimplantations=cr.dictfetchall()
#             for schoolimplantation in schoolimplantations:
#                 cr.execute("select count(extraschool_payment.id) as nbpayments,sum(extraschool_payment.amount) as amount from extraschool_payment left join extraschool_invoice on concernedinvoice=extraschool_invoice.id where biller_id=%s and schoolimplantationid=%s", (record.id,schoolimplantation['schoolimplantationid']))                
#                 paymentstats=cr.dictfetchall()[0]
#                 cr.execute("select sum(amount_total) from extraschool_invoice where biller_id=%s and schoolimplantationid=%s", (record.id,schoolimplantation['schoolimplantationid']))                
#                 totinvoices=cr.fetchall()[0][0]
#                 strhtml=strhtml+'<TR><TD>'+str(lbutils.genstreetcode(schoolimplantation['implantationname']))+'</TD><TD>'+str(schoolimplantation['nbinvoices'])+'</TD><TD>'+str(paymentstats['nbpayments'])+'</TD><TD>'+str(paymentstats['amount'])+'</TD><TD>'+str(totinvoices)+'</TD></TR>'
#             strhtml=strhtml+'</TABLE></HTML>'
# 
#             record.paymentsstats=strhtml

    @api.multi
    def unlink(self):          
        if len(self) > 1:
            raise Warning(_("You can delete only one biller at a time !!!"))  
              
        if self.search([]).sorted(key=lambda r: r.id)[-1].id != self.id:
            raise Warning(_("You can only delete the last biller !!!"))
        
        for invoice in self.invoice_ids:
            invoice.payment_ids.unlink()
        
        invoicelastcomstruct = str(self.invoice_ids.sorted(key=lambda r: r.id)[0].number)[-5:]
        
        self.activitycategoryid.sequence_ids.search([('type', '=', 'invoice'),
                                                     ('year', '=', self.get_from_year()),]).sequence.number_next = invoicelastcomstruct
        
        
           
             
        return super(extraschool_biller, self).unlink()   
           
    @api.one        
    def sendmails(self):  
        #to do refactoring et netoyage suite au passage api V8                   
        cr, uid = self.env.cr, self.env.user.id             
        ids = [self.id]   
        
        mail_mail = self.env['mail.mail']
        ir_attachment = self.env['ir.attachment']
        invoice_obj = self.env['extraschool.invoice']
        parent_obj  = self.env['extraschool.parent']
        biller_obj  = self.env['extraschool.biller']
        activitycategory_obj  = self.env['extraschool.activitycategory']
        invoice_ids = self.invoice_ids.ids
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
                            'body_html': '<pre>%s</pre>' % activitycat['invoiceemailtext']})
                        attachment_data = {
                            'name': invoice['filename'],
                            'datas_fname': invoice['filename'],
                            'datas': invoice['invoice_file'],
                            'res_model': mail_mail._name,
                            'res_id': mail_id,
                            }
                        attachment_id = ir_attachment.create(cr, uid, attachment_data)
                        mail_mail.write(cr, uid, mail_id, {'attachment_ids': [(6, 0, [attachment_id])]})                    
                        mail_mail.send(cr, uid, [mail_id])
                        ir_attachment.unlink(cr, uid, [attachment_id])
                        mail_mail.unlink(cr, uid, [mail_id])
        return False
    
    @api.multi
    def mail_invoices(self): 

        return {'name': 'Invoices',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,     
                'target': 'current',
                'limit': 50000,                                    
                'domain': [('biller_id.id', '=',self.id),
                           '|',('invoicesendmethod','=','onlybymail'),('invoicesendmethod','=','emailandmail')]
            }  

    @api.multi
    def email_invoices(self):         

        return {'name': 'Invoices',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,     
                'target': 'current',
                'limit': 50000,                 
                'domain': [('biller_id.id', '=',self.id),
                           '|',('invoicesendmethod','=','onlyemail'),('invoicesendmethod','=','emailandmail')],
                'context': {"search_default_actif":1},

            }          

    @api.multi
    def all_invoices(self): 

        return {'name': 'Invoices',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,     
                'target': 'current',
                'limit': 50000,                                    
                'domain': [('biller_id.id', '=',self.id)],
                'context': {"search_default_actif":1},
            }           
                        
    @api.multi
    def all_pdf(self): 
 
        return {'name': 'Docs',
                'type': 'ir.actions.act_window',
                'res_model': 'ir.attachment',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,     
                'target': 'current',
                'limit': 50000,                                    
                'domain': [('res_id', 'in',[i.id for i in self.invoice_ids]),
                            ('res_model', '=', 'extraschool.invoice')],
                'context': {"search_default_actif":1},

            }           

    def get_concerned_months(self):
        start_month = fields.Date.from_string(self.period_from).month
        end_months=(fields.Date.from_string(self.period_to).year-fields.Date.from_string(self.period_from).year)*12 + fields.Date.from_string(self.period_to).month+1
        months=[{'year':yr, 'month':mn} for (yr, mn) in (
            ((m - 1) / 12 + fields.Date.from_string(self.period_from).year, (m - 1) % 12 + 1) for m in range(start_month, end_months)
            )]      
        
        return months  
    
    @api.multi
    def get_from_year(self):
        return fields.Date.from_string(self.period_from).year
    
    @api.model
    def generate_pdf_thread(self, cr, uid, thread_lock, invoices_ids, context=None):
        """
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: List of IDs selected
        @param context: A standard dictionary
        """
        time.sleep(5)
        with Environment.manage():
#             print "******"
#             print invoices_ids
#             print "******"
            #As this function is in a new thread, i need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            new_env = Environment(new_cr, uid,context)
            count = 0
            report = new_env['report']
            for invoice in new_env['extraschool.invoice'].browse(invoices_ids):
                count = count + 1
                print "generate pdf %s count: %s" % (invoice.id, count)
                report.get_pdf(invoice ,'extraschool.invoice_report_layout')
          
                        
            thread_lock[1].acquire()
#             print "nbr_thread : %s" % (thread_lock[0])
            thread_lock[0] -= 1
            if thread_lock[0] == 0:
#                 print "this is the end"

#                 post_vars = {'subject': "Print Ready ;-)",
#                              'body': "You print is ready !",
#                              'partner_ids': [(uid)],} 
#                user = env['res.users'].browse(uid)
#                 print "Set biller pdf ready"
                new_env['extraschool.biller'].browse(thread_lock[2]).pdf_ready = True
                #print "update extraschool_biller set pdf_ready = True where id = %s" % (thread_lock[2])
                #new_cr.execute("update extraschool_biller set pdf_ready = True where id = %s",[thread_lock[2]])
                #env['res.partner'].message_post(new_cr, SUPERUSER_ID, False,context, **post_vars)                        
#                env.user.notify_info('My information message')

            thread_lock[1].release()                 
            new_cr.commit()     
            new_cr.close()
            return {}
    
    @api.one
    def generate_pdf(self):    
#         print "pinr invoices from biller : %s" % self.name_get()
#         print self.invoice_ids
#         print "---------------"
        cr,uid = self.env.cr, self.env.user.id 
        threaded_report = []
#        cr.execute("update extraschool_biller set pdf_ready = False where id = %s",[self.id])
#        cr.commit() 
        self.env['ir.attachment'].search([('res_id', 'in',[i.id for i in self.invoice_ids]),
                                           ('res_model', '=', 'extraschool.invoice')]).unlink()
        self.pdf_ready = False
        self.env.invalidate_all()
        
        lock = threading.Lock()
        chunk_size = int(self.env['ir.config_parameter'].get_param('extraschool.report.thread.chunk',200))
#         print "-------------------------------"
#         print "chunk_size:%s" % (chunk_size)
#         print "-------------------------------"
        
        nrb_thread = len(self.invoice_ids)/chunk_size+(len(self.invoice_ids)%chunk_size > 0)
        thread_lock = [len(self.invoice_ids)/chunk_size+(len(self.invoice_ids)%chunk_size > 0),
                        threading.Lock(),
                        self.id]
        for zz in range(0, nrb_thread):
            sub_invoices = [i.id for i in self.invoice_ids[zz*chunk_size:(zz+1)*chunk_size]]
            print "start thread for ids : %s" % (sub_invoices)
            if len(sub_invoices):
                thread = threading.Thread(target=self.generate_pdf_thread, args=(cr, uid, thread_lock, sub_invoices,self.env.context))
                threaded_report.append(thread)
                thread.start()
                        
    @api.one
    def export_onyx(self):
        output = ""
        line = ""
        output += u"MATRICULE\tNom du Responsable\tPrénom du Responsable\tCode rue\tLibellé rue\t"
        output += u"Numéro\tBoîte\tIndex\tCode postal\tLocalité\tPays\tLangue du redevable\tCivilité\tCode rue\tLibellé rue\t"
        output += u"Numéro\tBoîte\tIndex\tCode postal\tLocalité\tDate debut\tdate fin\tCommentaires\tsepar\tN fact\tN°\tM/P\t"
        output += u"NOM\tPRENOM\tDATE DE NAISSANCE\tN° REGISTRE NATIONAL\tANNEE D'ETUDE\tDate accueil\t"
        output += u"activité\tNbr j presences\tfisc\ttotal\n"
        total = 0
        for invoice in self.invoice_ids:            
            export = invoice.export_onyx()
            total += export['exported_amount']
            for r in export['lines']:
                output += "%s\n" % (r)
                
            
        attachment_obj = self.env['ir.attachment']
        filename = "Facturier_du_%s_au_%s__%s_aes_onyx.txt" % (time.strftime('%d/%m/%Y',time.strptime(self.period_from,'%Y-%m-%d')),time.strftime('%d/%m/%Y',time.strptime(self.period_to,'%Y-%m-%d')),total)
        attachment_obj.create({'res_model':'extraschool.biller',
                               'res_id':self.id,
                               'datas' : output.encode('utf-8').encode('base64'),
                               'datas_fname': filename,
                               'name': filename,
                                })    
        
    @api.one
    def compute_discount(self):
        print "------------------"
        print self
        print "------------------"
        for discount in self.env['extraschool.discount.version'].search([]):
            print "++++++++"
            print "%s - %s" %(discount, discount.name)
            discount.discount_forfait_week(self)

    @api.multi
    def pay_all(self):
        print "# Pay All initiated..."
        print "## %s to pay" % (len(self.invoice_ids))
        count = 0
        for invoice_id in self.invoice_ids:
            count += 1
            print "### [%s/%s]" % (count, len(self.invoice_ids))
            payment_id = self.env['extraschool.payment'].create({'parent_id': invoice_id.parentid.id,
                            'paymentdate': self.period_to,# This is Coda date.
                            'structcom_prefix': self.activitycategoryid.payment_invitation_com_struct_prefix,
                            'amount': invoice_id.amount_total,
                            'reject_id': False,
                            'comment': 'Paiement automatique'})

            reconciliation = self.env['extraschool.payment_reconciliation'].create({ 'payment_id' : payment_id.id,
                                                                    'invoice_id' : invoice_id.id,
                                                                    'amount' : invoice_id.amount_total,
                                                                    'date' : self.period_to})
            reconciliation.invoice_id._compute_balance()

        print "### FIN DES PAIEMENTS ###"