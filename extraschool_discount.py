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

class extraschool_discount(osv.osv):
    _name = 'extraschool.discount'
    _description = 'Discount'

    _columns = {
        'name' : fields.char('Name', size=50),
        'activities'  : fields.many2many('extraschool.activity','extraschool_discount_activity_rel', 'discount_id', 'activity_id','Activities'),
        'wichactivities' : fields.selection((('OneOf','One of these activities'),('Each','Each of these activities'),('Sum','Sum of these activities')),'Wich activities'),
        'childtypes'  : fields.many2many('extraschool.childtype','extraschool_discount_childtype_rel', 'discount_id', 'childtype_id','Childtypes'),
        'childposition_ids' : fields.many2many('extraschool.childposition','extraschool_activity_childposition_rel', 'activity_id', 'childposition_id','Child position'),
        'period' : fields.selection((('by_day','By Day'),('by_invoice','By Invoice')),'Period'),
        'discounttype' : fields.selection((('sub','Subtraction'),('prc','Percentage'),('max','Max amount')),'Discount type'),
        'discount' : fields.char('Discount', size=6),
        'discountrule'  : fields.many2many('extraschool.discountrule','extraschool_discount_discountrule_rel', 'discount_id', 'discountrule_id','Discount Rule'),
    }
extraschool_discount()
