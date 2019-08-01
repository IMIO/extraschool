# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
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
    dominant_payment_activity_category_id = fields.Many2one('extraschool.activitycategory')

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

    po_rappel_name2 = fields.Char('Name of resp reminder 2')
    po_rappel_fct2 = fields.Char('Fct of resp reminder 2')
    po_rappel_sign2 = fields.Binary('Signature of resp reminder 2')

    logo = fields.Binary()
    logo2 = fields.Binary()
    slogan = fields.Char('Slogan', size=50)

    biller_report_id = fields.Many2one('extraschool.report', 'Biller report')
    qrcode_report_id = fields.Many2one('extraschool.report', string ='QRCode report')
    taxcertificatetemplate = fields.Char('Tax Certificate Template', size=50)
    tax_certificate_code = fields.Char()
