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

class extraschool_activitycategory(models.Model):
    _name = 'extraschool.activitycategory'
    _description = 'Activities categories'
    
    name = fields.Char('Name', size=50)         
    activities = fields.One2many('extraschool.activity', 'category','Activities')               
    placeids = fields.Many2many('extraschool.place','extraschool_activitycategory_place_rel', 'activitycategory_id', 'place_id','Schoolcare place')
    childpositiondetermination = fields.Selection((('byparent','by parent'),('byparentwp','by parent (only childs with prestations)'),('byaddress','by address'),('byaddresswp','by address (only childs with prestations)')),'Child position determination')
    priorityorder = fields.Integer('Priority order')
    invoicetemplate = fields.Char('Invoice Template', size=50, default='facture.odt')        
    invoicecomstructprefix = fields.Char('Invoice Comstruct prefix', size=4)
    invoicelastcomstruct = fields.Integer('Last Invoice structured comunication number')
    invoiceemailaddress = fields.Char('Invoice email address', size=50)
    invoiceemailsubject = fields.Char('Invoice email subject', size=50)
    invoiceemailtext = fields.Text('Invoice email text')        
    remindercomstructprefix = fields.Char('Reminder Comstruct prefix', size=4)
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
    payment_invitation_report_id = fields.Many2one('extraschool.report', 'Payment invitation report')
    payment_invitation_email_subject = fields.Char('Payment invitation Email subject')
    payment_invitation_com_struct_prefix = fields.Char('Payment invitation Comstruct prefix', size=4)
    payment_invitation_courrier_text = fields.Text('Payment invitation courrier text')

    logo = fields.Binary()
    slogan = fields.Char('Slogan', size=50)


    
extraschool_activitycategory()
