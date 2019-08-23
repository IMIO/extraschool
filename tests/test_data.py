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

from openerp.tests.common import HttpCase, TransactionCase


class TestData(TransactionCase):

    def setUp(self):
        super(TestData, self).setUp()

        self.activityoccurrence_model = self.env['extraschool.activityoccurrence']
        self.child_model = self.env['extraschool.child']
        self.parent_model = self.env['extraschool.parent']
        self.activity_model = self.env['extraschool.activity']
        self.prestation_times_of_the_day_model = self.env['extraschool.prestation_times_of_the_day']
        self.prestation_times_model = self.env['extraschool.prestationtimes']
        self.activity_category_model = self.env['extraschool.activitycategory']
        self.school_implantation_model = self.env['extraschool.schoolimplantation']
        self.school_model = self.env['extraschool.school']
        self.place_model = self.env['extraschool.place']
        self.prestation_times_model = self.env['extraschool.prestationtimes']
        self.exclusion_date_model = self.env['extraschool.activityexclusiondates']
        self.organising_power_model = self.env['extraschool.organising_power']
        self.child_registration_model = self.env['extraschool.child_registration']
        self.price_list_model = self.env['extraschool.price_list']
        self.price_list_version_model = self.env['extraschool.price_list_version']
        self.class_model = self.env['extraschool.class']
        self.biller_model = self.env['extraschool.biller']
        self.invoice_model = self.env['extraschool.invoice']
        self.invoiced_prestations_model = self.env['extraschool.invoicedprestations']
        self.sequence_model = self.env['extraschool.activitycategory.sequence']


        # region Organising Power
        organising_power = self.organising_power_model.create({
            'town': 'Dreamland',
            'max_school_implantation': 100,
        })
        # endregion

        # region Activity Category
        activity_category_1 = self.activity_category_model.create({
            'name': 'Accueil',
            'childpositiondetermination': 'byparent',
            'invoicecomstructprefix': 100,
            'remindercomstructprefix': 200,
            'payment_invitation_com_struct_prefix': 300,
            'organising_power_id': organising_power.id,
        })

        activity_category_2 = self.activity_category_model.create({
            'name': 'Repas',
            'childpositiondetermination': 'byparent',
            'invoicecomstructprefix': 101,
            'remindercomstructprefix': 202,
            'payment_invitation_com_struct_prefix': 303,
            'organising_power_id': organising_power.id,
        })
        # endregion

        # region School
        school_1 = self.school_model.create({
            'name': 'Los Angeles'
        })
        school_2 = self.school_model.create({
            'name': 'Courrières'
        })
        # endregion

        # region School Implantation
        school_implantation_1 = self.school_implantation_model.create({
            'schoolid': school_1.id,
            'name': 'Hollywood',
        })
        school_implantation_2 = self.school_implantation_model.create({
            'schoolid': school_2.id,
            'name': 'Gembloux',
        })
        # endregion

        # region Place
        place_1 = self.place_model.create({
            'name': 'California',
            'schoolimplantation_ids': [school_implantation_1.id],
        })
        place_2 = self.place_model.create({
            'name': 'Namur',
            'schoolimplantation_ids': [school_implantation_2.id],
        })
        # endregion

        # region Class
        class_2_school_1 = self.class_model.create({
            'name': 'M1',
            'levelids': [2],
            'schoolimplantation': school_implantation_1.id,
        })
        class_5_school_1 = self.class_model.create({
            'name': 'P1',
            'levelids': [5],
            'schoolimplantation': school_implantation_1.id,
        })
        class_3_school_1 = self.class_model.create({
            'name': 'M2',
            'levelids': [3],
            'schoolimplantation': school_implantation_1.id,
        })
        class_6_school_1 = self.class_model.create({
            'name': 'P2',
            'levelids': [6],
            'schoolimplantation': school_implantation_1.id,
        })
        # endregion

        # region Parent
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
        # endregion

        # region Child
        child_1 = self.child_model.create({
            'lastname': 'Jackson',
            'firstname': 'Michael',
            'schoolimplantation': school_implantation_1.id,
            'childtypeid': 1,
            'levelid': 2,
            'classid': class_2_school_1.id,
            'parentid': parent_1.id,
            'birthdate': '2005-05-29',
        })

        child_2 = self.child_model.create({
            'lastname': 'Mercury',
            'firstname': 'Freddy',
            'schoolimplantation': school_implantation_1.id,
            'childtypeid': 1,
            'levelid': 5,
            'classid': class_5_school_1.id,
            'parentid': parent_1.id,
            'birthdate': '2003-06-12',
        })
        # endregion

        # region Exclusion Date
        exclusion_1 = self.exclusion_date_model.create({
            'date_from': '2018-07-16',
            'date_to': '2018-07-16',
            'name': 'Exclude 16-07-2018',
        })
        # endregion

        # region Activity
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

        activity_6 = self.activity_model.create({
            'name': 'stage 1',
            'category_id': activity_category_1.id,
            'validity_from': '2018-07-30',
            'validity_to': '2018-07-30',
            'leveltype': 'M,P',
            'days': '0',
            'default_from_to': 'from_to',
            'prest_from': 10,
            'prest_to': 17,
            'placeids': [(4, place_1.id)],
            'short_name': 'matin payant',
            'autoaddchilds': True,
            'onlyregisteredchilds': True,
        })

        activity_7 = self.activity_model.create({
            'name': 'repas',
            'category_id': activity_category_2.id,
            'validity_from': '2018-08-01',
            'validity_to': '2018-08-02',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'from_to',
            'prest_from': 12,
            'prest_to': 13,
            'placeids': [(4, place_1.id)],
            'short_name': 'repas',
            'autoaddchilds': False,
            'onlyregisteredchilds': False,
        })

        activity_8 = self.activity_model.create({
            'name': 'accueil matin',
            'category_id': activity_category_1.id,
            'validity_from': '2018-08-02',
            'validity_to': '2018-08-02',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'to',
            'prest_from': 7,
            'prest_to': 8,
            'placeids': [(4, place_1.id)],
            'short_name': 'matin gratuit',
            'autoaddchilds': False,
            'onlyregisteredchilds': False,
        })

        activity_9 = self.activity_model.create({
            'name': 'accueil soir',
            'category_id': activity_category_1.id,
            'validity_from': '2018-08-02',
            'validity_to': '2018-08-02',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'from',
            'prest_from': 16,
            'prest_to': 17,
            'placeids': [(4, place_1.id)],
            'short_name': 'soir gratuit',
            'autoaddchilds': False,
            'onlyregisteredchilds': False,
        })

        activity_10 = self.activity_model.create({
            'name': 'les bronzés font du ski',
            'category_id': activity_category_1.id,
            'validity_from': '2018-08-03',
            'validity_to': '2018-08-03',
            'leveltype': 'P',
            'days': '0,1,2,3,4',
            'default_from_to': 'to',
            'prest_from': 7,
            'prest_to': 9,
            'placeids': [(4, place_1.id)],
            'short_name': 'splendide',
            'autoaddchilds': False,
            'onlyregisteredchilds': False,
        })

        activity_11 = self.activity_model.create({
            'name': 'Garderie',
            'category_id': activity_category_1.id,
            'validity_from': '2018-08-06',
            'validity_to': '2018-08-06',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'to',
            'prest_from': 7,
            'prest_to': 10,
            'placeids': [(4, place_1.id)],
            'short_name': 'Garderie',
            'autoaddchilds': False,
            'onlyregisteredchilds': False,
        })

        activity_12 = self.activity_model.create({
            'name': 'Cirque',
            'category_id': activity_category_1.id,
            'validity_from': '2018-08-06',
            'validity_to': '2018-08-06',
            'leveltype': 'M,P',
            'days': '0,1,2,3,4',
            'default_from_to': 'from_to',
            'prest_from': 6,
            'prest_to': 9,
            'placeids': [(4, place_1.id)],
            'short_name': 'Cirque du soleil',
            'autoaddchilds': False,
            'onlyregisteredchilds': True,
        })
        # endregion

        # region Price List Version
        price_list_version_1 = self.price_list_version_model.create({
            'name': 'matin payant',
            'validity_from': '2018-01-01',
            'validity_to': '2018-12-31',
            'activity_ids': [(4, activity_5.id)],
            'child_type_ids': [(4, 1)],
            'child_position_ids': [(4, 1)],
            'period_duration': 15,
            'price': 0.150,
            'period_tolerance': 0,
            'max_price': 0.000,
        })
        # endregion

        # region Price List
        price_list_1 = self.price_list_model.create({
            'name': 'matin payant',
            'price_list_version_ids': [(4, price_list_version_1.id)]
        })
        # endregion

        # region Biller
        biller_1 = self.biller_model.create({
            'period_from': '2019-08-01',
            'period_to': '2019-08-31',
            'payment_term': '2019-09-15',
            'invoices_date': '2019-08-22',
            'activitycategoryid': [(4, activity_category_1.id)]
        })
        # endregion

        # region Invoice
        self.sequence_model.create({
            'year': 2019,
            'type': 'invoice',
            'name': 'sequence',
            'activity_category_id': activity_category_1.id,
            'sequence': 1,
        })
        next_invoice_num = activity_category_1.get_next_comstruct('invoice', biller_1.get_from_year())
        invoice_1 = self.invoice_model.create({
            'name': '1',
            'number': next_invoice_num['num'],
            'parentid': parent_1.id,
            'biller_id': biller_1.id,
            'payment_term': biller_1.payment_term,
            'activitycategoryid': [(4, activity_category_1.id)],
            'structcom': next_invoice_num['com_struct'],
        })

        invoiced_presta_1 = self.invoiced_prestations_model.create({
            'invoiceid': invoice_1.id,
            'description': 'Test01',
            'unitprice': 20,
            'quantity': 1,
            'total_price': 20,
        })

        invoice_1.reconcil()

        next_invoice_num = activity_category_1.get_next_comstruct('invoice', biller_1.get_from_year())
        invoice_2 = self.invoice_model.create({
            'name': '2',
            'number': next_invoice_num['num'],
            'parentid': parent_1.id,
            'biller_id': biller_1.id,
            'payment_term': biller_1.payment_term,
            'activitycategoryid': [(4, activity_category_1.id)],
            'structcom': next_invoice_num['com_struct'],
        })

        invoiced_presta_2 = self.invoiced_prestations_model.create({
            'invoiceid': invoice_2.id,
            'description': 'Test02',
            'unitprice': 30,
            'quantity': 1,
            'total_price': 30,
        })

        invoice_2.reconcil()

        biller_1.pdf_ready = True
        biller_1.in_creation = False
        # endregion
