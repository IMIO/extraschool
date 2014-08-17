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

class extraschool_invoice(osv.osv):
    _name = 'extraschool.invoice'
    _description = 'invoice'

    _columns = {
        'name' : fields.char('Name', size=20,readonly=True),
        'schoolimplantationid' : fields.many2one('extraschool.schoolimplantation', 'School implantation', required=False,readonly=True),
        'parentid' : fields.many2one('extraschool.parent', 'Parent', required=False),
        'number' : fields.integer('Number',readonly=True),
        'structcom' : fields.char('Structured Communication', size=50,readonly=True),
        'amount_total' : fields.float('Amount',readonly=True),
        'amount_received' : fields.float('Received',readonly=True),
        'balance' : fields.float('Balance',readonly=True),
        'no_value' : fields.float('No value',readonly=True),
        'discount' : fields.float('Discount',readonly=True),
        'biller_id' : fields.many2one('extraschool.biller', 'Biller', required=False,ondelete='cascade',readonly=True),
        'filename' : fields.char('filename', size=20,readonly=True),
        'invoice_file' : fields.binary('File', readonly=True),
        'payment_ids' : fields.one2many('extraschool.payment', 'concernedinvoice','Payments',readonly=True),
        'oldid' : fields.char('oldid', size=20),
        'activitycategoryid' : fields.related('biller_id', 'activitycategoryid', type='many2one',relation="extraschool.activitycategory", string='Activity Category'),
        'period_from' : fields.related('biller_id', 'period_from', type='date', string='Period from'),
        'period_to' : fields.related('biller_id', 'period_to', type='date', string='Period to'),
        'payment_term' : fields.related('biller_id', 'payment_term', type='date', string='Payment term'),      
    }
    _defaults = {
        'name' : lambda *a: 'Facture'
    }
    def addpayment(self, cr, uid, ids, context=None):
        view_obj = self.pool.get('ir.ui.view')
        extraschool_payment_form2 = view_obj.search(cr, uid, [('model', '=', 'extraschool.payment'), \
                                 ('name', '=', 'payment.form2')])
        
        return {
            'name': "Payment",
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': extraschool_payment_form2,            
            'res_model': 'extraschool.payment',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {'default_concernedinvoice' : ids[0]}
        }
extraschool_invoice()
