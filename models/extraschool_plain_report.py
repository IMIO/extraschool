# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia & Jenny Pans - Imio (<http://www.imio.be>).
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
from datetime import datetime
from docxtpl import DocxTemplate


class extraschool_plain_report(models.Model):
    _name = 'extraschool.plain_report'
    _description = 'Plain report'

    # todo filtrer les activités en fonction des centres
    # def _get__id(self):
    #     return self.env['extraschool.schoolimplantation'].search([])[0].filtered('id')

    name = fields.Char('Nom', required=True)
    start_date = fields.Date('Start date', required=True)
    end_date = fields.Date('End date', required=True)
    dates_ok = fields.Boolean(default=True)
    dates_warning = fields.Boolean(default=False)
    activity_ids = fields.Many2many(
        'extraschool.activity',
        'extraschool_activity_activity_plain_rel',
        'plain_report_id',
        'plain_activity_id',
        string='Activity',
        required=True)
    title = fields.Selection(
        (('public_power', 'Pouvoir public'),
         ('organisation', 'Organisation de jeunesse reconnue'),
         ('other', 'Autre')),
        default='public_power', string='Title')
    camps_radio = fields.Selection(
        (('holiday_plain', 'Plaine de vacances'),
         ('stays', u'Séjour de vacances'),
         ('holiday_camp', 'Camp de vacances'),
         ('residential_infra', 'Infrastructures Résidentielles'),
         ('tent', 'Sous tente')),
        default='holiday_plain', string='Stays and camps')
    center = fields.Many2one('extraschool.place', 'Implantation scolaire', required=True, domain="[('active', '=', 'True')]")
    guardian = fields.Many2one('extraschool.guardian', 'Accueillante', required=True, domain="[('isdisabled', '=', 'False')]")

    @api.onchange('start_date', 'end_date')
    @api.multi
    def _check_validity_date(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.end_date < record.start_date:
                    record.dates_ok = False
                    record.dates_warning = True
                else:
                    record.dates_ok = True
                    record.dates_warning = False

    @api.multi
    def _generate_subvention_request(self, tags, vals):

        tags['id_sub'] = ''
        organising_power = self.env['extraschool.organising_power'].search([])
        tags['po_denomination'] = organising_power['po_name'] or ''

        tags[vals.get('title')] = ' ' or ''
        tags[vals.get('camps_radio')] = ' '

        tags['po_adress'] = organising_power['po_street'] or ''
        tags['po_postal_code'] = organising_power['po_zipcode'] or ''
        tags['po_city'] = organising_power['po_city'] or ''
        tags['po_tel'] = organising_power['po_tel'] or ''
        tags['po_fax'] = organising_power['po_fax'] or ''
        tags['po_mail'] = organising_power['po_email'] or ''

        place = self.env['extraschool.place'].browse(vals['center'])
        tags['center_name'] = place.name or ''
        tags['center_adress'] = place.street_code + ' ' + place.street or ''
        tags['center_postalcode'] = place.zipcode or ''
        tags['center_city'] = place.city or ''
        tags['center_tel'] = place.tel or ''
        tags['center_fax'] = place.fax or ''
        tags['center_mail'] = place.email or ''

        tags['co_firstname'] = ''
        tags['co_lastname'] = ''
        tags['co_function'] = ''
        tags['cf_nb'] = ''
        tags['cf_holder'] = ''
        tags['cf_adress'] = ''
        tags['cf_postal_code'] = ''
        tags['cf_city'] = ''

        return tags

    @api.multi
    def _generate_summary(self, tags, vals):
        return tags

    @api.multi
    def _generate_childs_list(self, tags, prestation_ids, vals):
        under_6 = {}
        over_6 = {}
        tags['under_6'] = []
        tags['over_6'] = []
        nb_under_6 = 0
        nb_over_6 = 0

        # todo simplifier l'algorithme et également dans le rapport ONE
        for prestation in prestation_ids:
            age = prestation.childid.get_age()
            if age >= 6:
                if prestation.childid.id in over_6:
                    over_6[prestation.childid.id]['prestation'] += 1
                    over_6[prestation.childid.id]['price'] += prestation.invoiced_prestation_id.total_price
                else:
                    nb_over_6 += 1
                    over_6[prestation.childid.id] = {'lastname': prestation.childid.lastname.upper(),
                                                     'firstname': prestation.childid.firstname, 'age': age,
                                                     'prestation': 1,
                                                     'price': prestation.invoiced_prestation_id.total_price,
                                                     'nb' : nb_over_6}

                    if prestation.childid.health_sheet_ids:
                        health_sheet = prestation.childid.health_sheet_ids[0]
                        if health_sheet.handicap:
                            if health_sheet.level_handicap == 'mild':
                                over_6[prestation.childid.id]['mild'] = 'X'
                            else:
                                over_6[prestation.childid.id]['heavy'] = 'X'

                    if prestation.childid.disadvantaged:
                        over_6[prestation.childid.id]['disadvantaged'] = 'X'

                    tags['over_6'].append(over_6[prestation.childid.id])
            else:
                if prestation.childid.id in under_6:
                    under_6[prestation.childid.id]['prestation'] += 1
                    under_6[prestation.childid.id]['price'] += prestation.invoiced_prestation_id.total_price
                else:
                    nb_under_6 += 1
                    under_6[prestation.childid.id] = {'lastname': prestation.childid.lastname.upper(),
                                                      'firstname': prestation.childid.firstname, 'age': age,
                                                      'prestation': 1,
                                                      'price': prestation.invoiced_prestation_id.total_price,
                                                      'nb' : nb_under_6}

                    if prestation.childid.health_sheet_ids:
                        health_sheet = prestation.childid.health_sheet_ids[0]
                        if health_sheet.handicap:
                            if health_sheet.level_handicap == 'mild':
                                under_6[prestation.childid.id]['mild'] = 'X'
                            else:
                                under_6[prestation.childid.id]['heavy'] = 'X'

                    if prestation.childid.disadvantaged:
                        under_6[prestation.childid.id]['disadvantaged'] = 'X'

                    tags['under_6'].append(under_6[prestation.childid.id])

        tags['under_total'] = nb_under_6
        tags['over_total'] = nb_over_6
        return tags


    @api.multi
    def _generate_supervisors(self, tags, vals):
        return tags


    @api.multi
    def _generate_prestation_times(self, tags, vals):
        return tags


    @api.multi
    def _generate_context(self, vals):
        prestation_ids = self.env['extraschool.prestationtimes'].search([
            ('prestation_date', '>=', vals.get('start_date')),
            ('prestation_date', '<=', vals.get('end_date')),
            ('activity_occurrence_id.activityid', 'in', tuple(vals.get('activity_ids')[0][2])),
            ('es', '=', 'E'),
        ]).sorted(key=lambda r: (r.childid.lastname))

        if not prestation_ids:
            raise Warning(_("There is no prestationstimes for this dates."))

        tags = {}
        tags = self._generate_subvention_request(tags, vals)
        tags = self._generate_summary(tags, vals)
        tags = self._generate_childs_list(tags, prestation_ids, vals)
        tags = self._generate_supervisors(tags, vals)
        tags = self._generate_prestation_times(tags, vals)
        return tags


    @api.model
    def create(self, vals):
        if not vals['dates_ok']:
            raise Warning(_("Your dates are not ok. Please Check your dates."))

        id = super(extraschool_plain_report, self).create(vals)
        one_report_settings_obj = self.env['extraschool.onereport_settings']
        one_report_settings = one_report_settings_obj.search(
            [('name', '=', 'plain_report')])

        if not one_report_settings:
            raise Warning(_("There is no ONE report configuration"))

        report_template_filename = '/tmp/plain_report' + str(datetime.now()) + '.docx'
        report_template_file = open(report_template_filename, 'w')
        report_template_file.write(one_report_settings.report_template.decode('base64'))
        report_template_file.close()

        document = DocxTemplate(report_template_filename)
        tags = self._generate_context(vals)
        document.render(tags)
        document.save(report_template_filename)

        outfile = open(report_template_filename, "r").read()
        attachment_obj = self.env['ir.attachment']
        attachment_obj.create({'res_model': 'extraschool.plain_report', 'res_id': id.id,
                               'datas_fname': 'rapport_subvention_' + '.docx',
                               'name': 'plain_report_' + '.docx',
                               'datas': base64.b64encode(outfile), })
        os.remove(report_template_filename)

        return id
