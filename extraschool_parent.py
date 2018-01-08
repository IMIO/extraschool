# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014 
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
import re

from openerp import models, api, fields, _
from openerp.api import Environment
import lbutils
from datetime import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning

class extraschool_parent(models.Model):
    _name = 'extraschool.parent'
    _description = 'Parent'
    _inherit = 'mail.thread'

    @api.depends('firstname','lastname')
    def _name_compute(self):
        for record in self:
            record.name = '%s %s'  % (record.lastname, record.firstname)

    def _search_fullname(self, operator, value):
        return ['|',('firstname', operator, value),('lastname', operator, value)]

    def onchange_name(self, cr, uid, ids, lastname,firstname):
        v={}
        if lastname:
            if firstname:
                v['name']='%s %s' % (lastname, firstname)
            else:
                v['name']=lastname
        return {'value':v}

    def onchange_address(self, cr, uid, ids, street,city):
        v={}
        if street:
            if city:
                v['streetcode']=lbutils.genstreetcode(street+city)
            else:
                v['streetcode']=lbutils.genstreetcode(street)
        return {'value':v}

    def return_action_to_open(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current parent """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'extraschool', context['xml_id'], context=context)
            res['context'] = context
            res['domain'] = [('parentid','=', ids[0])]
            return res
        return False

    def _compute_totalinvoiced (self):
        cr = self.env.cr
        for record in self:
            cr.execute('select sum(amount_total) from extraschool_invoice where parentid=%s',(record.id,))
            record.totalinvoiced = cr.fetchall()[0][0]


    def _compute_totalreceived (self):
        cr = self.env.cr
        for record in self:
            cr.execute('select sum(amount_received) from extraschool_invoice where parentid=%s',(record.id,))
            record.totalreceived = cr.fetchall()[0][0]

    def _compute_totalbalance (self):
        cr = self.env.cr
        for record in self:
            cr.execute('select sum(balance) from extraschool_invoice where parentid=%s and (huissier = False or huissier is Null)',(record.id,))
            invoice = cr.fetchall()[0][0]
            invoice = invoice if invoice else 0.0
            cr.execute('select sum(fees_amount) from extraschool_reminder where parentid=%s', (record.id,))
            reminder = cr.fetchall()[0][0]
            reminder = reminder if reminder else 0.0
            record.totalbalance = invoice + reminder

    def _compute_totalhuissier (self):
        cr = self.env.cr
        for record in self:
            cr.execute('select sum(balance) from extraschool_invoice where parentid=%s and huissier = True',(record.id,))
            record.totalhuissier = cr.fetchall()[0][0]

    # def _compute_total_reminder_fees (self):
    #     cr = self.env.cr
    #     for record in self:
    #         cr.execute('select sum(fees_amount) from extraschool_reminder where parentid=%s',(record.id,))
    #         record.total_reminder_fees = cr.fetchall()[0][0]

    name = fields.Char(compute='_name_compute',string='FullName', search='_search_fullname', size=100)
    rn = fields.Char('RN', track_visibility='onchange')
    firstname = fields.Char('FirstName', size=50,required=True, track_visibility='onchange')
    lastname = fields.Char('LastName', size=50,required=True, track_visibility='onchange')
    street = fields.Char('Street', size=50,required=True, track_visibility='onchange')
    zipcode = fields.Char('ZipCode', size=6,required=True, track_visibility='onchange')
    city = fields.Char('City', size=50,required=True, track_visibility='onchange')
    housephone = fields.Char('House Phone', size=20, track_visibility='onchange')
    workphone = fields.Char('Work Phone', size=20, track_visibility='onchange')
    gsm = fields.Char('GSM', size=20, track_visibility='onchange')
    email = fields.Char('Email', size=100, track_visibility='onchange')
    invoicesendmethod = fields.Selection((('emailandmail','By mail and email'),
                                          ('onlyemail','Only by email'),
                                          ('onlybymail','Only by mail')),
                                         'Invoice send method',required=True, default='onlybymail', track_visibility='onchange')
    streetcode = fields.Char('Street code', size=50, track_visibility='onchange')
    child_ids = fields.One2many('extraschool.child', 'parentid','childs', readonly=True)
    invoice_ids = fields.One2many('extraschool.invoice', 'parentid','invoices', track_visibility='onchange')
    remindersendmethod = fields.Selection((('emailandmail','By mail and email'),
                                           ('onlyemail','Only by email'),
                                           ('onlybymail','Only by mail')),
                                          'Reminder send method',required=True, default='onlybymail', track_visibility='onchange')
    one_subvention_type = fields.Selection((('sf','operating grants'),
                                            ('sdp','positive differentiation grants')),
                                           required=True, default='sf', track_visibility='onchange')
    reminder_ids = fields.One2many('extraschool.reminder', 'parentid','reminders', readonly=True)
    totalinvoiced = fields.Float(compute='_compute_totalinvoiced', string="Total invoiced")
    totalreceived = fields.Float(compute='_compute_totalreceived', string="Total received")
    totalbalance = fields.Float(compute='_compute_totalbalance', string="Total balance")
    totalhuissier = fields.Float(compute='_compute_totalhuissier', string="Total huissier", track_visibility='onchange')
    payment_ids = fields.One2many('extraschool.payment','parent_id')
    payment_status_ids = fields.One2many('extraschool.payment_status_report','parent_id')
    last_import_date = fields.Datetime('Import date', readonly=True, track_visibility='onchange')
    modified_since_last_import = fields.Boolean('Modified since last import')
    isdisabled = fields.Boolean('Disabled', track_visibility='onchange')
    oldid = fields.Integer('oldid')
    nbr_actif_child = fields.Integer(compute='_compute_nbr_actif_child',string='Nbr actif child', store = True, track_visibility='onchange')
    comment = fields.Text('Comment', track_visibility='onchange')

    @api.multi
    def testwizard(self):
        print "test wizard"
        test = self.env['extraschool.payment_wizard'].create({
            'payment_date': datetime.now(),
            'amount': 0,
            'state': 'init',
            'parent_id': self.id,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'extraschool.payment_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': test.id,
            'views': [(False, 'form')],
            'target': 'new',
        }


    @api.multi
    def get_invoice(self):
        return {'name': 'Factures',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('parentid', '=',self.id),]
            }
        # return {'name': 'Paiements',
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'extraschool.payment_invoice',
        #         'tree_view_id': 'extraschool_payment_parent_tree',
        #         'view_type': 'form',
        #         'view_mode': 'tree,form',
        #         'nodestroy': False,
        #         'target': 'current',
        #         'limit': 50000,
        #         'domain': [('parent_id', '=',self.id),]
        #     }

    @api.multi
    def refund(self):
        # Compute the solde.
        solde = self.payment_status_ids.solde
        solde = round(solde,2)

        if solde == 0.00:
            raise Warning(_("There is no refund possible."))

        now = datetime.now().strftime("%Y-%m-%d")

        # Get the activity and the next invoice number.
        activity_id = self.env['extraschool.activitycategory'].search([], limit = 1)
        next_invoice_num = activity_id.get_next_comstruct('refund',datetime.now().year)

        payment_id = self.env['extraschool.payment'].create({
                                                            'solde': -solde,
                                                            'amount': -solde,
                                                            'parent_id': self.id,
                                                            'paymentdate': now,
                                                            'paymenttype': '2',
                                                            })

        self.env['extraschool.invoice']._compute_balance()

        # reconciliation_id = self.env['extraschool.payment_reconciliation'].create({'payment_id': payment_id.id,
        #                                                                            '',
        #                                                                            '',
        #                                                                            '',})


    def email_validation(self,email):
        if re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) != None:
            return True
        else:
            return False

    @api.depends('child_ids')
    def _compute_nbr_actif_child(self):
        for record in self:
            record.nbr_actif_child = len(record.child_ids.filtered(lambda r: r.isdisabled == False))

    @api.multi
    def wizard_action(self):
        return {
            'name': 'My Window',
            'domain': [],
            'res_model': 'extraschool.parent_fusion_wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {},
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        # todo replace check par une contraite
        parent_obj = self.env['extraschool.parent']
        parents=parent_obj.search([('firstname', 'ilike', vals['firstname'].strip()),
                                   ('lastname', 'ilike', vals['lastname'].strip()),
                                   ])

        if vals['email'] != False and vals['email'] != '' and vals['email'] != ' ':
            emails = vals['email'].split(',')
            for email in emails :
                if (not self.email_validation(email)):
                    print "vals['email']" , vals['email']
                    raise Warning("E-mail format invalid.")

        return super(extraschool_parent, self).create(vals)

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
            'context': {'parent_id' : ids[0]}
        }

    @api.multi
    def write(self, vals):
        fields_to_find = set(['firstname',
                              'lastname',
                              'street',
                              'zipcode',
                              'city',
                              'housephone',
                              'workphone',
                              'gsm',
                              'email',
                              ])

        if fields_to_find.intersection(set([k for k,v in vals.iteritems()])):
            vals['modified_since_last_import'] = True

        if 'email' in vals and vals['email'] != False:
            emails = vals['email'].split(',')
            for email in emails :
                if (not self.email_validation(email)):
                    raise Warning("E-mail format invalid.")

        return super(extraschool_parent,self).write(vals)

    @api.one
    def unlink(self):
        self.isdisabled = True

    def get_prepaid_comstruct(self, categ):
        com_struct_prefix_str = categ.payment_invitation_com_struct_prefix
        com_struct_id_str = str(self.id).zfill(7)
        com_struct_check_str = str(long(com_struct_prefix_str+com_struct_id_str) % 97).zfill(2)
        com_struct_check_str = com_struct_check_str if com_struct_check_str != '00' else '97'


        return self.env['extraschool.payment'].format_comstruct('%s%s%s' % (com_struct_prefix_str,com_struct_id_str,com_struct_check_str))
