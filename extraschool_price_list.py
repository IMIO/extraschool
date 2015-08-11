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

from openerp import models, api, fields
from openerp.api import Environment

class extraschool_price_list(models.Model):
    _name = 'extraschool.price_list'
    _description = 'Activities price list'
    
    name = fields.Char('Name', size=50)  
    price_list_version_ids = fields.One2many('extraschool.price_list_version', 'price_list_id','Versions')

    
    def get_price(self,price_list,presta_date):
        price_list_obj = self.env['extraschool.price_list_version']
        ids = price_list_obj.search([('price_list_id', '=', price_list.price_list_version_ids.id),
                                        ('validity_from', '<=', presta_date),
                                        ('validity_to', '>=', presta_date),
                                        ])
        return ids if ids else False
        
extraschool_price_list()

class extraschool_price_list_version(models.Model):
    _name = 'extraschool.price_list_version'
    _description = 'Activities price list version'
    
    name = fields.Char('Name', size=50)
    price_list_id = fields.Many2one('extraschool.price_list', 'Price list')          
    validity_from = fields.Date('Validity from')
    validity_to = fields.Date('Validity to')
    activity_ids = fields.Many2many('extraschool.activity', 'extraschool_activity_pricelist_rel',string='Activity')
    child_type_ids = fields.Many2many('extraschool.childtype', 'extraschool_childtype_pricelist_rel',string='Child type')              
    child_position_ids = fields.Many2many('extraschool.childposition', 'extraschool_childposition_pricelist_rel',string='Child position')
    period_duration = fields.Integer('Period Duration')  
    period_tolerance = fields.Integer('Period Tolerance')  
    price = fields.Float('Price',digits=(7,3))
    
extraschool_price_list_version()
