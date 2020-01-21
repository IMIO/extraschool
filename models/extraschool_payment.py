# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia - Imio (<http://www.imio.be>).
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
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import tools
from datetime import datetime

class extraschool_payment(models.Model):
    _name = 'extraschool.payment'
    _description = 'Payment'
    _order = 'paymentdate desc'

    paymenttype = fields.Selection((('1', 'CODA File'),
                                    ('2', 'Mandat classe 4'),
                                    ('3', 'Cash'),
                                    ('4', 'Non value'),
                                    ('5', 'Reject'),
                                    ('6', 'Online'),
                                    ),'Payment type')
    parent_id = fields.Many2one("extraschool.parent",domain="[('isdisabled','=',False)]")
    paymentdate = fields.Date(string='Date', required=True)
    structcom = fields.Char(string='Structured Communication', size=50)
    structcom_prefix = fields.Char(string='Structured communication prefix', size=3)
    account = fields.Char(string='Account', size=20)
    name = fields.Char(string='Name', size=50)
    addr1 = fields.Char(string='Addr1', size=50)
    addr2 = fields.Char(string='Addr2', size=50)
    amount = fields.Float(string='Amount')
    comment = fields.Char(string='Comment')
    solde = fields.Float(compute='compute_solde', string='Solde', store=True)
    payment_reconciliation_ids = fields.One2many('extraschool.payment_reconciliation','payment_id')
    coda = fields.Many2one('extraschool.coda', string='Coda', required=False,ondelete='cascade')
    reject_id = fields.Many2one('extraschool.reject', string='Reject',ondelete='cascade')
    activity_category_id = fields.Many2many(
        'extraschool.activitycategory',
        'extraschool_payment_activity_category_rel',
        string='Activity Category'
    )
    refund = fields.Float(default=0.0)

    @api.multi
    def name_get(self):
        res=[]
        for payment in self:
            res.append((payment.id, _("%s %s") % (self.parent_id.name,self.amount)))
        return res

    @api.onchange('structcom')
    def compute_prefix(self):
        for record in self:
            if self.structcom:
                if len(self.structcom) > 3:
                    record.structcom_prefix = self.structcom[0:3]

    @api.depends('amount', 'payment_reconciliation_ids', 'refund')
    def compute_solde(self):
        for record in self:
            record.solde = record.amount - sum(reconciliation.amount for reconciliation in record.payment_reconciliation_ids) - record.refund

    def format_comstruct(self,comstruct):
        return ('+++%s/%s/%s+++' % (comstruct[0:3],comstruct[3:7],comstruct[7:12]))

    def savepayment(self, cr, uid, ids, context=None):
        obj_payment = self.pool.get('extraschool.payment')
        form = self.read(cr,uid,ids,)[-1]
        payment_id = obj_payment.write(cr, uid, ids[0], {'parent_id':context['parent_id'],'account':form['account'],'paymenttype':form['paymenttype'],'paymentdate':form['paymentdate'],'structcom':form['structcom'],'name':form['name'],'amount':form['amount']}, context=context)

    @api.multi
    def _get_reconciliation_list(self,parent_id,com_struct_prefix,payment_type,amount,from_coda=False):
        search_domain = [('parentid', '=', parent_id),
                         ('balance', '>', 0),
                         ]

        # On CODA payment, do not pay tagged or reminder/reminder fees invoice.
        if from_coda:
            search_domain += [('tag', '=', None)]
            if payment_type == 1:  # Prepaid.
                activity_category_ids = self.env['extraschool.activitycategory'].search([('payment_invitation_com_struct_prefix', '=', com_struct_prefix)]).ids

                search_domain += [('activitycategoryid', 'in',activity_category_ids),]

        invoices = self.env['extraschool.invoice'].search(search_domain)

        # Sort result on date.
        invoices.sorted(key=lambda r: r.number)
        reste = amount
        tmp_payment_reconciliation_ids = []
        for invoice in invoices:
            #compute reconcil amount
            if reste >= invoice.balance:
                reconcil_amout = invoice.balance
            else:
                reconcil_amout = reste
            reste -= reconcil_amout

            tmp_payment_reconciliation_ids.append({'invoice_id': invoice.id,
                                                   'amount': reconcil_amout,
                                                   'date': fields.Date.today(),
                                                   })
        return tmp_payment_reconciliation_ids

    @api.multi
    def refunds(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'extraschool.refund_wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'payment_id': self.id,
                'amount': self.solde,
            }
        }

    @api.multi
    def cancel_refund(self):
        self.refund = 0.0
        self.comment += self.env['extraschool.helper'].add_date_user("Annulation remboursement")

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class extraschool_refund_wizard(models.Model):
    _name = 'extraschool.refund_wizard'

    amount = fields.Float(string='Amount to refund', required=True)
    comment = fields.Char(string='Comment about the refund', required=True)

    @api.multi
    def refund(self):
        if self.amount > self._context.get('amount'):
            raise Warning(_('You cannot refund more than the actual amount'))
        elif self.amount < 0.01:
            raise Warning(_('Please input a number greater than 0.01'))
        else:
            self.env['extraschool.payment'].search([('id', '=', self._context.get('payment_id'))]).refund += self.amount
            comment = self.env['extraschool.payment'].search([('id', '=', self._context.get('payment_id'))]).comment
            if comment:
                self.env['extraschool.payment'].search([('id', '=', self._context.get('payment_id'))]).comment += self.env['extraschool.helper'].add_date_user(self.comment)
            else:
                self.env['extraschool.payment'].search([('id', '=', self._context.get('payment_id'))]).comment = self.env['extraschool.helper'].add_date_user(self.comment)

            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

