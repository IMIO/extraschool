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
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import tools

class extraschool_payment(models.Model):
    _name = 'extraschool.payment'
    _description = 'Payment'

    paymenttype = fields.Selection((('1','CODA File'),
                                    ('3','Cash'),
                                    ('4','Non value'),
                                    ('5','Reject')),'Payment type')
    parent_id = fields.Many2one("extraschool.parent")
    paymentdate = fields.Date('Date', required=True)
    structcom = fields.Char('Structured Communication', size=50)
    structcom_prefix = fields.Char('Structured communication prefix', size=3)
    account = fields.Char('Account', size=20)
    name = fields.Char('Name', size=50)
    addr1 = fields.Char('Addr1', size=50)
    addr2 = fields.Char('Addr2', size=50)
    amount = fields.Float('Amount')
    solde = fields.Float(compute='compute_solde', string='Solde', store=True)
    payment_reconciliation_ids = fields.One2many('extraschool.payment_reconciliation','payment_id')
    coda = fields.Many2one('extraschool.coda', 'Coda', required=False)

    @api.onchange('structcom')
    def compute_prefix(self):
        for record in self:
            print "structcom : %s" % (self.structcom)
            if self.structcom:
                if len(self.structcom) > 3:
                    record.structcom_prefix = self.structcom[0:3]

    @api.depends('amount', 'payment_reconciliation_ids')
    def compute_solde(self):
        for record in self:
            record.solde = record.amount - sum(reconciliation.amount for reconciliation in record.payment_reconciliation_ids)
 
    
    def savepayment(self, cr, uid, ids, context=None):
        print "savepayment context : %s" % (context,)
        obj_payment = self.pool.get('extraschool.payment')
        form = self.read(cr,uid,ids,)[-1]
        payment_id = obj_payment.write(cr, uid, ids[0], {'parent_id':context['parent_id'],'account':form['account'],'paymenttype':form['paymenttype'],'paymentdate':form['paymentdate'],'structcom':form['structcom'],'name':form['name'],'amount':form['amount']}, context=context)
        
    
class extraschool_payment_reconciliation(models.Model):
    _name = 'extraschool.payment_reconciliation'
    _description = 'Payment reconciliation'
    
    payment_id = fields.Many2one("extraschool.payment", required=True)
    invoice_id = fields.Many2one("extraschool.invoice", required=True)
    amount = fields.Float('Amount')
    account = fields.Char(related='payment_id.account')
    paymentdate = fields.Date(related='payment_id.paymentdate')
    
    def name_get(self):            
        res=[]
        for reg in self:
            res.append((reg.id, "%s - %s" % (reg.structcom.name, reg.invoice_id.name)))    

        return res       
    
    
    class extraschool_payment_status_report(models.Model):
        _name = 'extraschool.payment_status_report'
        _description = 'Payment status report'
        _auto = False
        
        activity_category_id = fields.Many2one('extraschool.activitycategory',select=True)
        parent_id = fields.Many2one('extraschool.parent',select=True)  
        solde = fields.Float('solde',select=True)
        com_struct = fields.Char('Structured Communication')
        
        def init(self, cr):
            tools.sql.drop_view_if_exists(cr, 'extraschool_payment_status_report')
            cr.execute("""
                CREATE view extraschool_payment_status_report as
                    select min((zz.ac_id*10+zz.p_id)) as id, zz.ac_id as activity_category_id,
                           zz.p_id as parent_id, 
                           CASE 
                            WHEN sum(pay.solde) is NULL 
                               THEN 0
                               ELSE sum(pay.solde) 
                        END as solde,
                        '+++' || LPAD(case when zz.ac_com_struct_prefix is NULL then '0' else zz.ac_com_struct_prefix end, 3, '0') 
                        || '/' || LPAD(zz.p_id::TEXT,7,'0') || '/'
                        || LPAD(((LPAD(case when zz.ac_com_struct_prefix is NULL then '0' else zz.ac_com_struct_prefix end, 3, '0') || LPAD(zz.p_id::TEXT,7,'0'))::bigint % 97)::TEXT,2,'0')
                        || '+++' as com_struct 
                        
                    from (select ac.id as ac_id, p.id as p_id, ac.payment_invitation_com_struct_prefix as ac_com_struct_prefix from extraschool_activitycategory ac, extraschool_parent p) zz
                    left join extraschool_payment pay on zz.p_id = pay.parent_id and zz.ac_com_struct_prefix = pay.structcom_prefix
                    group by zz.ac_id,zz.p_id, zz.ac_com_struct_prefix
                    order by zz.ac_id,zz.p_id 
            """)
   
    

    
    


