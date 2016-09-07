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
from openerp.exceptions import except_orm, Warning, RedirectWarning

class extraschool_coda(models.Model):
    _name = 'extraschool.coda'

    _order = 'codadate desc'
    
    name = fields.Char('Name', size=20)
    codafile = fields.Binary('CODA File')
    codadate = fields.Date('CODA Date',readonly=True)
    #amountperyear = fields.Text(compute='_compute_amountperyear', string="Amount per year")
    amount_accepted = fields.Float(compute='_compute_amount_accepted', string="Amount accepted")
    amount_rejected = fields.Float(compute='_compute_amount_rejected', string="Amount rejected")

    paymentids = fields.One2many('extraschool.payment', 'coda','Payments',readonly=True)
    rejectids = fields.One2many('extraschool.reject', 'coda','Rejects',readonly=True)

    state = fields.Selection([('todo', 'To Do'),
                              ('handled', 'Handled')],
                              'validated', required=True, default='todo'
                              )
    @api.one
    def validate(self):
        print "validate"

        if self.state == 'todo':
            self.state = 'handled'
                
    @api.depends('paymentids')
    def _compute_amount_accepted (self):       
        for r in self:
            r.amount_accepted = sum(p.amount for p in r.paymentids)

    @api.depends('paymentids')
    def _compute_amount_rejected (self):       
        for r in self:
            r.amount_rejected = sum(rej.amount for rej in r.rejectids)
            
    def format_comstruct(self,comstruct):
        return ('+++%s/%s/%s+++' % (comstruct[0:3],comstruct[3:7],comstruct[7:12]))
    @api.model
    def create(self, vals):  
        #to do refactoring suite api V8
        cr = self.env.cr
        paymentids = []
        rejectids = []
        if not vals['codafile']:
            raise Warning(_('No coda file!','ERROR: No CODA File !!!'))
        lines = unicode(base64.decodestring(vals['codafile']), 'windows-1252', 'strict').split('\n')
        bankaccount = lines[1][5:21]
        codadate = '20'+lines[0][9:11]+'-'+lines[0][7:9]+'-'+lines[0][5:7]
        coda_obj = self.env['extraschool.coda']
        coda_ids = coda_obj.search([('codadate','=',codadate)]).ids
        if coda_ids:
            raise Warning(_('CODA already imported !!!'))
        activitycategory_obj = self.env['extraschool.activitycategory']
        invoice_obj = self.env['extraschool.invoice']
        reminder_obj = self.env['extraschool.reminder']
        payment_obj = self.env['extraschool.payment']
        payment_reconciliation_obj = self.env['extraschool.payment_reconciliation']
        reject_obj = self.env['extraschool.reject']
        activitycategory_ids=activitycategory_obj.search([('bankaccount', '=', bankaccount)]).ids
        if lines[0][127] !='2':
            raise Warning(_('ERROR: Wrong CODA version !!!'))
        if (activitycategory_ids == 0):
            raise Warning(_('ERROR: The account number in this CODA file is not used in this application !!!'))
        reject = False
        amount = 0.0
        transfertdate=''
        communication=''
        free_communication=''
        rejectcause=''
        parentaccount=''
        name=''
        adr1=''
        adr2=''
        withaddress=False
        for line in lines:
            if len(line) > 0:                
                if line[0]=='3':
                    withaddress=True        
        for line in lines:
            if len(line) > 0:                
                if line[0]=='2':
                    if line[1]=='1':
                        amount=eval(line[31:44]+'.'+line[44:47])
                        transfertdate=codadate                      
                        if line[62]=='1':
                            communication=self.format_comstruct(line[65:77])                            
                        else:
                            reject=True
                            rejectcause=_('No structured Communication')
                            free_communication=line[62:112]
                    else:
                        if (line[1]=='3') and (amount > 0.0) and transfertdate:
                            parentaccount=line[10:26]
                            name=line[47:73]                        
                if (line[0]=='3') and (line[1]=='2') and (len(name) > 1):
                    adr1=line[10:45]
                    adr2=line[45:80]
                
                if ((withaddress == True) and (len(adr1) > 0)) or ((withaddress == False) and (len(name) > 1)):                    
                    if reject == False:
                        cr.execute('select invoicecomstructprefix from extraschool_activitycategory')
                        prefixes=cr.dictfetchall()
                        prefixfound=False                    
                        for prefix in prefixes:
                                if (len(prefix['invoicecomstructprefix']) > 0) and (len(communication) > len(prefix['invoicecomstructprefix'])):
                                    if communication[3:3+len(prefix['invoicecomstructprefix'])] == prefix['invoicecomstructprefix']:
                                        prefixfound=True
                                        _prefix = prefix['invoicecomstructprefix']
                        if prefixfound:          
                            invoice=invoice_obj.search([('structcom', '=', communication)])                      
                            if len(invoice.ids) == 1:
                                if invoice.balance < amount:
                                    reject=True
                                    rejectcause=_('Amount greather than invoice balance')
                                else:            
                                    payment_id = payment_obj.create({'parent_id': invoice.parentid.id,
                                                                  'paymentdate': transfertdate,
                                                                  'structcom_prefix': _prefix,
                                                                  'structcom':communication,
                                                                  'paymenttype':'1',
                                                                  'account':parentaccount,
                                                                  'name':name,
                                                                  'adr1':adr1,
                                                                  'adr2':adr2,
                                                                  'amount': amount})
                                                                            
                                    payment_reconciliation_obj.create({'payment_id' : payment_id.id,
                                                                           'invoice_id' : invoice.id,
                                                                           'amount' : amount})
                                    invoice._compute_balance()
                                    paymentids.append(payment_id.id)                                    
                            else:
                                reject=True
                                rejectcause=_('No valid structured Communication')
                        else:
                            #Rappels
                            cr.execute('select remindercomstructprefix from extraschool_activitycategory')
                            prefixes=cr.dictfetchall()
                            prefixfound=False
                            for prefix in prefixes:
                                if prefix['remindercomstructprefix']:
                                    if len(communication) > len(prefix['remindercomstructprefix']):
                                        if communication[3:3+len(prefix['remindercomstructprefix'])] == prefix['remindercomstructprefix']:
                                            prefixfound=True
                                            _prefix = prefix['remindercomstructprefix']
                            if prefixfound:
                                reminder=reminder_obj.search([('structcom', '=', communication)])
                                if reminder.ensure_one():
                                    totaldue = sum(invoice.balance for invoice in reminder.concerned_invoice_ids)
                                    print '--------------------'
                                    print amount
                                    print totaldue
                                    for invoice in reminder.concerned_invoice_ids:
                                        print '*'
                                        print invoice.balance
                                        print invoice.parentid.name
                                    print '---------------------'
                                    if amount != totaldue:
                                        reject=True
                                        rejectcause=_('A reminder has been found but the amount is not corresponding to balances of invoices')
                                    else:
                                        for invoice in reminder.concerned_invoice_ids:
                                            payment_id = payment_obj.create({'parent_id': invoice.parentid.id,
                                                                  'paymentdate': transfertdate,
                                                                  'structcom_prefix': _prefix,
                                                                  'structcom':communication,
                                                                  'paymenttype':'1',
                                                                  'account':parentaccount,
                                                                  'name':name,
                                                                  'adr1':adr1,
                                                                  'adr2':adr2,
                                                                  'amount': invoice.balance})
                                                                            
                                            payment_reconciliation_obj.create({'payment_id' : payment_id.id,
                                                                           'invoice_id' : invoice.id,
                                                                           'amount' : invoice.balance})
                                            invoice._compute_balance()
                                            paymentids.append(payment_id.id)         
                            else:
                                #Pre-paiements
                                cr.execute('select payment_invitation_com_struct_prefix from extraschool_activitycategory')
                                prefixes=cr.dictfetchall()
                                prefixfound=False
                                for prefix in prefixes:
                                    if prefix['payment_invitation_com_struct_prefix']:
                                        if len(communication) > len(prefix['payment_invitation_com_struct_prefix']):
                                            if communication[3:3+len(prefix['payment_invitation_com_struct_prefix'])] == prefix['payment_invitation_com_struct_prefix']:
                                                prefixfound=True
                                                _prefix = prefix['payment_invitation_com_struct_prefix']
                                if prefixfound:
                                        parentid = int(communication[7:11]+communication[12:15])
                                        if len(self.env['extraschool.parent'].search([('id', '=',parentid)])) == 0:
                                            reject=True;
                                            print communication
                                            rejectcause=_('Parent not found')
                                        else:                              
                                            payment_id = payment_obj.create({'parent_id': parentid,
                                                                      'paymentdate': transfertdate,
                                                                      'structcom_prefix': _prefix,
                                                                      'structcom':communication,
                                                                      'paymenttype':'1',
                                                                      'account':parentaccount,
                                                                      'name':name,
                                                                      'adr1':adr1,
                                                                      'adr2':adr2,
                                                                      'amount': amount})
                                            
                                            for reconciliation in payment_id._get_reconciliation_list(parentid,prefix['payment_invitation_com_struct_prefix'],1,amount):
                                                payment_reconciliation_obj.create({'payment_id' : payment_id.id,
                                                                               'invoice_id' : reconciliation['invoice_id'],
                                                                               'amount' : reconciliation['amount']})
                                                invoice_obj.browse(reconciliation['invoice_id'])._compute_balance()
                                                
                                            paymentids.append(payment_id.id)
                                else:
                                    reject=True;
                                    rejectcause=_('No valid structured Communication')
                    if reject:
                        reject_id = reject_obj.create({'account':parentaccount,
                                                       'paymenttype':'1',
                                                       'paymentdate':transfertdate,
                                                       'structcom':communication,
                                                       'freecom': free_communication,
                                                       'name':name,
                                                       'amount':amount,
                                                       'adr1':adr1,
                                                       'adr2':adr2,
                                                       'rejectcause':rejectcause}).id
                        rejectids.append(reject_id)
                    reject = False
                    amount = 0.0
                    transfertdate=''
                    communication=''
                    rejectcause=''
                    parentaccount=''
                    name=''
                    adr1=''
                    adr2=''
        return super(extraschool_coda, self).create({'name':'CODA '+codadate,'codadate':codadate,'codafile':vals['codafile'],'paymentids':[(6,0,paymentids)],'rejectids':[(6,0,rejectids)]})

    def com_struct_builder(self,prefix, val):
        #padding 
        val = val.zfill(7)
        comstruct=prefix+str(val)
        numverif=str(int(comstruct) % 97)
        if (int(numverif)==0):
            numverif='97'
        if (len(numverif)==1):
            numverif='0'+numverif
            
        return comstruct+numverif
