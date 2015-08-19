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
import cStringIO
import base64
import os

class extraschool_payment_wizard(models.TransientModel):
    _name = 'extraschool.payment_wizard'

    
    payment_type = fields.Selection((('1','Prepaid'),
                                    ('2','Invoice'),
                                    ),'Payment type', required=True)
    payment_date = fields.Date('Date', required=True)
    amount = fields.Float('Amount', required=True)
    parent_id = fields.Many2one("extraschool.parent")
    activity_category_id = fields.Many2one("extraschool.activitycategory")
    state = fields.Selection([('init', 'Init'),
                             ('print_payment', 'Print payment'),
                             ('print_reconciliation', 'Print reconciliation')],
                            'State', required=True, default='init'
                            )
    @api.model
    def default_get(self,fields):
        print "----------------"
        print "context : %s" % (self.env.context,)
        print "----------------"
        print "fields : %s" % (fields,)
        print "----------------"
        print "return : %s" % {'parent_id': self.env.context.get('parent_id'),}
        return {'state': 'init',
                'parent_id': self.env.context.get('parent_id'),}
        
    @api.multi
    def create_payment(self):
        payment = self.env['extraschool.payment']
        payment.create({'parent_id': self.parent_id.id,
                        'paymentdate': self.payment_date,
                        'structcom_prefix': self.activity_category_id.payment_invitation_com_struct_prefix,
                        'amount': self.amount})
        return {}
    
#         #get last qrcode value from config
#         self.last_id = config.lastqrcodenbr + 1
#         if self.print_type == 'qrcode':
#             #SET last qrcode value to config
#             config.lastqrcodenbr = config.lastqrcodenbr + self.quantity
# 
#         datas = {
#         'ids': self.ids,
#         'model': report.model, 
#         }
#         
#         return {
#                'type': 'ir.actions.report.xml',
#                'report_name': 'extraschool.tpl_payment_wizard_report',
#                'datas': datas,
#                'report_type': 'qweb-pdf',
#            }        

