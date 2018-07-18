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

from openerp.tests.common import HttpCase

class TestData(HttpCase):

    def setUp(self):
        super(TestData, self).setUp()

        self.activityoccurrence_model = self.env['extraschool.activityoccurrence']
        self.child_model = self.env['extraschool.child']
        self.parent_model = self.env['extraschool.parent']
        self.activity_model = self.env['extraschool.activity']
        self.prestation_times_of_the_day_model = self.env['extraschool.prestation_times_of_the_day']
        self.pda_prestation_times_model = self.env['extraschool.pdaprestationtimes']
        self.activity_category_model = self.env['extraschool.activitycategory']
        self.school_implantation_model = self.env['extraschool.schoolimplantation']
        self.school_model = self.env['extraschool.school']
        self.place_model = self.env['extraschool.place']
        self.prestation_times_model = self.env['extraschool.prestationtimes']

        # Creation of activity category
        activity_category_1 = self.activity_category_model.create({
            'childpositiondetermination': 'byparent',
            'invoicecomstructprefix': 100,
            'remindercomstructprefix': 200,
            'payment_invitation_com_struct_prefix': 300,
            'max_school_implantation': 1,
        })

        # Creation of school
        school_1 = self.school_model.create({
            'name': 'Los Angeles'
        })

        # Creation of school implantation
        school_implantation_1 = self.school_implantation_model.create({
            'schoolid': school_1.id,
            'name': 'Hollywood',
        })

        # Creation of place
        place_1 = self.place_model.create({
            'name': 'California',
            'schoolimplantation_ids': [school_implantation_1.id],
        })

        # Creation of parents.
        parent_1 = self.parent_model.create({
            'lastname': 'Jackson',
            'firstname': 'Joseph',
            'street': 'Rue Léon Morel, 1',
            'zipcode': '5032',
            'city': 'Isnes',
            'one_subvention_type': 'sf',
            'invoicesendmethod': 'onlyemail',
            'remindersendmethod': 'onlyemail',
            'email': 'jm@star.be',
        })

        # Creation of children.
        child_1 = self.child_model.create({
            'lastname': 'Jackson',
            'firstname': 'Michael',
            'schoolimplantation': school_implantation_1.id,
            'childtypeid': 1,
            'levelid': 2,
            'parentid': parent_1.id,
            'birthdate': '2005-05-29',
        })

        # Creation of activities.
        activity_1 = self.activity_model.create({
            'name': 'les bronzés font du ski',
            'category_id': activity_category_1.id,
            'validity_from': '2018-07-18',
            'validity_to': '2018-07-19',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'to',
            'prest_from': 7,
            'prest_to': 9,
            'placeids': [(4, place_1.id)],
            'short_name': 'splendide',
        })

        # Creation of pda prestation
        pda_prestation_id = self.pda_prestation_times_model.create({
            'activitycategoryid': activity_category_1.id,
            'childid': child_1.id,
            'prestation_date': '2018-07-18',
            'es': 'E',
            'placeid': place_1.id,
            'prestation_time': 7.15,
        })
