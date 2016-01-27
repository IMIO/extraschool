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

from openerp import models, api, fields, _
from openerp.api import Environment
import cStringIO
import base64
import os
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschool_manuel_invoice_wizard(models.TransientModel):
    _name = 'extraschool.manuel_invoice_wizard'

    parent_id = fields.Many2one("extraschool.parent")
    invoice_date = fields.Date('Date', required=True)
    payment_term = fields.Date('Payment term', required=True)     
    description = fields.Char('Description', required=True)
    invoice_child = fields.Boolean('One invoice / child')
    leveltype = fields.Selection((('M,P','Maternelle et Primaire'),
                                  ('M','Maternelle'),
                                  ('P','Primaire')),
                                 'Level type')
    amount = fields.Float('Amount', required=True)
    activity_category_id = fields.Many2one("extraschool.activitycategory", required=True)
    state = fields.Selection([('init', 'Init'),
                             ('redirect', 'Redirect'),],
                            'State', required=True, default='init'
                            )

    @api.multi
    def generate_invoice(self):
        if len(self._context.get('active_ids')):                    
            #create a bille to store invoice
            biller = self.env['extraschool.biller'].create({'period_from' : self.invoice_date,
                                                            'period_to' : self.invoice_date,
                                                            'payment_term': self.payment_term,
                                                            })
        else:
            return True
        
        payment_obj = self.env['extraschool.payment']
        invoice_ids = []
        inv_obj = self.env['extraschool.invoice']  
        inv_line_obj = self.env['extraschool.invoicedprestations']  
        next_invoice_num = self.activity_category_id.invoicelastcomstruct
        for parent in self.env['extraschool.parent'].browse(self._context.get('active_ids')):
            if self.invoice_child:
                for child in parent.child_ids:
                    if child.levelid.leveltype in self.leveltype:
                        com_struct_prefix_str = self.activity_category_id.invoicecomstructprefix
                        com_struct_id_str = str(next_invoice_num).zfill(7)
                        com_struct_check_str = str(long(com_struct_prefix_str+com_struct_id_str) % 97)
                        com_struct_check_str = com_struct_check_str if com_struct_check_str != '00' else '97'
                        invoice = inv_obj.create({'name' : _('invoice_%s') % (str(next_invoice_num).zfill(7),),
                                    'number' : next_invoice_num,
                                    'parentid' : parent.id,
                                    'biller_id' : biller.id,
                                    'activitycategoryid': self.activity_category_id.id,
                                    'schoolimplantationid': child.schoolimplantation.id,
                                    'structcom': payment_obj.format_comstruct('%s%s%s' % (com_struct_prefix_str,com_struct_id_str,com_struct_check_str))})
                        inv_line_obj.create({'invoiceid' : invoice.id,
                            'childid': child.id,
                            'description' : self.description,
                            'unit_price': self.amount,
                            'quantity': 1,
                            'total_price': self.amount,
                            })
                                                
                        next_invoice_num += 1
                        invoice_ids.append(invoice.id)
                    
            else:
                com_struct_prefix_str = self.activity_category_id.invoicecomstructprefix
                com_struct_id_str = str(next_invoice_num).zfill(7)
                com_struct_check_str = str(long(com_struct_prefix_str+com_struct_id_str) % 97)
                com_struct_check_str = com_struct_check_str if com_struct_check_str != '00' else '97'
                invoice = inv_obj.create({'name' : _('invoice_%s') % (str(next_invoice_num).zfill(7),),
                                'number' : next_invoice_num,
                                'parentid' : parent.id,
                                'biller_id' : biller.id,
                                'activitycategoryid': self.activity_category_id.id,
                                'structcom': payment_obj.format_comstruct('%s%s%s' % (com_struct_prefix_str,com_struct_id_str,com_struct_check_str))})
                inv_line_obj.create({'invoiceid' : invoice.id,
                    'description' : self.description,
                    'unit_price': self.amount,
                    'quantity': 1,
                    'total_price': self.amount,
                    })
                next_invoice_num += 1          
                invoice_ids.append(invoice.id)
        
        self.activity_category_id.invoicelastcomstruct = next_invoice_num
        inv_obj.browse(invoice_ids).reconcil()
        
        return True



    
