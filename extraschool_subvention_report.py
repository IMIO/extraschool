# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchial - Imio (<http://www.imio.be>).
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
from docutils.utils.math.math2html import Formula

from openerp import models, api, fields,_
from openerp.api import Environment
import cStringIO
import base64
import os
from pyPdf import PdfFileWriter, PdfFileReader
import datetime
from xlrd import open_workbook
from xlutils.copy import copy
from xlutils.styles import Styles
import xlwt
import xlsxwriter
from xlwt import *
from datetime import date, datetime, timedelta as td
from openerp.exceptions import Warning
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
import json


class extraschool_subvention_report(models.Model):
    _name = 'extraschool.subvention_report'

    start_date = fields.Date('Start date', required=True)
    end_date = fields.Date('End date', required=True)
    activity = fields.Many2many(
        'extraschool.activity',
        'extraschool_activity_activity_subvention_rel',
        'subvention_id',
        'activity_id',
        string='Activity',
        required=True
    )

    @api.multi
    def generate_report(self,under_6,over_6,id):
        report = '/tmp/subvention_report' + str(datetime.now()) + '.xls'
        workbook = xlsxwriter.Workbook(report)

        title = workbook.add_format({'bold': True, 'bg_color': '#cccccc', 'font_size': 20, 'border': True})
        bold = workbook.add_format({'bold': True})

        worksheet = workbook.add_worksheet()
        worksheet.merge_range('A1:E1', "ENFANTS DE + DE 6 ANS", title)
        worksheet.write(1,0, "Nom", bold)
        worksheet.write(1,1, u"Prénom", bold)
        worksheet.write(1,2, "Age", bold)
        worksheet.write(1,3, "Nombre de jours", bold)
        worksheet.write(1,4, "Prix", bold)

        row = 2

        for child in under_6:
            worksheet.write(row, 0, under_6[child]['lastname'])
            worksheet.write(row, 1, under_6[child]['firstname'])
            worksheet.write(row, 2, under_6[child]['age'])
            worksheet.write(row, 3, under_6[child]['prestation'])
            row += 1

        workbook.close()

        outfile = open(report, "r").read()
        attachment_obj = self.env['ir.attachment']
        attachment_obj.create({'res_model': 'extraschool.subvention_report', 'res_id': id.id,
                               'datas_fname': 'rapport_subvention_' + '.xls',
                               'name': 'rapport_one_' + '.xls',
                               'datas': base64.b64encode(outfile), })
        os.remove(report)

    @api.model
    def create(self,vals):

        under_6 = {}
        over_6 = {}

        prestation_ids = self.env['extraschool.prestationtimes'].search([
            ('prestation_date', '>=', vals.get('start_date')),
            ('prestation_date', '<=', vals.get('end_date')),
            ('activity_occurrence_id.activityid', 'in', tuple(vals.get('activity')[0][2])),
            ('es', '=', 'E'),
        ]).sorted(key=lambda r: (r.childid.lastname))

        for prestation in prestation_ids :
            age = prestation.childid.get_age()
            if age >= 6 :
                if prestation.childid.id in over_6:
                    over_6[prestation.childid.id]['prestation'] += 1
                else:
                    over_6[prestation.childid.id] = {'lastname': prestation.childid.lastname, 'firstname':  prestation.childid.firstname, 'age': age, 'prestation': 1}
            else :
                if prestation.childid.id in under_6:
                    under_6[prestation.childid.id]['prestation'] += 1
                else:
                    under_6[prestation.childid.id] = {'lastname': prestation.childid.lastname, 'firstname':  prestation.childid.firstname, 'age': age, 'prestation': 1}

        id = super(extraschool_subvention_report, self).create(vals)
        self.generate_report(under_6,over_6,id)

        return id
