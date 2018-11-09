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
        """
        Unittest of prestation times of the day.
        :return: None
        """

##############################################################################
#   Simple case of a single entry.
#   I'll detail everything the first test but the rest will fillow the same
#   patern so I won't comment the next ones.
##############################################################################
#   Scenario: Entry 7h15
#   Expect: From entry get exit at 9. Verified = True
##############################################################################

        # First we target the category activity, child and place to create the right pdaprestationtimes.
        activity_category_1 = self.env['extraschool.activitycategory'].search([('name', '=', 'Accueil')])
        activity_category_2 = self.env['extraschool.activitycategory'].search([('name', '=', 'Repas')])
        child_1 = self.env['extraschool.child'].search([('lastname', '=', 'Jackson'), ('firstname', '=', 'Michael')])[1]
        place_1 = self.env['extraschool.place'].search([('name', '=', 'California')])[1]
        place_2 = self.env['extraschool.place'].search([('name', '=', 'Namur')])[1]
        school_implantation_1 = self.env['extraschool.schoolimplantation'].search([('name', '=', 'Hollywood')])[1]
        activity_1 = self.env['extraschool.activity'].search([('name', '=', 'stage 1')])[1]

        # Then we simulate a scan from a smartphone.
        pda_prestation_1 = self.env['extraschool.pdaprestationtimes'].create({
            'activitycategoryid': activity_category_1.id,
            'childid': child_1.id,
            'prestation_date': '2018-07-18',
            'es': 'E',
            'placeid': place_1.id,
            'prestation_time': 7.15,
        })

        # Finally we start the unittest.
        # First assert is to see if it's not verified before a check.
        self.assertEqual(pda_prestation_1.prestation_times_of_the_day_id.verified, False)

        # Check of that prestation.
        pda_prestation_1.prestation_times_of_the_day_id.check()

        # Get created prestation times order by time to check ES.
        prestation_times_ids_1 = self.env['extraschool.prestationtimes'].search(
            [('prestation_times_of_the_day_id', '=', pda_prestation_1.prestation_times_of_the_day_id.id)])\
            .sorted(key=lambda r: r.prestation_time)

        # Self explainatory
        self.assertEqual(len(prestation_times_ids_1), 2)
        self.assertEqual(pda_prestation_1.prestation_times_of_the_day_id.verified, True)
        self.assertEqual(prestation_times_ids_1[0].es, 'E')
        self.assertEqual(prestation_times_ids_1[1].es, 'S')
        self.assertEqual(prestation_times_ids_1[0].prestation_date, '2018-07-18')
        self.assertEqual(prestation_times_ids_1[1].prestation_date, '2018-07-18')
        self.assertEqual(prestation_times_ids_1[0].prestation_time, 7.15)
        self.assertEqual(prestation_times_ids_1[1].prestation_time, 9)

##################################################################################
#   Second test
#   Scenario: Entry at 6h30 (out of planned time)
#   Expect: Verified = False, Just one entry at 6h30
##################################################################################

        pda_prestation_2 = self.env['extraschool.pdaprestationtimes'].create({
            'activitycategoryid': activity_category_1.id,
            'childid': child_1.id,
            'prestation_date': '2018-07-19',
            'es': 'E',
            'placeid': place_1.id,
            'prestation_time': 6.5,
        })

        self.assertEqual(pda_prestation_2.prestation_times_of_the_day_id.verified, False)

        pda_prestation_2.prestation_times_of_the_day_id.check()

        prestation_times_ids_2 = self.env['extraschool.prestationtimes'].search(
            [('prestation_times_of_the_day_id', '=', pda_prestation_2.prestation_times_of_the_day_id.id)])\
            .sorted(key=lambda r: r.prestation_time)

        self.assertEqual(len(prestation_times_ids_2), 1)
        self.assertEqual(pda_prestation_2.prestation_times_of_the_day_id.verified, False)
        self.assertEqual(prestation_times_ids_2[0].es, 'E')
        self.assertEqual(prestation_times_ids_2[0].prestation_date, '2018-07-19')
        self.assertEqual(prestation_times_ids_2[0].prestation_time, 6.5)

