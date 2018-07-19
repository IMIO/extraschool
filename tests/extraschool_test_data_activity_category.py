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

class TestDataActivityCategory(HttpCase):

    def setUp(self):
        super(TestDataActivityCategory, self).setUp()
        self.activity_category_model = self.env['extraschool.activitycategory']

        # Creation of activity category.
        activity_category_1 = self.activity_category_model.create({
            'name': 'testForCheck',
            'childpositiondetermination': 'byparent',
            'invoicecomstructprefix': 100,
            'remindercomstructprefix': 200,
            'payment_invitation_com_struct_prefix': 300,
            'max_school_implantation': 1,
        })
