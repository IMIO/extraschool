# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia- Imio (<http://www.imio.be>).
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

from odoo.tests import common
from odoo import models, api, fields, _

import logging
_logger = logging.getLogger(__name__)


class InvoiceTest(common.TransactionCase):

    def setUp(self):
        super(InvoiceTest, self).setUp()

        self.invoice_wizard_model = self.env['extraschool.invoice_wizard']


        activity_category_1 = self.env['extraschool.activitycategory'].search([('name', '=', 'Accueil')])
        activity_category_2 = self.env['extraschool.activitycategory'].search([('name', '=', 'Repas')])
        # self.period_from = '2018-08-01'
        # self.period_to = '2018-08-31'
        # self.generate_pdf = False
        # self.invoice_date = '2018-09-02'
        # self.invoice_term = '2018-09-02'
        # self.activitycategory = activity_category_2

    def test_invoice_generation(self):
        """
        Unittest of invoicing.
        :return: None
        """

        activity_category_2 = self.env['extraschool.activitycategory'].search([('name', '=', 'Repas')])

        self.invoice_wizard_model.with_context(
            period_from='2018-08-01',
            period_to='2018-08-31',
            generate_pdf=False,
            invoice_date='2018-09-02',
            invoice_term='2018-09-02',
            activitycategory=[(6, 0, activity_category_2.id)],
        ).action_compute_invoices()

        self.assertEqual(False, True)