##################################################################################
#   Third test
#   Scenario: Entry at 7h15 on an exclusion date
#   Expect: Verified = False, Just one entry at 7h15
##################################################################################

        pda_prestation_3 = self.env['extraschool.pdaprestationtimes'].create({
            'activitycategoryid': activity_category_1.id,
            'childid': child_1.id,
            'prestation_date': '2018-07-16',
            'es': 'E',
            'placeid': place_1.id,
            'prestation_time': 7.15,
        })

        self.assertEqual(pda_prestation_3.prestation_times_of_the_day_id.verified, False)

        pda_prestation_3.prestation_times_of_the_day_id.check()

        prestation_times_ids_3 = self.env['extraschool.prestationtimes'].search(
            [('prestation_times_of_the_day_id', '=', pda_prestation_3.prestation_times_of_the_day_id.id)])\
            .sorted(key=lambda r: r.prestation_time)

        self.assertEqual(len(prestation_times_ids_3), 1)
        self.assertEqual(pda_prestation_3.prestation_times_of_the_day_id.verified, False)
        self.assertEqual(prestation_times_ids_3[0].es, 'E')
        self.assertEqual(prestation_times_ids_3[0].prestation_date, '2018-07-16')
        self.assertEqual(prestation_times_ids_3[0].prestation_time, 7.15)

##################################################################################
#   Fourth test
#   Scenario: Single exit at 16h59.
#   Expect: Get 2 activites from 15h45 to 16h59.
##################################################################################

        pda_prestation_4 = self.env['extraschool.pdaprestationtimes'].create({
            'activitycategoryid': activity_category_1.id,
            'childid': child_1.id,
            'prestation_date': '2018-07-23',
            'es': 'S',
            'placeid': place_1.id,
            'prestation_time': 17,
        })

        self.assertEqual(pda_prestation_4.prestation_times_of_the_day_id.verified, False)

        pda_prestation_4.prestation_times_of_the_day_id.check()

        prestation_times_ids_4 = self.env['extraschool.prestationtimes'].search(
            [('prestation_times_of_the_day_id', '=', pda_prestation_4.prestation_times_of_the_day_id.id)])\
            .sorted(key=lambda r: r.prestation_time)

        self.assertEqual(len(prestation_times_ids_4), 4)
        self.assertEqual(pda_prestation_4.prestation_times_of_the_day_id.verified, True)
        self.assertEqual(prestation_times_ids_4[0].es, 'E')
        self.assertEqual(prestation_times_ids_4[0].prestation_date, '2018-07-23')
        self.assertEqual(prestation_times_ids_4[0].prestation_time, 15.75)
        self.assertEqual(prestation_times_ids_4[1].es, 'S')
        self.assertEqual(prestation_times_ids_4[1].prestation_date, '2018-07-23')
        self.assertEqual(prestation_times_ids_4[1].prestation_time, 16)
        self.assertEqual(prestation_times_ids_4[2].es, 'E')
        self.assertEqual(prestation_times_ids_4[2].prestation_date, '2018-07-23')
        self.assertEqual(prestation_times_ids_4[2].prestation_time, 16)
        self.assertEqual(prestation_times_ids_4[3].es, 'S')
        self.assertEqual(prestation_times_ids_4[3].prestation_date, '2018-07-23')
        self.assertEqual(prestation_times_ids_4[3].prestation_time, 17)

##################################################################################
#   Fifth test
#   Scenario: Single exit at 16h59.
#   Expect: Not verified because it's not the right placeid
##################################################################################

        pda_prestation_5 = self.env['extraschool.pdaprestationtimes'].create({
            'activitycategoryid': activity_category_1.id,
            'childid': child_1.id,
            'prestation_date': '2018-07-24',
            'es': 'S',
            'placeid': place_2.id,
            'prestation_time': 17,
        })

        self.assertEqual(pda_prestation_5.prestation_times_of_the_day_id.verified, False)

        pda_prestation_5.prestation_times_of_the_day_id.check()

        prestation_times_ids_5 = self.env['extraschool.prestationtimes'].search(
            [('prestation_times_of_the_day_id', '=', pda_prestation_5.prestation_times_of_the_day_id.id)])\
            .sorted(key=lambda r: r.prestation_time)

        self.assertEqual(len(prestation_times_ids_5), 1)
        self.assertEqual(prestation_times_ids_5.prestation_times_of_the_day_id.verified, False)
        self.assertEqual(prestation_times_ids_5[0].es, 'S')
        self.assertEqual(prestation_times_ids_5[0].prestation_date, '2018-07-24')
        self.assertEqual(prestation_times_ids_5[0].prestation_time, 17)

