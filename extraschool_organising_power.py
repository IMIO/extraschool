# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia - Imio (<http://www.imio.be>).
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

from openerp import models, api, fields, _

class extraschool_organising_power(models.Model):
    _name = 'extraschool.organising_power'
    _description = 'Organising Power that contains all activities'

    activity_category_ids = fields.One2many('extraschool.activitycategory', 'organising_power_id', 'Activity Category')
    town = fields.Char('Name of the town', required=True)
    max_school_implantation = fields.Integer()
    dominant_activity_category_id = fields.Many2one('extraschool.activitycategory')

    po_name = fields.Char('Name of PO')
    po_street = fields.Char('Street')
    po_zipcode = fields.Char('ZipCode')
    po_city = fields.Char('City')
    po_sign = fields.Binary('Signature')

    po_attestation_name = fields.Char('Name of resp tax certificate')
    po_attestation_fct = fields.Char('Fct of resp tax certificate')
    po_attestation_sign = fields.Binary('Signature of resp tax certificate')

    po_email = fields.Char('email')
    po_tel = fields.Char('tel')
    po_addresse_free_text = fields.Char('Adresse texte libre')
    po_addresse_free_text2 = fields.Char('Adresse texte libre 2')

    po_stamp = fields.Binary('stamp')
    po_sign_img = fields.Binary('Signature image')

    po_resp_name = fields.Char('Name of resp')
    po_resp_fct = fields.Char('Fct of resp')
    po_resp2_sign = fields.Binary('Signature of resp2')
    po_resp2_name = fields.Char('Name of resp2')
    po_resp2_fct = fields.Char('Fct of resp2')

    po_rappel_name = fields.Char('Name of resp reminder')
    po_rappel_fct = fields.Char('Fct of resp reminder')
    po_rappel_sign = fields.Binary('Signature of resp reminder')

    logo = fields.Binary()
    slogan = fields.Char('Slogan', size=50)

    biller_report_id = fields.Many2one('extraschool.report', 'Biller report')
    qrcode_report_id = fields.Many2one('extraschool.report', string ='QRCode report')
    taxcertificatetemplate = fields.Char('Tax Certificate Template', size=50)

    @api.model
    def reprise_signaletic(self):
        activity_category = self.env['extraschool.activitycategory'].search([])[0]

        self.env['extraschool.organising_power'].search([])[0].write({
            'po_name': activity_category.po_name,
            'po_street': activity_category.po_street,
            'po_email': activity_category.po_email,
            'po_zipcode': activity_category.po_zipcode,
            'po_city': activity_category.po_city,
            'po_sign': activity_category.po_sign,
            'po_stamp': activity_category.po_stamp,
            'po_tel': activity_category.po_tel,
            'po_addresse_free_text': activity_category.po_addresse_free_text,
            'po_addresse_free_text2': activity_category.po_addresse_free_text2,
            'po_resp_name': activity_category.po_resp_name,
            'po_resp_fct': activity_category.po_resp_fct,
            'po_sign_img': activity_category.po_sign_img,
            'po_resp2_name': activity_category.po_resp2_name,
            'po_resp2_fct': activity_category.po_resp2_fct,
            'po_resp2_sign': activity_category.po_resp2_sign,
            'po_rappel_name': activity_category.po_rappel_name,
            'po_rappel_fct': activity_category.po_rappel_fct,
            'po_rappel_sign': activity_category.po_rappel_sign,
            'po_attestation_name': activity_category.po_attestation_name,
            'po_attestation_fct': activity_category.po_attestation_fct,
            'po_attestation_sign': activity_category.po_attestation_sign,
            'logo': activity_category.logo,
            'slogan': activity_category.slogan,
        })
