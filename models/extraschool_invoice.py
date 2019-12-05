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
from openerp.api import Environment
import openerp.addons.decimal_precision as dp
from openerp import tools
import datetime
import time
from datetime import date, datetime, timedelta as td
import calendar
import re
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)

import logging
_logger = logging.getLogger(__name__)

class extraschool_invoice(models.Model):
    _name = 'extraschool.invoice'
    _description = 'invoice'
    _inherit = 'mail.thread'

    @api.multi
    def name_get(self):
        res = []
        for invoice in self:
            res.append((invoice.id, _("Invoice from %s to %s") % (
                datetime.strptime(invoice.period_from, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y"),
                datetime.strptime(invoice.period_to, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y"))))
        return res

    name = fields.Char('Name', size=20,readonly=True, default='Facture', track_visibility='onchange')
    schoolimplantationid = fields.Many2one('extraschool.schoolimplantation', 'School implantation', required=False,readonly=True, index=True, track_visibility='onchange')
    classid = fields.Many2one('extraschool.class', 'Class', required=False, domain="[('schoolimplantation','=',schoolimplantationid)]", index=True, track_visibility='onchange')
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=False, index = True, track_visibility='onchange')
    invoicesendmethod = fields.Selection(related="parentid.invoicesendmethod", store=True, track_visibility='onchange')
    number = fields.Integer('Number',readonly=True, track_visibility='onchange')
    structcom = fields.Char('Structured Communication', size=50, readonly=True, required=True, track_visibility='onchange')
    amount_total = fields.Float(string='Amount', digits_compute=dp.get_precision('extraschool_invoice'), readonly=True, store=True, track_visibility='onchange')
    amount_received = fields.Float( string='Received', digits_compute=dp.get_precision('extraschool_invoice'), readonly=True,store=True, track_visibility='onchange')
    balance = fields.Float(digits_compute=dp.get_precision('extraschool_invoice'), string='Balance',readonly=True, store=True, track_visibility='onchange')
    no_value = fields.Float('No value',default=0.0,readonly=True, track_visibility='onchange')
    discount = fields.Float('Discount',readonly=True, track_visibility='onchange')
    biller_id = fields.Many2one('extraschool.biller', 'Biller', required=False,ondelete='cascade',readonly=True, index=True, track_visibility='onchange')
    filename = fields.Char('filename', size=20,readonly=True,  invisible= True, track_visibility='onchange')
    invoice_file = fields.Binary('File', readonly=True, invisible= True, track_visibility='onchange')
    payment_ids = fields.One2many('extraschool.payment_reconciliation', 'invoice_id','Payments', track_visibility='onchange')
    invoice_line_ids = fields.One2many('extraschool.invoicedprestations', 'invoiceid','Details', track_visibility='onchange')
    refound_line_ids = fields.One2many('extraschool.refound_line', 'invoiceid','Refound', track_visibility='onchange')
    oldid = fields.Char('oldid', size=20, track_visibility='onchange')
    activitycategoryid = fields.Many2many('extraschool.activitycategory', 'extraschool_invoice_activity_category_rel', store=True, auto_join=True, track_visibility='onchange')
    # activitycategoryid = fields.Many2one(related='biller_id.activitycategoryid', store=True, auto_join=True, track_visibility='onchange')
    period_from = fields.Date(related='biller_id.period_from', index=True, track_visibility='onchange')
    period_to = fields.Date(related='biller_id.period_to', index=True, track_visibility='onchange')
    payment_term = fields.Date('Payment term', track_visibility='onchange')
    comment = fields.Text("Comment",default="", track_visibility='onchange')
    last_reminder_id = fields.Many2one('extraschool.reminder', 'Last reminder',readonly=True, index = True, track_visibility='onchange')
    reminder_fees = fields.Boolean('Reminder fees', default=False, track_visibility='onchange')
    huissier = fields.Boolean('Huissier', default=False, track_visibility='onchange')
    fees_huissier = fields.Float('Fees Huissier', default=0.0, track_visibility='onchange')
    tag = fields.Many2one('extraschool.invoice_tag', 'Tag', readonly=True, track_visibility='onchange')

    no_value_amount = fields.Float(
        string='No value amount',
        default=0.00,
        readonly=True,
    )

    _sql_constraints = [
        ('structcom_uniq', 'unique(structcom)',
            "The structured communication is already distributed. Please contact support-aes@imio.be"),
    ]

    @api.multi
    def _compute_balance(self):
        for invoice in self:

            total = 0 if len(invoice.invoice_line_ids) == 0 else sum(line.total_price for line in invoice.invoice_line_ids)
            total = 0 if total < 0.0001 else total
            reconcil = 0 if len(invoice.payment_ids) == 0 else sum(reconcil_line.amount for reconcil_line in invoice.payment_ids)
            reconcil = 0 if reconcil < 0.0001 else reconcil
            balance = total - reconcil - self.no_value_amount
            balance = 0 if balance < 0.0001 else balance
            balance = round(balance,5) # MiCo used this to resolve a balance problem (hannut 21/08/2017)
            invoice.write({'amount_total' : total,
                           'amount_received' : reconcil,
                           'balance' : balance
                           })

    @api.multi
    def get_today(self):
        return datetime.datetime.now().strftime("%y-%m-%d")

    @api.multi
    def get_payment_term_str(self):
        return self.payment_term.strftime("%y-%m-%d")

    @api.multi
    def is_echue(self):
        return True if self.payment_term < fields.Datetime.now() else False

    @api.multi
    def is_echue_and_not_reminder(self):
        return False if self.last_reminder_id and not self.reminder_fees else True

    @api.multi
    def get_balance(self, activity_category_id):
        if not self.invoice_line_ids.filtered(lambda r: r.activity_occurrence_id.activity_category_id.id):
            return self.balance
        else:
            return sum(invoiced_line.total_price - invoiced_line.no_value_amount for invoiced_line in self.invoice_line_ids.filtered(
                lambda r: r.activity_occurrence_id.activity_category_id.id == activity_category_id))

    @api.multi
    def reconcil(self):
        payment_obj = self.env['extraschool.payment']
        payment_reconcil_obj = self.env['extraschool.payment_reconciliation']
        organizing_power = self.env['extraschool.organising_power'].search([])[0]
        for invoice in self:
            invoice._compute_balance()
            if invoice.balance != 0.00:
                # todo: Check if the biller (invoices_date) <= today(). Do a cron to launch this method everyday.
                # If there is a dominant payment
                if (organizing_power.dominant_payment_activity_category_id):
                    payment_ids = payment_obj.search([('parent_id','=',invoice.parentid.id),
                                                      ('solde','>',0),
                                                      ]).sorted(key=lambda r: r.paymentdate)

                    count = 0
                    solde = invoice.balance - invoice.no_value_amount

                    while count < len(payment_ids) and solde > 0:
                        amount = solde if payment_ids[count].solde >= solde else payment_ids[count].solde
                        payment_reconcil_obj.create({'payment_id': payment_ids[count].id,
                                                     'invoice_id': invoice.id,
                                                     'amount': amount,
                                                     'date': fields.Date.today(),
                                                     })
                        solde -= amount
                        count += 1
                else:
                    for invoice_category in invoice.activitycategoryid:
                        payments = payment_obj.search([('parent_id','=',invoice.parentid.id),
                                                       ('activity_category_id', '=', invoice_category.id),
                                                       ('solde','>',0),
                                                       ]).sorted(key=lambda r: r.paymentdate)

                        zz = 0

                        solde = invoice.get_balance(invoice_category.id)

                        while zz < len(payments) and solde > 0:
                            amount = solde if payments[zz].solde >= solde else payments[zz].solde
                            payment_reconcil_obj.create({'payment_id': payments[zz].id,
                                                         'invoice_id': invoice.id,
                                                         'amount': amount,
                                                         'date': fields.Date.today(),
                                                         })
                            solde -= amount
                            zz += 1

                invoice._compute_balance()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.multi
    def full_no_value(self):
        # Put the totality of the invoice in no value.
        try:
            self.ensure_one()
            for line in self.invoice_line_ids:
                line.write({
                    'no_value_amount': line.total_price,
                })
            # This needs to be last. Otherwise an error appear on the total amount.
            self.write({
                'no_value_amount': self.amount_total
            })
            self._compute_balance()
        except:
            raise Warning(_("An error occured, please contact an adminsitrator"))

    @api.multi
    def cancel_and_invoice_after(self):
        self.ensure_one()
        if self.balance == self.amount_total:
            self.full_no_value()
            for line in self.invoice_line_ids:
                line.prestation_ids.write({
                    'invoiced_prestation_id': None,
                })
        else:
            raise Warning(_("You cannot cancel an invoice that recieved payments"))

    @api.multi
    def cancel(self):
        self.ensure_one()
        if self.balance == self.amount_total:
            self.full_no_value()
        else:
            raise Warning(_("You cannot cancel an invoice that recieved payments"))

    def get_concerned_short_name(self):
        res = []

        for line in self.invoice_line_ids:
            if line.activity_activity_id.short_name not in res:
                res.append(line.activity_activity_id.short_name)

        return sorted(res)


    def get_concerned_child(self):
        res = []

        for line in self.invoice_line_ids:
            if line.childid not in res:
                res.append(line.childid)

        res.sort(key=lambda r: r.name)

        return res

    @api.multi
    def get_invoice_calendar(self, child_id = None, exclued_free=False):
        """
        Build a calendar of activities by child for this invoice
        :param child_id: The id of the child
        :param exclued_free: True if you want to exclued free activities. False by default
        :return: Dictionnary of concerned month with the quantity of presences by day and name of activities.
        """
        concened_months = self.biller_id.get_concerned_months()
        for month in concened_months:
            month['days'] = calendar.monthcalendar(month['year'], month['month'])
            month['activity'] = self.get_concerned_short_name()
            month['quantity'] = []

            if exclued_free:
                activity_to_remove = []
                for activity in month['activity']:
                    if self.isfree(activity):
                        activity_to_remove.append(activity)

                if activity_to_remove:
                    for activity in activity_to_remove:
                        month['activity'].remove(activity)

            zz=0
            for week in month['days']:
                month['quantity'].append([])

                for d in week:
                    d={'day_id': d,
                       'quantity': [],
                       }
                    for activity in month['activity']:
                        d['quantity'].append(sum(self.invoice_line_ids.filtered(lambda r: r.childid.id == child_id
                                                                                and r.prestation_date == '%s-%02d-%02d' % (month['year'],month['month'],d['day_id'])
                                                                                and r.activity_activity_id.short_name == activity
                                                                                ).mapped('quantity')))
                    month['quantity'][zz].append(d)

                zz+=1

        return concened_months

    def isfree(self, activity_name):
        for line in self.invoice_line_ids.filtered(lambda r: r.activity_activity_id.short_name == activity_name):
            if line.total_price == 0.00:
                return True
        return False

    @api.one
    def export_onyx_but(self):
        self.export_onyx()

    def export_onyx_child_change(self,invoicedline, saved_child, reset_nbr_jour = False):
        p = re.compile(r"([^0-9^,]*|.*\b11 novembre\b)[\s,]*([0-9]*)[\/\s]*([a-zA-Z]*[0-9]*)[\/\s]*([a-zA-Z]*)$")

        if reset_nbr_jour:
            saved_child['nbr_jour'] = 1 if invoicedline.activity_activity_id.on_tax_certificate else 0
            saved_child['nbr_jour_printed'] = False

        saved_child['saved_activity'] = invoicedline.activity_activity_id.short_name
        saved_child['saved_child'] = invoicedline.childid.name
        saved_child['rn'] = invoicedline.childid.rn if invoicedline.childid.rn else ''
        saved_child['lastname'] = invoicedline.childid.lastname
        saved_child['firstname'] = invoicedline.childid.firstname
        saved_child['birthdate'] = time.strftime('%d/%m/%Y',time.strptime(invoicedline.childid.birthdate,'%Y-%m-%d'))
        saved_child['level'] = invoicedline.childid.levelid.leveltype if invoicedline.childid.levelid.leveltype else ''
        saved_child['child_class'] = invoicedline.childid.classid.name if invoicedline.childid.classid.name else ''
        saved_child['child_id'] = invoicedline.childid.id
        saved_child['street_code'] = invoicedline.placeid.street_code
        saved_child['amount'] = invoicedline.total_price
        saved_child['fisc_amount'] = invoicedline.total_price if invoicedline.activity_activity_id.on_tax_certificate else 0
        saved_child['invoice_num'] = invoicedline.invoiceid.number
        saved_child['inv_date'] = invoicedline.prestation_date
        saved_child['inv_date_str'] = time.strftime('%d/%m/%Y',time.strptime(invoicedline.prestation_date,'%Y-%m-%d'))
        try:
            saved_child['splited_place_street'] = p.findall(invoicedline.placeid.street)
        except TypeError:
            raise Warning(_("There is no street on the place."))
        saved_child['place'] = invoicedline.placeid
        saved_child['quantity'] = invoicedline.quantity

        return saved_child

    def export_onyx(self):
        res = []
        #split street
        p = re.compile(r"([^0-9^,]*|.*\b11 novembre\b)[\s,]*([0-9]*)[\/\s]*([a-zA-Z]*[0-9]*)[\/\s]*([a-zA-Z]*[0-9]*)$")

        splited_street = p.findall(self.parentid.street)
        if len(splited_street) == 0:
            splited_street = [(splited_street,'','','','')]
        #split rue ecole


        activities = self.env["extraschool.activity"].search([]).mapped('name')

        #statique part
        format_str = ""
        format_str += "%7s\t" # matricule sur 7 char
        format_str += "%s\t" # Nom du redev
        format_str += "%s\t" # prenom du redev
        format_str += "%s\t" # code rue (facultatif)
        format_str += "%s\t" # libellé rue
        format_str += "%s\t" # num
        format_str += "%s\t" # boite
        format_str += "%s\t" # index
        format_str += "%04d\t" # code post sur 4 pos avec leading 0
        format_str += "%s\t" # localité
        format_str += "%s\t" # pays
        format_str += "%s\t" # langue defaut F
        format_str += "%s\t" # civilité
        #adresse ecole
        format_str += "%s\t" # code rue (facultatif)
        format_str += "%s\t" # libellé rue
        format_str += "%s\t" # num
        format_str += "%s\t" # boite
        format_str += "%s\t" # index
        format_str += "%04d\t" # code post sur 4 pos avec leading 0
        format_str += "%s\t" # localité
        format_str += "%s\t" # from
        format_str += "%s\t" # to
        format_str += "%s\t" # comment
        #separator
        format_str += "%s\t" #separator
        #dynamique part
        format_str += "%s\t" # Num de fact
        format_str += "%s\t" # id de l'enfant
        format_str += "%s\t" # niveau de l'enfant (M/P)
        format_str += "%s\t" # Nom de l'enfant
        format_str += "%s\t" # prenom de l'enfant
        format_str += "%s\t" # birtdate de l'enfant
        format_str += "%7s\t" # matricule sur 7 char
        format_str += "%s\t" # class de l'enfant
        format_str += "%s\t" # date de présence
#        format_str += "%s\t" # debug
        format_str += "%s\t" # activity
        format_str += "%s\t" # nbr j présences
        format_str += "%.2f\t" # fisc amount
        format_str += "%.2f\t" # amount
        format_str += "%.2f" # quantity


        format_activities_str = ""
        for activity in activities:
            format_activities_str += "%s\t"

        str_line = ""
        zz = 0
        amount = 0.0
        breaking = False

        saved_child = {}
        saved_child['saved_activity'] = "+++++++++"
        saved_child['saved_child'] = ""
        saved_child['rn'] = ""
        saved_child['lastname'] = ""
        saved_child['firstname'] = ""
        saved_child['birthdate'] = ""
        saved_child['level'] = ""
        saved_child['child_class'] = ""
        saved_child['child_id'] = ""
        saved_child['street_code'] = ""
        saved_child['nbr_jour'] = 0
        saved_child['nbr_jour_printed'] = False
        saved_child['amount'] = 0.0
        saved_child['fisc_amount'] = 0.0
        saved_child['invoice_num'] = ""
        saved_child['inv_date'] = ""
        saved_child['inv_date_str'] = ""
        saved_child['splited_place_street'] = []
        saved_child['place'] = ''
        saved_child['quantity'] = 0.0


        total = 0
        lines_ids = self.invoice_line_ids.filtered(lambda r: r.total_price > 0.0001).sorted(key=lambda r: "%s%s%s%s%s" % (r.childid.rn, r.childid.name, r.placeid.street_code, r.prestation_date, r.activity_activity_id.short_name))

        if len(lines_ids) == 0:
            return {'lines': res,
                    'exported_amount': total,
                     }

        for invoicedline in lines_ids:
            if zz == 0:
                saved_child = self.export_onyx_child_change(invoicedline, saved_child, True)
                str_line = ""

            if (zz > 0 and (saved_child['saved_child'] != invoicedline.childid.name or saved_child['inv_date'] != invoicedline.prestation_date or saved_child['saved_activity'] != invoicedline.activity_activity_id.short_name))  or zz == len(self.invoice_line_ids) -1:
                str_line = format_str % (self.parentid.rn if self.parentid.rn else "", # Matricule.
                                        self.parentid.lastname,
                                        self.parentid.firstname,
                                        '', # code rue
                                        splited_street[0][0], # libellé rue
                                        splited_street[0][1], # num
                                        splited_street[0][2], # boite
                                        splited_street[0][3], # index
                                        int(self.parentid.zipcode), #code post
                                        self.parentid.city,
                                        '', # pays
                                        'F', # Langue
                                        '', # civilité
                                        saved_child['street_code'], #code rue place
                                        saved_child['splited_place_street'][0][0], # libellé rue
                                        saved_child['splited_place_street'][0][1], # num
                                        saved_child['splited_place_street'][0][2], # boite
                                        saved_child['splited_place_street'][0][3], # index
                                        int(saved_child['place'].zipcode),
                                        saved_child['place'].city,
                                        time.strftime('%d/%m/%Y',time.strptime(self.biller_id.period_from,'%Y-%m-%d')),
                                        time.strftime('%d/%m/%Y',time.strptime(self.biller_id.period_to,'%Y-%m-%d')),
                                        '',
                                        '#', # comment
                                        saved_child['invoice_num'],
                                        saved_child['child_id'],
                                        saved_child['level'],
                                        saved_child['lastname'],
                                        saved_child['firstname'],
                                        saved_child['birthdate'],
                                        saved_child['rn'],
                                        saved_child['child_class'],
                                        saved_child['inv_date_str'],
                                        saved_child['saved_activity'],
                                        1 if saved_child['nbr_jour'] >= 1 and not saved_child['nbr_jour_printed'] else 0,
                                        saved_child['fisc_amount'],
                                        saved_child['amount'],
                                        saved_child['quantity']
                                        )
                total+=saved_child['amount']
                if saved_child['nbr_jour']:
                    saved_child['nbr_jour_printed'] = True

                res.append(str_line)

            #break on child, date or activity_short_name
            if saved_child['saved_child'] != invoicedline.childid.name or saved_child['inv_date'] != invoicedline.prestation_date or saved_child['saved_activity'] != invoicedline.activity_activity_id.short_name:
                #if break on child, date
                if saved_child['saved_child'] != invoicedline.childid.name or saved_child['inv_date'] != invoicedline.prestation_date:
                    saved_child = self.export_onyx_child_change(invoicedline, saved_child, True)
                    str_line = ""
                else:
                    saved_child = self.export_onyx_child_change(invoicedline,saved_child)
                    str_line = ""
                    if invoicedline.activity_activity_id.on_tax_certificate:
                        saved_child['nbr_jour'] += 1
            else:
                if zz > 0:
                    if invoicedline.activity_activity_id.on_tax_certificate:
                        saved_child['nbr_jour'] += 1
                        saved_child['fisc_amount'] += invoicedline.total_price
                    saved_child['amount'] += invoicedline.total_price

            zz+=1

        if str_line == "":
            str_line = format_str % (self.parentid.rn or '',
            self.parentid.lastname,
            self.parentid.firstname,
            '', # code rue
            splited_street[0][0], # libellé rue
            splited_street[0][1], # num
            splited_street[0][2], # boite
            splited_street[0][3], # index
            int(self.parentid.zipcode), #code post
            self.parentid.city,
            '', # pays
            'F', # Langue
            '', # civilité
            saved_child['street_code'], #code rue place
            saved_child['splited_place_street'][0][0], # libellé rue
            saved_child['splited_place_street'][0][1], # num
            saved_child['splited_place_street'][0][2], # boite
            saved_child['splited_place_street'][0][3], # index
            int(saved_child['place'].zipcode),
            saved_child['place'].city,
            time.strftime('%d/%m/%Y',time.strptime(self.biller_id.period_from,'%Y-%m-%d')),
            time.strftime('%d/%m/%Y',time.strptime(self.biller_id.period_to,'%Y-%m-%d')),
            '',
            '#', # comment
            saved_child['invoice_num'],
            saved_child['child_id'],
            saved_child['level'],
            saved_child['lastname'],
            saved_child['firstname'],
            saved_child['birthdate'],
            saved_child['rn'] or '',
            saved_child['child_class'] or '',
            saved_child['inv_date_str'],
            saved_child['saved_activity'],
            1 if saved_child['nbr_jour'] >= 1 and not saved_child['nbr_jour_printed'] else 0,
            saved_child['fisc_amount'],
            saved_child['amount'],
            saved_child['quantity'],
                                        )
            total+=saved_child['amount']
            res.append(str_line)

        return {'lines': res,
                'exported_amount': total,
                 }

    @api.multi
    def set_tag(self, context):
        invoice_tag_obj = self.env['extraschool.invoice_tag']
        if not context['tag']:
            self.tag = None # Plus de tag.
        elif context['tag'] == 'huissier':
            self.tag = invoice_tag_obj.search([('name', '=', 'Huissier')]).id  # Huissier.
        elif context['tag'] == 'plan_de_paiement':
            self.tag = invoice_tag_obj.search([('name', '=', 'Plan de paiement')]).id  # Plan de paiement.
        else:
            self.tag = invoice_tag_obj.search([('name', '=', 'Bloquer')]).id  # Bloquer.

    @api.multi
    def cancel_payment(self):
        self.amount_received = 0.0
        for payment in self.payment_ids:
            payment.unlink()

        self._compute_balance()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.multi
    def add_no_value(self):
        return {
            'name': "No value wizard",
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'extraschool.no_value_wizard',
            'src_model': 'extraschool.invoice',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'context': {}
        }


class extraschool_invoice_tag(models.Model):
    _name = 'extraschool.invoice_tag'
    _description = 'Different tag can be used but they all block the process of this invoice. No reminder and so on.'

    name = fields.Char('Name of the tag')
    invoice_ids = fields.One2many('extraschool.invoice', 'tag', 'invoice_id')
