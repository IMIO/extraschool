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

class Test_PrestationCheck(common.TransactionCase):

    def setUp(self):
        """*****setUp*****"""
        super(Test_PrestationCheck, self).setUp()
        cr, uid = self.cr, self.uid

        self.prestationscheck_wizard = self.registry('extraschool.prestationscheck_wizard')
        
    def test_00_test_fct(self):
        """test test _check"""
        cr, uid = self.cr, self.uid
        form = {'placeid': [1,2,3],
                'period_from': '2014-01-01',
                'period_to': '2014-01-31',
                'activitycategory': 1,
                'state': 'init',
                'currentdate': False,
                }
        return_value = self.prestationscheck_wizard._check(cr, uid,form)
        print "-------------"
        print str(return_value)
        print "-------------"
        
        self.assertEqual(return_value,'tutu')
