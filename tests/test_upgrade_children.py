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

from openerp.addons.extraschool.tests.test_data import TestData
import logging
_logger = logging.getLogger(__name__)

class UpgradeChildrenCheckTest(TestData):

    def test_upgrade(self):

        child_1 = self.env['extraschool.child'].search([('lastname', '=', 'Jackson'), ('firstname', '=', 'Michael')])
        child_2 = self.env['extraschool.child'].search([('lastname', '=', 'Mercury'), ('firstname', '=', 'Freddy')])

        self.assertEqual(child_1.levelid.id, 2)
        self.assertEqual(child_2.levelid.id, 4)
