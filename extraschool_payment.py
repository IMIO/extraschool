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

class extraschool_payment(osv.osv):
    _name = 'extraschool.payment'
    _description = 'Payment'

    _columns = {
        'paymenttype' : fields.selection((('1','CODA File'),('2','Ordinary account'),('3','Cash'),('4','Non value'),('5','Reject')),'Payment type'),
        'paymentdate' : fields.date('Date'),
        'structcom' : fields.char('Structured Communication', size=50),
        'account' : fields.char('Account', size=20),
        'name' : fields.char('Name', size=50),
        'addr1' : fields.char('Addr1', size=50),
        'addr2' : fields.char('Addr2', size=50),
        'amount' : fields.float('Amount'),
        'concernedinvoice' : fields.many2one('extraschool.invoice', 'Concerned invoice', required=False),
        'coda' : fields.many2one('extraschool.coda', 'Coda', required=False),
    }
    
    def savepayment(self, cr, uid, ids, context=None):
        obj_payment = self.pool.get('extraschool.payment')
        obj_invoice = self.pool.get('extraschool.invoice')
        form = self.read(cr,uid,ids,)[-1]
        invoice=obj_invoice.read(cr, uid, [form['concernedinvoice'][0]],['amount_received','amount_total','balance','no_value'])[0] 
        if (round(invoice['balance'],2) < form['amount']):
            raise osv.except_osv('Wrong value!','ERROR: The amount is bigger than the balance !!!')
            return False
        payment_id = obj_payment.write(cr, uid, ids[0], {'concernedinvoice':form['concernedinvoice'][0],'account':form['account'],'paymenttype':form['paymenttype'],'paymentdate':form['paymentdate'],'structcom':form['structcom'],'name':form['name'],'amount':form['amount']}, context=context)
        
        if form['paymenttype'] != '4':
            obj_invoice.write(cr, uid, [form['concernedinvoice'][0]], {'amount_received':round(invoice['amount_received'],2)+round(form['amount'],2),'balance':round(invoice['balance'],2)-round(form['amount'],2)}, context=context)
        else:
            obj_invoice.write(cr, uid, [form['concernedinvoice'][0]], {'no_value':round(invoice['no_value'],2)+round(form['amount'],2),'balance':round(invoice['balance'],2)-round(form['amount'],2)}, context=context)            
        return {'warning': {'title': 'Record saved','message': 'record saved!',}}
extraschool_payment()

