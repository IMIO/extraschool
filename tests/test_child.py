# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (c) 2012-TODAY OpenERP S.A. <http://openerp.com>
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

from openerp import tools
from openerp.tests import common

class Test_Child(common.TransactionCase):

    def setUp(self):
        """*****setUp*****"""
        super(Test_Child, self).setUp()
        cr, uid = self.cr, self.uid

        self.res_users = self.registry('res.users')
        self.child = self.registry('extraschool.child')

    def test_00_test_fct(self):
        """test test fct"""
        cr, uid = self.cr, self.uid
        self.my_child = self.child.browse(cr,uid,1,context=None)
        self.my_child.test()
        #we check that our order_line is a 'new' one and that there are no cashmove linked to that order_line:
        self.assertEqual(self.my_child.toto,'tutu')
