# __openerp__.py
# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014 
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot - Imio (<http://www.imio.be>).
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

{
    'name' : 'Extraschool',
    'version' : '0.3',
    'author' : 'Town of La Bruyère and Imio',
    'depends' : ['base',],
    'init_xml' : ['init.xml',],
    'demo' : ['extraschool_demo.xml',],
    'test' : ['test/invoice_test.yml'],
    'data' : [
        'views/extraschool_activitycategory.xml',
        'views/extraschool_activity.xml',
        'views/extraschool_biller.xml',
        'views/extraschool_childsimportfilter.xml',
        'views/extraschool_childsimport.xml',
        'views/extraschool_childsworkbook_wizard.xml',
        'views/extraschool_coda.xml',
        'views/extraschool_discount.xml',
        'views/extraschool_guardianprestationtimes.xml',
        'views/extraschool_guardian.xml',
        'views/extraschool_initupdate_wizard.xml',
        'views/extraschool_invoice_wizard.xml',
        'views/extraschool_invoice.xml',
        'views/extraschool_mainsettings.xml',
        'views/extraschool_parent.xml',
        'views/extraschool_payment.xml',
        'views/extraschool_place.xml',
        'views/extraschool_prestationscheck_wizard.xml',
        'views/extraschool_prestations_wizard.xml',
        'views/extraschool_prestationtimes.xml',
        'views/extraschool_qrcodes_wizard.xml',
        'views/extraschool_remindersjournal.xml',
        'views/extraschool_smartphone.xml',
        'views/extraschool_statsone.xml',
        'views/extraschool_taxcertificates.xml',
        'views/extraschool_timecorrection.xml',
        'views/extraschool_school.xml',
        'views/extraschool_schoolimplantation.xml',
        'views/extraschool_class.xml',
        'views/extraschool_level.xml',
        'views/extraschool_child.xml',
        'extraschool_view.xml',
        'extraschool_report.xml',
        'security/extraschool_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable' : True,
    'application': True,
    'description' : "This module is to manage billing attendance for extra school activities",
}
