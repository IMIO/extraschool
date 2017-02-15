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

    name = fields.Char('Name')
    description = fields.Char('Description')
    discount_version_ids = fields.One2many('extraschool.discount.version', 'discount_id',string='Versions',copy=True)

        
    
    def compute(self, biller_id):
        self.discount_version_ids.get_valide_version(biller_id.period_from,biller_id.period_to).compute(biller_id)
        
        return True

class extraschool_discount_version(models.Model):
    _name = 'extraschool.discount.version'
    _description = 'Discount version'

    name = fields.Char('Name', size=50, required = True)
    discount_id = fields.Many2one('extraschool.discount', 'Discount',ondelete='cascade', required = True)  
    validity_from = fields.Date('Validity from', required = True)
    validity_to = fields.Date('Validity to', required = True)    
    price_list_ids = fields.Many2many('extraschool.price_list', 'extraschool_discount_pricelist_rel',string='Price list')
    child_type_ids = fields.Many2many('extraschool.childtype', 'extraschool_discount_childtype_rel',string='Child type')              
    period = fields.Selection((('ca','Completed activity'),
                               ('d','Day'),
                               ('w','Week'),
                               ('m','Month')), string="Period",required = True)
    type = fields.Selection((('a','amount'),
                             ('p','Max price'),
                             ('p','Percent')),string="Type",required = True)
    apply_on = fields.Selection((('f','Invoice'),
                                ('c','Child'),),string="Apply on",required = True)
    value = fields.Float(string="Value", required = True)
    quantity_type = fields.Selection((('m','Minute'),
                                      ('q','Quantity'),                                      
                                      ('p','Presence'),),string="Quantity type",required = True)
    quantity_from = fields.Integer(string="Quantity from", default=0)
    quantity_to = fields.Integer(string="Quantity to", default=0)
    
    def get_valide_version(self,_from,_to):
        
        return self.search([('validity_from', '<=', _from),
                            ('validity_to', '>=', _to),
                         ])
    
    def compute(self,biller_id):
        print "compute discount !!!!!"
        cr,uid = self.env.cr, self.env.user.id
        for discount_version_id in self:
            print "get concerned lines ids"        
            #get concerned lines filtered on price_list
    #        lines = invoice.invoice_line_ids.filtered(lambda r: r.price_list_version_id.price_list_id.id in self.price_list_ids.ids)
            
            sql = """select ip.invoiceid as invoiceid, ip.childid as childid, 
                     sum(duration) as sum_duration, sum(quantity) as sum_quantity, count(*) as count
                     from extraschool_invoicedprestations ip
                     left join extraschool_price_list_version plv on plv.id = ip.price_list_version_id
                     left join extraschool_child c on c.id = ip.childid
                     where ip.invoiceid in (""" + ','.join(map(str, biller_id.invoice_ids.ids))+ """)
                     and plv.price_list_id in (""" + ','.join(map(str, self.price_list_ids.ids))+ """)
                     and c.childtypeid in (""" + ','.join(map(str, self.child_type_ids.ids))+ """)
                     group by ip.invoiceid,ip.childid
                     having sum(duration) >= %s
                     """
#            print sql % (self.quantity_from,)
            cr.execute(sql,(self.quantity_from,))
            args=[]
            for r in cr.dictfetchall():
                args.append((uid,
                             uid,
                             r['invoiceid'],
                             r['childid'],
                             discount_version_id.discount_id.description,
                             1,#quantité
                             self.value,#unit_price
                             self.value,#total price
                             ))
            lines_args_str = ""
            if len(args):
                lines_args_str += ','.join(cr.mogrify("""(%s, current_timestamp, %s, current_timestamp,
                                                        %s,%s,%s,%s,%s,%s)""", x) for x in args)   
            print "exec sql create discount lines"
            #print insert_data               
            invoice_line_ids = cr.execute("""insert into extraschool_invoicedprestations 
                                            (create_uid, create_date, write_uid, write_date,
                                            invoiceid, childid, description, quantity, unit_price,total_price) 
                                            VALUES """ + lines_args_str + ";")
            
            #self.env.cr.execute(sql_update_invoice_total_price,(self.price_list_ids.ids))
        
    