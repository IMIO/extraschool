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
        self.place = self.registry('extraschool.place')
        self.activitycategory = self.registry('extraschool.activitycategory')
        self.prestationtimes = self.registry('extraschool.prestationtimes')
        
        
    def test_00_test_fct(self):
        cr, uid = self.cr, self.uid
        form = {'placeid': self.place.search(cr,uid,[('name','in',['Ecole du parc'])]),
                'period_from': '2014-01-01',
                'period_to': '2014-01-31',
                'activitycategory': self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])]),
                'state': 'init',
                'currentdate': False,
                }
        return_value = self.prestationscheck_wizard._check(cr, uid,form)
        
        #check return
        self.assertEqual(return_value['state'],'end_of_verification')
        #check ajout de la presta manquante
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-01')])
        self.assertEqual(len(presta),2,'check ajout de la presta manquante')
        #check verified field is true
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-01'),
                                                     ('verified','=',True),
                                                     ])
        self.assertEqual(len(presta),2,'check verified field is true')
        