class extraschool_payment_reconciliation(models.Model):
    _name = 'extraschool.payment_reconciliation'
    _description = 'Payment reconciliation'

    payment_id = fields.Many2one("extraschool.payment", required=True,ondelete='cascade')
    invoice_id = fields.Many2one("extraschool.invoice", required=True, index=True)
    biller_id = fields.Many2one(related='invoice_id.biller_id', store=True, index=True)
    biller_other_ref = fields.Char(related='invoice_id.biller_id.other_ref', store=True)
    amount = fields.Float('Amount')
    account = fields.Char(related='payment_id.account')
    paymentdate = fields.Date(related='payment_id.paymentdate', store=True)
    date = fields.Date("Reconcil date", index=True)

    def name_get(self):
        res=[]
        for reg in self:
            res.append((reg.id, "%s" % (reg.invoice_id.name)))

        return res


class extraschool_payment_status_report(models.Model):
    _name = 'extraschool.payment_status_report'
    _description = 'Payment status report'
    _auto = False # Disable creation of table.
    _order = 'totalbalance DESC'

    activity_category_id = fields.Many2one('extraschool.activitycategory',select=True)
    parent_id = fields.Many2one('extraschool.parent',select=True)
    solde = fields.Float('solde',select=True)
    com_struct = fields.Char('Structured Communication')
    totalbalance = fields.Float('Total balance')
    nbr_actif_child = fields.Integer('Nbr actif child')
    reminder_to_pay = fields.Boolean('Reminder to pay')
    # payment_date = fields.Date('Payment Date', select=True)

    # This is the view we use.
    def init(self, cr):
        # Drop before a new view.
        tools.sql.drop_view_if_exists(cr, 'extraschool_payment_status_report')
        cr.execute("""
            CREATE view extraschool_payment_status_report as
                select min((zz.ac_id*10000000000+zz.p_id)) as id, zz.ac_id as activity_category_id,
                       zz.p_id as parent_id,
                       CASE
                        WHEN sum(pay.solde) is NULL
                            THEN 0
                        WHEN round( CAST(sum(pay.solde) as numeric), 2) = 0.00
                            THEN 0
                        ELSE sum(pay.solde)
                        END as solde,
                    '+++' || LPAD(case when zz.ac_com_struct_prefix is NULL then '0' else zz.ac_com_struct_prefix end, 3, '0')
                    || '/' || substring(LPAD(zz.p_id::TEXT,7,'0') from 1 for 4) || '/' || substring(LPAD(zz.p_id::TEXT,7,'0') from 5 for 3)
                    || case when LPAD(((LPAD(case when zz.ac_com_struct_prefix is NULL then '0' else zz.ac_com_struct_prefix end, 3, '0') || LPAD(zz.p_id::TEXT,7,'0'))::bigint % 97)::TEXT,2,'0') = '00' then '97'
                    else LPAD(((LPAD(case when zz.ac_com_struct_prefix is NULL then '0' else zz.ac_com_struct_prefix end, 3, '0') || LPAD(zz.p_id::TEXT,7,'0'))::bigint % 97)::TEXT,2,'0') end
                    || '+++' as com_struct,
                    COALESCE((select sum(i.balance) from extraschool_invoice i where i.parentid = zz.p_id),0.0) as totalbalance,
                    (select count(*) from extraschool_child c where c.parentid = zz.p_id and c.isdisabled = False) as nbr_actif_child,
                    (select count(*)

                    from extraschool_invoice
                    where parentid = zz.p_id and last_reminder_id is not NULL and balance > 0) AS reminder_to_pay

                from (select ac.id as ac_id, p.id as p_id, ac.payment_invitation_com_struct_prefix as ac_com_struct_prefix,
          ac.invoicecomstructprefix as ac_invoicecomstructprefix, ac.remindercomstructprefix as ac_remindercomstructprefix from extraschool_activitycategory ac, extraschool_parent p) zz
                left join extraschool_payment pay on zz.p_id = pay.parent_id
                        and (zz.ac_com_struct_prefix = pay.structcom_prefix or
                             zz.ac_invoicecomstructprefix = pay.structcom_prefix or
                             zz.ac_remindercomstructprefix = pay.structcom_prefix)
                group by zz.p_id, zz.ac_com_struct_prefix,zz.ac_id
                ;
        """)

    def get_date_now(self):
        return datetime.now().strftime('%d-%m-%Y')

