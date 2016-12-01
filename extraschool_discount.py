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

class extraschool_discount(models.Model):
    _name = 'extraschool.discount'
    _description = 'Discount'

    name = fields.Char('Name', size=50)
    discount_version_ids = fields.One2many('extraschool.discount.version', 'discount_id',string='Versions',copy=True)

        
    
    def compute(self, invoice_ids):
#         for invoice in invoice_ids:
#             self.discount_version_ids.get_valide_version(invoice.period_from,invoice.period_to).compute(invoice)
        
        return True

class extraschool_discount_version(models.Model):
    _name = 'extraschool.discount.version'
    _description = 'Discount version'

    name = fields.Char('Name', size=50, required = True)
    discount_id = fields.Many2one('extraschool.duscount', 'Discount',ondelete='cascade', required = True)  
    validity_from = fields.Date('Validity from', required = True)
    validity_to = fields.Date('Validity to', required = True)    
    price_list_ids = fields.Many2many('extraschool.price_list', 'extraschool_discount_pricelist_rel',string='Price list')
    period = fields.Selection((('ca','Completed activity'),('d','Day'),('w','Week'),('m','Month')), string="Period",required = True)
    type = fields.Selection((('a','amount'),('p','Max price'),('p','Percent')),string="Type",required = True)
    value = fields.Float(string="Value", required = True)
    quantity_from = fields.Integer(string="Quantity from", default=0)
    quantity_to = fields.Integer(string="Quantity to", default=0)
    
    def get_valide_version(self,_from,_to):
        
        return self.search([('Validity from', '<=', _from),
                            ('Validity to', '>=', _to),
                         ])
    
    def compute(self,invoice):
        #get concerned lines filtered on price_list
        lines = invoice.invoice_line_ids.filtered(lambda r: r.price_list_version_id.price_list_id.id in self.price_list_ids.ids)
        
        #self.env.cr.execute(sql_update_invoice_total_price,(self.price_list_ids.ids))
    
    