##################################################################################
#   Sixth test
#   Scenario: Single entry at 07h05.
#   Expect: Get 2 activites from 07h05 to 08h00.
##################################################################################

        pda_prestation_6 = self.env['extraschool.pdaprestationtimes'].create({
            'activitycategoryid': activity_category_1.id,
            'childid': child_1.id,
            'prestation_date': '2018-07-25',
            'es': 'E',
            'placeid': place_1.id,
            'prestation_time': 7.05,
        })

        self.assertEqual(pda_prestation_6.prestation_times_of_the_day_id.verified, False)

        pda_prestation_6.prestation_times_of_the_day_id.check()

        prestation_times_ids_6 = self.env['extraschool.prestationtimes'].search(
            [('prestation_times_of_the_day_id', '=', pda_prestation_6.prestation_times_of_the_day_id.id)])\
            .sorted(key=lambda r: r.prestation_time)

        self.assertEqual(len(prestation_times_ids_6), 4)
        self.assertEqual(pda_prestation_6.prestation_times_of_the_day_id.verified, True)
        self.assertEqual(prestation_times_ids_6[0].es, 'E')
        self.assertEqual(prestation_times_ids_6[0].prestation_date, '2018-07-25')
        self.assertEqual(prestation_times_ids_6[0].prestation_time, 7.05)
        self.assertEqual(prestation_times_ids_6[1].es, 'S')
        self.assertEqual(prestation_times_ids_6[1].prestation_date, '2018-07-25')
        self.assertEqual(prestation_times_ids_6[1].prestation_time, 7.5)
        self.assertEqual(prestation_times_ids_6[2].es, 'E')
        self.assertEqual(prestation_times_ids_6[2].prestation_date, '2018-07-25')
        self.assertEqual(prestation_times_ids_6[2].prestation_time, 7.5)
        self.assertEqual(prestation_times_ids_6[3].es, 'S')
        self.assertEqual(prestation_times_ids_6[3].prestation_date, '2018-07-25')
        self.assertEqual(prestation_times_ids_6[3].prestation_time, 8)

##################################################################################
#   Seventh test
#   Scenario: Registred activity.
#   Expect: Get 1 activity from 10 to 17.
##################################################################################

        child_registration_1 = self.env['extraschool.child_registration'].create({
            'school_implantation_id': school_implantation_1.id,
            'place_id': place_1.id,
            'activity_id': activity_1.id,
            'week': 31,
            'date_from': '2018-07-30',
            'date_to': '2018-08-05',
        })

        child_registration_line_1 = self.env['extraschool.child_registration_line'].create({
            'child_registration_id': child_registration_1.id,
            'monday': True,
            'child_id': child_1.id,
        })

        child_registration_1.validate()
        child_registration_1.validate()

        prestation_times_of_the_day_1 = self.env['extraschool.prestation_times_of_the_day'].search([('date_of_the_day', '=', '2018-07-30'), ('child_id', '=', child_1.id)])


        self.assertEqual(prestation_times_of_the_day_1.verified, False)

        prestation_times_of_the_day_1.check()

        prestation_times_ids_7 = self.env['extraschool.prestationtimes'].search(
            [('prestation_times_of_the_day_id', '=', prestation_times_of_the_day_1.id)])\
            .sorted(key=lambda r: r.prestation_time)

        self.assertEqual(len(prestation_times_ids_7), 2)
        self.assertEqual(prestation_times_of_the_day_1.verified, True)
        self.assertEqual(prestation_times_ids_7[0].es, 'E')
        self.assertEqual(prestation_times_ids_7[0].prestation_date, '2018-07-30')
        self.assertEqual(prestation_times_ids_7[0].prestation_time, 10)
        self.assertEqual(prestation_times_ids_7[1].es, 'S')
        self.assertEqual(prestation_times_ids_7[1].prestation_date, '2018-07-30')
        self.assertEqual(prestation_times_ids_7[1].prestation_time, 17)

##################################################################################
#   Eigth test
#   Scenario: Repas.
#   Expect: Get 1 activity from 10 to 17.
##################################################################################

        pda_prestation_7 = self.env['extraschool.pdaprestationtimes'].create({
            'activitycategoryid': activity_category_2.id,
            'childid': child_1.id,
            'prestation_date': '2018-08-01',
            'es': 'E',
            'placeid': place_1.id,
            'prestation_time': 12.5,
        })

        self.assertEqual(pda_prestation_7.prestation_times_of_the_day_id.verified, False)

        pda_prestation_7.prestation_times_of_the_day_id.check()

        prestation_times_ids_7 = self.env['extraschool.prestationtimes'].search(
            [('prestation_times_of_the_day_id', '=', pda_prestation_7.prestation_times_of_the_day_id.id)])\
            .sorted(key=lambda r: r.prestation_time)

        self.assertEqual(len(prestation_times_ids_7), 4)
        self.assertEqual(pda_prestation_7.prestation_times_of_the_day_id.verified, True)
        self.assertEqual(prestation_times_ids_7[0].es, 'E')
        self.assertEqual(prestation_times_ids_7[0].prestation_date, '2018-08-01')
        self.assertEqual(prestation_times_ids_7[0].prestation_time, 12)
        self.assertEqual(prestation_times_ids_7[1].es, 'S')
        self.assertEqual(prestation_times_ids_7[1].prestation_date, '2018-08-01')
        self.assertEqual(prestation_times_ids_7[1].prestation_time, 13)