class extraschool_payment_report(models.Model):
    _name = 'extraschool.payment_report'
    _description = 'Payment report'
    _auto = False

    parent_id = fields.Many2one('extraschool.parent',select=True)
    amount = fields.Float('amount',select=True)
    solde = fields.Float('solde',select=True)
    structcom = fields.Char('Structured Communication')
    structcom_prefix = fields.Char('Structured Communication Prefix')
    payment_date = fields.Date('Payment Date')
    comment = fields.Char('Comment')



    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'extraschool_payment_report')
        cr.execute("""
            CREATE view extraschool_payment_report as
                select id, amount, solde, parent_id, comment,paymentdate as payment_date, structcom, structcom_prefix
                from extraschool_payment;
        """)

class extraschool_aged_balance(models.TransientModel):
    _name = 'extraschool.aged_balance'

    aged_date = fields.Date( string ='Reconcil Date', select=True)
    aged_balance_item_ids = fields.One2many('extraschool.aged_balance_item', 'aged_balance_id','Items')

    @api.onchange('aged_date')
    @api.one
    def _on_change_payment_type(self):

        self.aged_balance_item_ids = [(5, 0, 0)]
        if not self.aged_date:
            return

        items = []
        sql_aged_balance = """
            select b_year,
                (select sum(amount_total)::numeric(10,2)
                from extraschool_invoice i
                left join extraschool_biller b on i.biller_id = b.id
                where extract(YEAR from period_to) = b_year
                ) as total_fact,
                (select sum(no_value)::numeric(10,2)
                from extraschool_invoice i
                left join extraschool_biller b on i.biller_id = b.id
                where extract(YEAR from period_to) = b_year
                ) as no_value,
                (select sum(amount)::numeric(10,2)
                from extraschool_refound_line rl
                left join extraschool_invoice i on rl.invoiceid = i.id
                left join extraschool_biller b on i.biller_id = b.id
                where extract(YEAR from period_to) = b_year and rl.date <= %s
                ) as aged_no_value,
                (select sum(amount)::numeric(10,2)
                from extraschool_payment_reconciliation pr
                left join extraschool_biller b on pr.biller_id = b.id
                where pr.date <= %s and extract(YEAR from period_to) = b_year) as received
            from
                (select extract(YEAR from period_to) as b_year
                from extraschool_biller b
                group by extract(YEAR from period_to)) as t_b_year
            order by b_year
        """
        tmp_item_ids = []
        self.env.cr.execute(sql_aged_balance, (self.aged_date,self.aged_date))
        for item in self.env.cr.dictfetchall():
            item['total_fact'] = item['total_fact'] if item['total_fact'] else 0
            item['aged_no_value'] = item['aged_no_value'] if item['aged_no_value'] else 0
            item['received'] = item['received'] if item['received'] else 0
            tmp_item_ids.append((0,0,{'year' : item['b_year'],
                                      'total_fact' : item['total_fact'],
                                      'total_no_value' : item['aged_no_value'],
                                      'total_received' : item['received'],
                                      'total_balance' : item['total_fact'] - item['aged_no_value'] - item['received'],
                                      }))

        self.aged_balance_item_ids = tmp_item_ids

class extraschool_aged_balance_item(models.TransientModel):
    _name = 'extraschool.aged_balance_item'
    _description = 'Aged balance'

    aged_balance_id = fields.Many2one('extraschool.aged_balance')
    year = fields.Integer(string = 'Year')
    total_fact = fields.Float('Total fact')
    total_no_value = fields.Float('Total no value')
    total_received = fields.Float('Total received')
    total_balance = fields.Float('Total Balance')






