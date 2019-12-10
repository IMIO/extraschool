# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchial & Jenny Pans - Imio (<http://www.imio.be>).
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
from openerp.exceptions import Warning, RedirectWarning
import base64
import os
import datetime
import xlsxwriter
from datetime import date, datetime, timedelta as td


class extraschool_subvention_report(models.Model):
    _name = 'extraschool.subvention_report'

    name = fields.Char('Nom', required=True)
    start_date = fields.Date('Start date', required=True)
    end_date = fields.Date('End date', required=True)
    dates_ok = fields.Boolean(default=True)
    activity = fields.Many2many(
        'extraschool.activity',
        'extraschool_activity_activity_subvention_rel',
        'subvention_id',
        'activity_id',
        string='Activity',
        required=True
    )
    title = fields.Selection(
        (('public_power', 'Pouvoir public'),
         ('organisation', 'Organisation de jeunesse reconnue'),
         ('other', 'Autre')),
        default='public_power', string='Title')
    camps_radio = fields.Selection(
        (('holiday_plain', 'Plaine de vacances'),
         ('stays', u'Séjour de vacances'),
         ('holiday_camp', 'Camp de vacances'),
         ('residential_infra', 'uInfrastructures Résidentielles'),
         ('tent', 'Sous tente')),
        default='holiday_plain', string='Stays and camps')

    # todo Vérifier si les deux dates sont entrées (pour le feeling utilisateur)
    @api.onchange('start_date', 'end_date')
    def _check_validity_date(self):
        for record in self:
            if record.end_date < record.start_date:
                record.dates_ok = False
            else:
                record.dates_ok = True

    @api.multi
    def generate_report(self, under_6, over_6, id):
        report = '/tmp/subvention_report' + str(datetime.now()) + '.xls'
        workbook = xlsxwriter.Workbook(report)

        title = workbook.add_format({'bold': True, 'bg_color': '#cccccc', 'font_size': 20, 'border': True})
        bold = workbook.add_format({'bold': True, 'border': True})
        border = workbook.add_format({'border': True})

        # - de 6 ans
        worksheet = workbook.add_worksheet('- 6 ans')
        worksheet.merge_range('A1:E1', "ENFANTS DE - DE 6 ANS", title)
        worksheet.write(1, 0, "Nom", bold)
        worksheet.write(1, 1, u"Prénom", bold)
        worksheet.write(1, 2, "Age", bold)
        worksheet.write(1, 3, "Nombre de jours", bold)
        worksheet.write(1, 4, "Prix", bold)

        row = 2
        total_prestation = total_price = 0

        for child in under_6:
            worksheet.write(row, 0, under_6[child]['lastname'], border)
            worksheet.write(row, 1, under_6[child]['firstname'], border)
            worksheet.write(row, 2, str(under_6[child]['age']) + " ans", border)
            worksheet.write(row, 3, under_6[child]['prestation'], border)
            worksheet.write(row, 4, str(under_6[child]['price']) + "€".decode('utf-8'), border)
            row += 1
            total_prestation += under_6[child]['prestation']
            total_price += under_6[child]['price']
        worksheet.merge_range('A' + str(row + 1) + ':C' + str(row + 1), "Total", bold)
        worksheet.write(row, 3, total_prestation, border)
        worksheet.write(row, 4, str(total_price) + "€".decode('utf-8'), border)

        # + de 6 ans
        worksheet = workbook.add_worksheet('+ 6 ans')
        worksheet.merge_range('A1:E1', "ENFANTS DE + DE 6 ANS", title)
        worksheet.write(1, 0, "Nom", bold)
        worksheet.write(1, 1, u"Prénom", bold)
        worksheet.write(1, 2, "Age", bold)
        worksheet.write(1, 3, "Nombre de jours", bold)
        worksheet.write(1, 4, "Prix", bold)

        row = 2
        total_prestation = total_price = 0

        for child in over_6:
            worksheet.write(row, 0, over_6[child]['lastname'], border)
            worksheet.write(row, 1, over_6[child]['firstname'], border)
            worksheet.write(row, 2, str(over_6[child]['age']) + " ans", border)
            worksheet.write(row, 3, over_6[child]['prestation'], border)
            worksheet.write(row, 4, str(over_6[child]['price']) + "€".decode('utf-8'), border)
            row += 1
            total_prestation += over_6[child]['prestation']
            total_price += over_6[child]['price']
        worksheet.merge_range('A' + str(row + 1) + ':C' + str(row + 1), "Total", bold)
        worksheet.write(row, 3, total_prestation, border)
        worksheet.write(row, 4, str(total_price) + "€".decode('utf-8'), border)

        workbook.close()

        outfile = open(report, "r").read()
        attachment_obj = self.env['ir.attachment']
        attachment_obj.create({'res_model': 'extraschool.subvention_report', 'res_id': id.id,
                               'datas_fname': 'rapport_subvention_' + '.xls',
                               'name': 'rapport_one_' + '.xls',
                               'datas': base64.b64encode(outfile), })
        os.remove(report)

    @api.model
    def create(self, vals):

        if not vals['dates_ok']:
            raise Warning(_("Your dates are not ok. Please Check your dates."))

        under_6 = {}
        over_6 = {}

        prestation_ids = self.env['extraschool.prestationtimes'].search([
            ('prestation_date', '>=', vals.get('start_date')),
            ('prestation_date', '<=', vals.get('end_date')),
            ('activity_occurrence_id.activityid', 'in', tuple(vals.get('activity')[0][2])),
            ('es', '=', 'E'),
        ]).sorted(key=lambda r: (r.childid.lastname))

        for prestation in prestation_ids:
            age = prestation.childid.get_age()
            if age >= 6:
                if prestation.childid.id in over_6:
                    over_6[prestation.childid.id]['prestation'] += 1
                    over_6[prestation.childid.id]['price'] += prestation.invoiced_prestation_id.total_price
                else:
                    over_6[prestation.childid.id] = {'lastname': prestation.childid.lastname.upper(),
                                                     'firstname': prestation.childid.firstname, 'age': age,
                                                     'prestation': 1,
                                                     'price': prestation.invoiced_prestation_id.total_price}
            else:
                if prestation.childid.id in under_6:
                    under_6[prestation.childid.id]['prestation'] += 1
                    under_6[prestation.childid.id]['price'] += prestation.invoiced_prestation_id.total_price
                else:
                    under_6[prestation.childid.id] = {'lastname': prestation.childid.lastname.upper(),
                                                      'firstname': prestation.childid.firstname, 'age': age,
                                                      'prestation': 1,
                                                      'price': prestation.invoiced_prestation_id.total_price}

        id = super(extraschool_subvention_report, self).create(vals)
        self.generate_report(under_6, over_6, id)

        return id
