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

from openerp.osv import osv, fields

class extraschool_activitycategory(osv.osv):
    _name = 'extraschool.activitycategory'
    _description = 'Activities categories'
    
    _columns = {
        'name' : fields.char('Name', size=50),         
        'activities' : fields.one2many('extraschool.activity', 'category','Activities'),               
        'placeids'  : fields.many2many('extraschool.place','extraschool_activitycategory_place_rel', 'activitycategory_id', 'place_id','Schoolcare place'),
        'childpositiondetermination' : fields.selection((('byparent','by parent'),('byparentwp','by parent (only childs with prestations)'),('byaddress','by address'),('byaddresswp','by address (only childs with prestations)')),'Child position determination'),
        'priorityorder': fields.integer('Priority order'),
        'invoicetemplate': fields.char('Invoice Template', size=50),        
        'invoicecomstructprefix': fields.char('Invoice Comstruct prefix', size=4),
        'invoicelastcomstruct' : fields.integer('Last Invoice structured comunication number'),
        'invoiceemailaddress' : fields.char('Invoice email address', size=50),
        'invoiceemailsubject' : fields.char('Invoice email subject', size=50),
        'invoiceemailtext': fields.text('Invoice email text'),        
        'remindercomstructprefix': fields.char('Reminder Comstruct prefix', size=4),
        'reminderlastcomstruct' : fields.integer('Last Reminder structured comunication number'),
        'reminderemailaddress' : fields.char('Reminder email address', size=50),
        'reminderemailsubject' : fields.char('Reminder email subject', size=50),
        'reminderemailtext': fields.text('Reminder email text'),
        'bankaccount': fields.char('Bank account', size=4),
        'taxcertificatetemplate': fields.char('Tax Certificate Template', size=50)
    }
    _defaults = {
        'invoicetemplate' : lambda *a: 'facture.odt',
    }
extraschool_activitycategory()
