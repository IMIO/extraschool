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

from openerp.tests.common import HttpCase, TransactionCase

class TestData(TransactionCase):

    def setUp(self):
        super(TestData, self).setUp()

        self.activityoccurrence_model = self.env['extraschool.activityoccurrence']
        self.child_model = self.env['extraschool.child']
        self.parent_model = self.env['extraschool.parent']
        self.activity_model = self.env['extraschool.activity']
        self.prestation_times_of_the_day_model = self.env['extraschool.prestation_times_of_the_day']
        self.activity_category_model = self.env['extraschool.activitycategory']
        self.school_implantation_model = self.env['extraschool.schoolimplantation']
        self.school_model = self.env['extraschool.school']
        self.place_model = self.env['extraschool.place']
        self.prestation_times_model = self.env['extraschool.prestationtimes']
        self.exclusion_date_model = self.env['extraschool.activityexclusiondates']

        # Creation of activity category
        activity_category_1 = self.activity_category_model.create({
            'childpositiondetermination': 'byparent',
            'invoicecomstructprefix': 100,
            'remindercomstructprefix': 200,
            'payment_invitation_com_struct_prefix': 300,
            'max_school_implantation': 2,
        })

        # Creation of school
        school_1 = self.school_model.create({
            'name': 'Los Angeles'
        })
        school_2 = self.school_model.create({
            'name': 'Courrières'
        })

        # Creation of school implantation
        school_implantation_1 = self.school_implantation_model.create({
            'schoolid': school_1.id,
            'name': 'Hollywood',
        })
        school_implantation_2 = self.school_implantation_model.create({
            'schoolid': school_2.id,
            'name': 'Gembloux',
        })

        # Creation of place
        place_1 = self.place_model.create({
            'name': 'California',
            'schoolimplantation_ids': [school_implantation_1.id],
        })
        place_2 = self.place_model.create({
            'name': 'Namur',
            'schoolimplantation_ids': [school_implantation_2.id],
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

        # Creation of exclusion date.
        exclusion_1 = self.exclusion_date_model.create({
            'date_from': '2018-07-16',
            'date_to': '2018-07-16',
            'name': 'Exclude 16-07-2018',
        })

        # Creation of activities.
        activity_1 = self.activity_model.create({
            'name': 'les bronzés font du ski',
            'category_id': activity_category_1.id,
            'validity_from': '2018-07-16',
            'validity_to': '2018-07-20',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'to',
            'prest_from': 7,
            'prest_to': 9,
            'exclusiondates_ids': [(4, exclusion_1.id)],
            'placeids': [(4, place_1.id)],
            'short_name': 'splendide',
        })

        activity_2 = self.activity_model.create({
            'name': 'Accueil soir gratuit',
            'category_id': activity_category_1.id,
            'validity_from': '2018-07-23',
            'validity_to': '2018-07-27',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'from',
            'prest_from': 15.75,
            'prest_to': 16,
            'placeids': [(4, place_1.id)],
            'short_name': 'soir gratuit',
            'autoaddchilds': False,
            'onlyregisteredchilds': False,
        })

        activity_3 = self.activity_model.create({
            'name': 'Accueil soir payant',
            'category_id': activity_category_1.id,
            'validity_from': '2018-07-23',
            'validity_to': '2018-07-27',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'from',
            'prest_from': 16,
            'prest_to': 18,
            'placeids': [(4, place_1.id)],
            'short_name': 'soir payant',
            'parent_id': activity_2.id,
            'autoaddchilds': False,
            'onlyregisteredchilds': False,
        })

        activity_4 = self.activity_model.create({
            'name': 'Accueil matin gratuit',
            'category_id': activity_category_1.id,
            'validity_from': '2018-07-23',
            'validity_to': '2018-07-27',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'to',
            'prest_from': 7,
            'prest_to': 7.5,
            'placeids': [(4, place_1.id)],
            'short_name': 'matin gratuit',
            'autoaddchilds': False,
            'onlyregisteredchilds': False,
        })

        activity_5 = self.activity_model.create({
            'name': 'Accueil matin payant',
            'category_id': activity_category_1.id,
            'validity_from': '2018-07-23',
            'validity_to': '2018-07-27',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'to',
            'prest_from': 7.5,
            'prest_to': 8,
            'placeids': [(4, place_1.id)],
            'short_name': 'matin payant',
            'parent_id': activity_4.id,
            'autoaddchilds': False,
            'onlyregisteredchilds': False,
        })
