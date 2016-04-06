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
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschool_activitycategory(models.Model):
    _name = 'extraschool.activitycategory'
    _description = 'Activities categories'
    
    name = fields.Char('Name', size=50)    
    po_name = fields.Char('Name of PO')    
    po_street = fields.Char('Street')
    po_zipcode = fields.Char('ZipCode')
    po_city = fields.Char('City')   
    po_sign = fields.Binary('Signature')
    po_resp_name = fields.Char('Name of resp')
    po_resp_fct = fields.Char('Fct of resp')
    po_resp2_sign = fields.Binary('Signature of resp2')
    po_resp2_name = fields.Char('Name of resp2')
    po_resp2_fct = fields.Char('Fct of resp2')

    po_stamp = fields.Binary('stamp')
    
    po_email = fields.Char('email')
    po_tel = fields.Char('tel')
    po_addresse_free_text = fields.Char('Adresse texte libre')

    
    activities = fields.One2many('extraschool.activity', 'category','Activities')               
    placeids = fields.Many2many('extraschool.place','extraschool_activitycategory_place_rel', 'activitycategory_id', 'place_id','Schoolcare place')
    childpositiondetermination = fields.Selection((('byparent','by parent'),
                                                   ('byparentwp','by parent (only childs with prestations)'),
                                                   ('byparent_nb_childs','by parent (position replaced by nbr childs'),                                                   
                                                   ('byparent_nb_childs_wp','by parent (position replaced by nbr childs with prestations'),                                                   
                                                   ('byaddress','by address'),
                                                   ('byaddresswp','by address (only childs with prestations)'),
                                                   ('byaddress_nb_childs','by address (position replaced by nbr childs'),
                                                   ('byaddress_nb_childs_wp','by address (position replaced by nbr childs with prestations'),
                                                   ),'Child position determination', required = True)
    priorityorder = fields.Integer('Priority order')
    invoicetemplate = fields.Char('Invoice Template', size=50, default='facture.odt')        
    invoicecomstructprefix = fields.Char('Invoice Comstruct prefix', size=3, required = True)
    invoicelastcomstruct = fields.Integer('Last Invoice structured comunication number')
    invoiceemailaddress = fields.Char('Invoice email address', size=50)
    invoiceemailsubject = fields.Char('Invoice email subject', size=50)
    invoiceemailtext = fields.Text('Invoice email text')        
    invoice_comment = fields.Text('Invoice comment')        
    remindercomstructprefix = fields.Char('Reminder Comstruct prefix', size=3, required = True)
    reminderlastcomstruct = fields.Integer('Last Reminder structured comunication number')
    reminderemailaddress = fields.Char('Reminder email address', size=50)
    reminderemailsubject = fields.Char('Reminder email subject', size=50)
    reminderemailtext = fields.Text('Reminder email text')
    bankaccount = fields.Char('Bank account')
    bank_bic = fields.Char('Bank BIC')
    bank_address = fields.Char('Bank address')
    bank_zip = fields.Char('Bank zip')
    bank_city = fields.Char('Bank city')

    taxcertificatetemplate = fields.Char('Tax Certificate Template', size=50)
    invoice_report_id = fields.Many2one('extraschool.report', 'Invoice report')    
    invoice_detail_report_id = fields.Many2one('extraschool.report', 'Invoice detail report')
    biller_report_id = fields.Many2one('extraschool.report', 'Biller report')
    payment_invitation_report_id = fields.Many2one('extraschool.report', 'Payment invitation report')
    payment_invitation_email_subject = fields.Char('Payment invitation Email subject')
    payment_invitation_com_struct_prefix = fields.Char('Payment invitation Comstruct prefix', size=3, required = True)
    payment_invitation_courrier_text = fields.Text('Payment invitation courrier text')

    logo = fields.Binary()
    slogan = fields.Char('Slogan', size=50)


    def check_invoice_prefix(self,invoicecomstructprefix):
        res = {'return_val' : True,
               'msg' : ''}
        # search for activity category that have invoicecomstructprefix = payment_invitation_com_struct_prefix or remindercomstructprefix = payment_invitation_com_struct_prefix
        if len(self.search(['|',('payment_invitation_com_struct_prefix', '=', invoicecomstructprefix), ('remindercomstructprefix', '=', invoicecomstructprefix)])) :
            res = {'return_val' : False,
                   'msg' : "It's not possible to update the activity_categ because there are other activity category with the same prefix used for pre-paid or reminder "}
        if len(self.env['extraschool.payment'].search([('structcom_prefix', '=', invoicecomstructprefix),])) :
            res = {'return_val' : False,
                   'msg' : "It's not possible to update the activity_categ because there are payment with the old invoice prefix"}
        
        return res
    
    def check_pay_invit_prefix(self,payment_invitation_com_struct_prefix):
        res = {'return_val' : True,
               'msg' : ''}
        # search for activity category that have invoicecomstructprefix = payment_invitation_com_struct_prefix or remindercomstructprefix = payment_invitation_com_struct_prefix
        if len(self.search(['|',('invoicecomstructprefix', '=', payment_invitation_com_struct_prefix), ('remindercomstructprefix', '=', payment_invitation_com_struct_prefix)])) :
            res = {'return_val' : False,
                   'msg' : "It's not possible to update the activity_categ because there are other activity category with the same prefix used for invoicing or reminder"}
        if len(self.env['extraschool.payment'].search([('structcom_prefix', '=', payment_invitation_com_struct_prefix),])) :
            res = {'return_val' : False,
                   'msg' : "It's not possible to update the activity_categ because there are payment with the old pre-paid prefix"}            
        return res
    
    def check_reminder_prefix(self,remindercomstructprefix):
        res = {'return_val' : True,
               'msg' : ''}
        # search for activity category that have invoicecomstructprefix = payment_invitation_com_struct_prefix or remindercomstructprefix = payment_invitation_com_struct_prefix
        if len(self.search(['|',('invoicecomstructprefix', '=', remindercomstructprefix), ('payment_invitation_com_struct_prefix', '=', remindercomstructprefix)])) :
            res = {'return_val' : False,
                   'msg' : "It's not possible to update the activity_categ because there are other activity category with the same prefix used for invoicing or pre-paid"}
        if len(self.env['extraschool.payment'].search([('structcom_prefix', '=', remindercomstructprefix),])) :
            res = {'return_val' : False,
                   'msg' : "It's not possible to update the activity_categ because there are payment with the old reminder prefix"}            
        return res
    

            
        return res

    @api.multi
    def write(self, vals):
        print "vals = %s" % (vals)
        for activity_categ in self:
            if 'invoicecomstructprefix' in vals:
                res = activity_categ.check_invoice_prefix(vals['invoicecomstructprefix'])
                if not res['return_val']:
                    raise Warning(res['msg'])
            if 'remindercomstructprefix' in vals:
                res = activity_categ.check_reminder_prefix(vals['remindercomstructprefix'])
                if not res['return_val']:
                    raise Warning(res['msg'])
            if 'payment_invitation_com_struct_prefix' in vals:
                res = activity_categ.check_pay_invit_prefix(vals['payment_invitation_com_struct_prefix'])
                if not res['return_val']:
                    raise Warning(res['msg'])
                                
            super(extraschool_activitycategory,activity_categ).write(vals)
        
        return True
            


    @api.model
    def create(self, vals):  
        res = self.check_pay_invit_prefix(vals['payment_invitation_com_struct_prefix'])
        if not res['return_val']:
            raise Warning(res['msg'])     
        res = self.check_pay_invit_prefix(vals['payment_invitation_com_struct_prefix'])
        if not res['return_val']:
            raise Warning(res['msg'])     
        res = self.check_pay_invit_prefix(vals['payment_invitation_com_struct_prefix'])
        if not res['return_val']:
            raise Warning(res['msg'])     
                                
        res = super(extraschool_activitycategory,self).create(vals)

        return res
    

