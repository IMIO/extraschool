# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014
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

from openerp.addons.extraschool.tests.test_data import TestData

class PrestationCheckTest(TestData):

    def test_check_presta(self):

        activity_category_1 = self.env['extraschool.activity'].search([('name', '=', 'les bronzés font du ski')])
        child_1 = self.env['extraschool.child'].search([('lastname', '=', 'Jackson'), ('firstname', '=', 'Michael')])
        place_1 = self.env['extraschool.place'].search([('name', '=', 'California')])

        pda_prestation_1 = self.env['extraschool.pdaprestationtimes'].create({
            'activitycategoryid': activity_category_1.id,
            'childid': child_1.id,
            'prestation_date': '2018-07-18',
            'es': 'E',
            'placeid': place_1.id,
            'prestation_time': 7.15,
        })

        # Check of the function 'extraschool.prestation_times_of_the_day'.check() with data created.
        pda_prestation_1.prestation_times_of_the_day_id.check()

        # Get created prestation times order by time to check ES.
        prestation_times_ids_1 = self.env['extraschool.prestationtimes'].search(
            [('prestation_times_of_the_day_id', '=', pda_prestation_1.prestation_times_of_the_day_id.id)]).sorted(key=lambda r: r.prestation_time)

        
        self.assertEqual(pda_prestation_1.prestation_times_of_the_day_id.verified, True)
        self.assertEqual(prestation_times_ids_1[0].es, 'E')
        self.assertEqual(prestation_times_ids_1[1].es, 'S')
        self.assertEqual(prestation_times_ids_1[0].prestation_time, 7.15)
        self.assertEqual(prestation_times_ids_1[1].prestation_time, 9)
