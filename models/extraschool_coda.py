# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia & Jenny Pans - Imio (<http://www.imio.be>).
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
import base64
import re

from openerp import models, api, fields, _
from openerp.exceptions import Warning


class extraschool_coda(models.Model):
    _name = 'extraschool.coda'

    _order = 'codadate desc'

    name = fields.Char('Name', size=20)
    codafile = fields.Binary('CODA File')
    codadate = fields.Date('CODA Date', readonly=True)
    # amountperyear = fields.Text(compute='_compute_amountperyear', string="Amount per year")
    amount_accepted = fields.Float(compute='_compute_amount_accepted', string="Amount accepted")
    amount_rejected = fields.Float(compute='_compute_amount_rejected', string="Amount rejected")

    paymentids = fields.One2many('extraschool.payment', 'coda', 'Payments', readonly=True)
    rejectids = fields.One2many('extraschool.reject', 'coda', 'Rejects', readonly=True)

    state = fields.Selection([('todo', 'To Do'),
                              ('handled', 'Handled')],
                             'validated', required=True, default='todo'
                             )
    bank_account_number = fields.Char(
        string='Bank account number',
        readonly=True,
    )

    @api.multi
    def unlink(self):
        for payment in self.paymentids:
            for reconciliation in payment.payment_reconciliation_ids:
                if reconciliation:
                    reconciliation.invoice_id.cancel_payment()
            payment.unlink()
        for reject in self.rejectids:
            for reconciliation_reject in reject.corrected_payment_id.payment_reconciliation_ids:
                if reconciliation_reject:
                    reconciliation_reject.invoice_id.cancel_payment()
            reject.unlink()
        return super(extraschool_coda, self).unlink()

    @api.one
    def validate(self):
        if self.state == 'todo':
            self.state = 'handled'

    @api.depends('paymentids')
    def _compute_amount_accepted(self):
        for r in self:
            r.amount_accepted = sum(p.amount for p in r.paymentids)

    @api.depends('paymentids')
    def _compute_amount_rejected(self):
        for r in self:
            r.amount_rejected = sum(rej.amount for rej in r.rejectids)

    def _get_amount(self, line):
        pass

    @api.model
    def create(self, vals):
        # Check if there is a file
        if not vals['codafile']:
            raise Warning(_('No coda file!', 'ERROR: No CODA File !!!'))
        # Check if coda's version correct
        lines = unicode(base64.decodestring(vals['codafile']), 'windows-1252', 'strict').split('\n')
        if lines[0][127] != '2':
            raise Warning(_('ERROR: Wrong CODA version !!!'))
        # Check if coda already imported
        bank_account = lines[1][5:21]
        date = '20' + lines[0][9:11] + '-' + lines[0][7:9] + '-' + lines[0][5:7]
        if self.search([
            ('codadate', '=', date),
            ('bank_account_number', '=', bank_account)
        ]).ids:
            raise Warning(_('CODA already imported !!!'))
        # Check if valid account
        activitycategory_obj = self.env['extraschool.activitycategory']
        # Get all bank account and remove no valids characters
        accounts = [re.sub(r"[^a-zA-Z0-9]", "", account) for account in
                    activitycategory_obj.search([]).mapped("bankaccount")]
        if bank_account not in accounts:
            raise Warning(_('ERROR: The account number in this CODA file is not used in this application !!!'))
        ################################################################################################################
        # to do refactoring suite api V8
        cr = self.env.cr
        paymentids = []
        rejectids = []
        invoice_obj = self.env['extraschool.invoice']
        reminder_obj = self.env['extraschool.reminder']
        payment_obj = self.env['extraschool.payment']
        payment_reconciliation_obj = self.env['extraschool.payment_reconciliation']
        reject_obj = self.env['extraschool.reject']

        reject = False
        amount = 0.0
        transfer_date = ''
        communication = ''
        free_communication = ''
        reject_cause = ''
        parent_account = ''
        name = ''
        adr1 = ''
        adr2 = ''
        with_address = False

        # On parcours toutes les lignes du CODA
        for line in lines:
            # On ne prends que les lignes non vides
            if len(line) > 0:
                #
                if line[0] == '2':
                    if line[1] == '1':
                        # On récupère le montant
                        amount = eval(line[31:44] + '.' + line[44:47])
                        transfer_date = date
                        if line[62] == '1':
                            communication = self.env["extraschool.structured_communication"].format(line[65:77])
                        else:
                            reject = True
                            reject_cause = _('No structured Communication')
                            free_communication = line[62:112]
                    else:
                        if (line[1] == '3') and (amount > 0.0) and transfer_date:
                            parent_account = line[10:26]
                            name = line[47:73]
                #
                if (line[0] == '3') and (line[1] == '2') and (len(name) > 1):
                    adr1 = line[10:45]
                    adr2 = line[45:80]
                    with_address = True

                if ((with_address == True) and (len(adr1) > 0)) or ((with_address == False) and (len(name) > 1)):
                    if reject == False:
                        cr.execute('select invoicecomstructprefix from extraschool_activitycategory')
                        prefixes = cr.dictfetchall()
                        prefixfound = False
                        for prefix in prefixes:
                            if (len(prefix['invoicecomstructprefix']) > 0) and (
                                len(communication) > len(prefix['invoicecomstructprefix'])):
                                if communication[3:3 + len(prefix['invoicecomstructprefix'])] == prefix[
                                    'invoicecomstructprefix']:
                                    prefixfound = True
                                    _prefix = prefix['invoicecomstructprefix']
                        if prefixfound:
                            invoice = invoice_obj.search([('structcom', '=', communication),
                                                          ('huissier', '=', False),
                                                          ('tag', '=', None)
                                                          ])

                            if len(invoice.ids) == 1:
                                if invoice.balance < amount:
                                    reject = True
                                    reject_cause = _('Amount greather than invoice balance')
                                else:
                                    activity_category = activitycategory_obj.search(
                                        [('invoicecomstructprefix', '=', _prefix)])
                                    payment_id = payment_obj.create({
                                        'parent_id': invoice.parentid.id,
                                        'paymentdate': transfer_date,
                                        'structcom_prefix': _prefix,
                                        'structcom': communication,
                                        'paymenttype': '1',
                                        'account': parent_account,
                                        'name': name,
                                        'adr1': adr1,
                                        'adr2': adr2,
                                        'amount': amount,
                                        'activity_category_id': [(6, 0, [activity_category.id])],
                                    })

                                    payment_reconciliation_obj.create({'payment_id': payment_id.id,
                                                                       'invoice_id': invoice.id,
                                                                       'date': transfer_date,
                                                                       # Todo: si date facture <= coda: date coda sinon date facture
                                                                       'amount': amount})
                                    invoice._compute_balance()
                                    paymentids.append(payment_id.id)
                            else:
                                reject = True
                                reject_cause = _('No valid structured Communication')
                        else:
                            # Rappels
                            cr.execute('select remindercomstructprefix from extraschool_activitycategory')
                            prefixes = cr.dictfetchall()
                            prefixfound = False
                            for prefix in prefixes:
                                if prefix['remindercomstructprefix']:
                                    if len(communication) > len(prefix['remindercomstructprefix']):
                                        if communication[3:3 + len(prefix['remindercomstructprefix'])] == prefix[
                                            'remindercomstructprefix']:
                                            prefixfound = True
                                            _prefix = prefix['remindercomstructprefix']
                            if prefixfound:
                                reminder = reminder_obj.search([('structcom', '=', communication)])
                                fees_to_pay = False
                                if len(reminder) == 1:
                                    totaldue = sum(invoice.balance for invoice in reminder.concerned_invoice_ids)
                                    if reminder.reminders_journal_item_id.reminder_type_id.fees_type == 'fix':
                                        fees_to_pay = True

                                    # This is were I check if the structcom comes from an old reminder.
                                    has_invoice = self.env['extraschool.invoice'].search(
                                        [('last_reminder_id', '=', reminder.id)])

                                    if amount != round(totaldue, 2):
                                        reject = True
                                        reject_cause = _(
                                            'A reminder has been found but the amount is not corresponding to balances of invoices')

                                    # Check if this reminder and invoice concerned (If a parent tries to pay an old reminder).
                                    elif not has_invoice:
                                        reject = True
                                        reject_cause = _(
                                            'The communication is outdated. Another reminder has been created.')

                                    else:
                                        # if fees_to_pay:
                                        #     # Create a payment for the fees.
                                        #     payment_id = payment_obj.create({'parent_id': reminder.parentid.id,
                                        #                                      'paymentdate': transfer_date,
                                        #                                      'structcom_prefix': _prefix,
                                        #                                      'structcom': communication,
                                        #                                      'paymenttype': '1',
                                        #                                      'comment': 'Paiement des frais de rappel',
                                        #                                      'account': parent_account,
                                        #                                      'name': name,
                                        #                                      'adr1': adr1,
                                        #                                      'adr2': adr2,
                                        #                                      'solde': 0.0,
                                        #                                      'amount': reminder.reminders_journal_item_id.reminder_type_id.fees_amount})
                                        #
                                        #     invoice = self.env['extraschool.invoice'].search([('last_reminder_id', '=', reminder.id), ('reminder_fees', '=', True)])
                                        #
                                        #     payment_reconciliation_obj.create({'payment_id': payment_id.id,
                                        #                                        'invoice_id': invoice.id,
                                        #                                        'date': transfer_date,
                                        #                                        # todo: si date facture <= coda: date coda sinon date facture
                                        #                                        'amount': invoice.balance})
                                        #     invoice._compute_balance()
                                        #     paymentids.append(payment_id.id)

                                        # todo: paramètrage des paiements des rappels. Apure fees en premier, toutes les factures avant fees
                                        for invoice in reminder.concerned_invoice_ids:
                                            activity_category = activitycategory_obj.search(
                                                [('remindercomstructprefix', '=', _prefix)])
                                            payment_id = payment_obj.create({'parent_id': invoice.parentid.id,
                                                                             'activity_category_id': [
                                                                                 (6, 0, [activity_category.id])],
                                                                             'paymentdate': transfer_date,
                                                                             'structcom_prefix': _prefix,
                                                                             'structcom': communication,
                                                                             'paymenttype': '1',
                                                                             'account': parent_account,
                                                                             'name': name,
                                                                             'amount': invoice.balance})

                                            payment_reconciliation_obj.create({'payment_id': payment_id.id,
                                                                               'invoice_id': invoice.id,
                                                                               'date': transfer_date,
                                                                               # todo: si date facture <= coda: date coda sinon date facture
                                                                               'amount': invoice.balance})
                                            invoice._compute_balance()
                                            paymentids.append(payment_id.id)
                                else:
                                    reject = True;
                                    reject_cause = _('No valid structured Communication')
                            else:
                                # Pre-paiements
                                cr.execute(
                                    'select payment_invitation_com_struct_prefix from extraschool_activitycategory')
                                prefixes = cr.dictfetchall()
                                prefixfound = False
                                for prefix in prefixes:
                                    if prefix['payment_invitation_com_struct_prefix']:
                                        if len(communication) > len(prefix['payment_invitation_com_struct_prefix']):
                                            if communication[
                                               3:3 + len(prefix['payment_invitation_com_struct_prefix'])] == prefix[
                                                'payment_invitation_com_struct_prefix']:
                                                prefixfound = True
                                                _prefix = prefix['payment_invitation_com_struct_prefix']
                                if prefixfound:
                                    parentid = int(communication[7:11] + communication[12:15])
                                    if len(self.env['extraschool.parent'].search([('id', '=', parentid)])) == 0 or \
                                        self.env['extraschool.parent'].search(
                                            [('id', '=', parentid)]).isdisabled == True:
                                        reject = True
                                        reject_cause = _('Parent not found')
                                    else:
                                        activity_category = activitycategory_obj.search(
                                            [('payment_invitation_com_struct_prefix', '=', _prefix)])
                                        payment_id = payment_obj.create({
                                            'parent_id': parentid,
                                            'paymentdate': transfer_date,
                                            'activity_category_id': [(6, 0, [activity_category.id])],
                                            'structcom_prefix': _prefix,
                                            'structcom': communication,
                                            'paymenttype': '1',
                                            'account': parent_account,
                                            'name': name,
                                            'adr1': adr1,
                                            'adr2': adr2,
                                            'amount': amount,
                                        })

                                        for reconciliation in payment_id._get_reconciliation_list(parentid, _prefix, 1,
                                                                                                  amount, True):
                                            payment_reconciliation_obj.create({'payment_id': payment_id.id,
                                                                               'invoice_id': reconciliation[
                                                                                   'invoice_id'],
                                                                               'date': transfer_date,
                                                                               # todo: si date facture <= coda: date coda sinon date facture
                                                                               'amount': reconciliation['amount']})
                                            invoice_obj.browse(reconciliation['invoice_id'])._compute_balance()

                                        paymentids.append(payment_id.id)
                                else:
                                    reject = True;
                                    reject_cause = _('No valid structured Communication')
                    if reject:
                        reject_id = reject_obj.create({'account': parent_account,
                                                       'paymenttype': '1',
                                                       'paymentdate': transfer_date,
                                                       'structcom': communication,
                                                       'freecom': free_communication,
                                                       'name': name,
                                                       'amount': amount,
                                                       'adr1': adr1,
                                                       'adr2': adr2,
                                                       'reject_cause': reject_cause}).id
                        transfer_date = ''
                        communication = ''
                        free_communication = ''
                        reject_cause = ''
                        parent_account = ''
                        name = ''
                        adr1 = ''
                        adr2 = ''

                        rejectids.append(reject_id)
                    reject = False
                    amount = 0.0
                    transfer_date = ''
                    communication = ''
                    reject_cause = ''
                    parent_account = ''
                    name = ''
                    adr1 = ''
                    adr2 = ''
                    with_address = False

        return super(extraschool_coda, self).create({
            'name': 'CODA ' + date,
            'codadate': date,
            'codafile': vals['codafile'],
            'paymentids': [(6, 0, paymentids)],
            'rejectids': [(6, 0, rejectids)],
            'bank_account_number': bank_account,
        })
