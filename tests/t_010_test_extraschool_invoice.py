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

class T_010_Test_ExtraSchool_Invoice(common.TransactionCase):

    def setUp(self):
        """*****setUp*****"""
        super(T_010_Test_ExtraSchool_Invoice, self).setUp()
        cr, uid = self.cr, self.uid

        self.invoice_wizard = self.registry('extraschool.invoice_wizard')
        self.schoolimplantation = self.registry('extraschool.schoolimplantation')
        self.activitycategory = self.registry('extraschool.activitycategory')
        self.prestationtimes = self.registry('extraschool.prestationtimes')

    def test_00_test_compute_invoice(self):
        print "test_00_test_compute_invoice"       
        cr, uid = self.cr, self.uid
        form = {'schoolimplantationid': self.schoolimplantation.search(cr,uid,[]),
                'period_from': '2014-02-01',
                'period_to': '2014-02-28',
                'invoice_date': '2014-02-28',
                'invoice_term': '2014-02-28',
                'activitycategory': self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])]),
                'state': 'init',
                }

        return_value = self.invoice_wizard._compute_invoices(cr,uid,form)
        
        self.assertEqual(return_value['state'],'compute_invoices','Facture boum')           
          
     
