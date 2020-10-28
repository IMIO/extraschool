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

from openerp import models, api, fields, _
from openerp.api import Environment
from datetime import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning
from _abcoll import Sequence


class extraschool_activitycategory(models.Model):
    _name = 'extraschool.activitycategory'
    _description = 'Activities categories'

    name = fields.Char('Name', size=50)

    organising_power_id = fields.Many2one(comodel_name='extraschool.organising_power', string='Organising Power',
                                          required=True)
    accrued_ids = fields.One2many(comodel_name='extraschool.accrued', inverse_name='activity_category_id')

    childpositiondetermination = fields.Selection((('byparent', 'by parent'),
                                                   ('byparent_without_la_ribambelle', 'by parent without la ribambelle'),
                                                   ('byparentwp', 'by parent (only childs with prestations)'),
                                                   ('byparent_nb_childs', 'by parent (position replaced by nbr childs'),
                                                   ('byparent_nb_childs_wp',
                                                    'by parent (position replaced by nbr childs with prestations'),
                                                   ('byaddress', 'by address'),
                                                   ('byaddresswp', 'by address (only childs with prestations)'),
                                                   ('byaddress_nb_childs',
                                                    'by address (position replaced by nbr childs'),
                                                   ('byaddress_nb_childs_wp',
                                                    'by address (position replaced by nbr childs with prestations'),
                                                   ('by_address_by_activity',
                                                    'by address and by activity (only childs with prestations'),
                                                   ), 'Child position determination', required=True)

    activities = fields.One2many(comodel_name='extraschool.activity', inverse_name='category_id', string='Activities')
    placeids = fields.Many2many(comodel_name='extraschool.place', relation='extraschool_activitycategory_place_rel',
                                column1='activitycategory_id',
                                column2='place_id', string='Schoolcare place')

    priorityorder = fields.Integer('Priority order')
    invoicecomstructprefix = fields.Char('Invoice Comstruct prefix', size=3, required=True)
    invoicelastcomstruct = fields.Integer('Last Invoice structured comunication number')
    invoiceemailaddress = fields.Char('Invoice email address', size=50)
    invoiceemailsubject = fields.Char('Invoice email subject', size=50)
    invoiceemailtext = fields.Text('Invoice email text')
    invoice_comment = fields.Text('Invoice comment')
    invoice_comment2 = fields.Text('Invoice comment 2')
    remindercomstructprefix = fields.Char('Reminder Comstruct prefix', size=3, required=True)
    reminderlastcomstruct = fields.Integer('Last Reminder structured comunication number')
    reminderemailaddress = fields.Char('Reminder email address', size=50)
    reminderemailsubject = fields.Char('Reminder email subject', size=50)
    reminderemailtext = fields.Text('Reminder email text')
    reminer_type_ids = fields.One2many(comodel_name='extraschool.remindertype', inverse_name='activity_category_id',
                                       string='Reminder type')

    bankaccount = fields.Char('Bank account')
    bank_bic = fields.Char('Bank BIC')
    bank_address = fields.Char('Bank address')
    bank_zip = fields.Char('Bank zip')
    bank_city = fields.Char('Bank city')

    taxcertificatetemplate = fields.Char('Tax Certificate Template', size=50)
    tax_certificate_code = fields.Char()

    invoice_report_id = fields.Many2one(comodel_name='extraschool.report', string='Invoice report')
    invoice_detail_report_id = fields.Many2one(comodel_name='extraschool.report', string='Invoice detail report')
    biller_report_id = fields.Many2one(comodel_name='extraschool.report', string='Biller report')
    qrcode_report_id = fields.Many2one(comodel_name='extraschool.report', string='QRCode report')
    payment_invitation_report_id = fields.Many2one(comodel_name='extraschool.report',
                                                   string='Payment invitation report')
    payment_invitation_email_subject = fields.Char('Payment invitation Email subject')
    payment_invitation_com_struct_prefix = fields.Char('Payment invitation Comstruct prefix', size=3, required=True)
    payment_invitation_courrier_text = fields.Text('Payment invitation courrier text')
    logo = fields.Binary()
    logo_reminder = fields.Binary()
    slogan = fields.Char('Slogan', size=50)
    sequence_ids = fields.One2many(comodel_name='extraschool.activitycategory.sequence',
                                   inverse_name='activity_category_id', string='Sequences')
    max_school_implantation = fields.Integer()
    date_college = fields.Date(default=datetime.now())

    def check_invoice_prefix(self, invoicecomstructprefix):
        res = {'return_val': True,
               'msg': ''}
        # search for activity category that have invoicecomstructprefix = payment_invitation_com_struct_prefix or remindercomstructprefix = payment_invitation_com_struct_prefix
        if len(self.search(['|', ('payment_invitation_com_struct_prefix', '=', invoicecomstructprefix),
                            ('remindercomstructprefix', '=', invoicecomstructprefix)])):
            res = {'return_val': False,
                   'msg': "It's not possible to update the activity_categ because there are other activity category with the same prefix used for pre-paid or reminder "}
        if len(self.env['extraschool.payment'].search([('structcom_prefix', '=', invoicecomstructprefix), ])):
            res = {'return_val': False,
                   'msg': "It's not possible to update the activity_categ because there are payment with the old invoice prefix"}

        return res

    def check_pay_invit_prefix(self, payment_invitation_com_struct_prefix):
        res = {'return_val': True,
               'msg': ''}
        # search for activity category that have invoicecomstructprefix = payment_invitation_com_struct_prefix or remindercomstructprefix = payment_invitation_com_struct_prefix
        if len(self.search(['|', ('invoicecomstructprefix', '=', payment_invitation_com_struct_prefix),
                            ('remindercomstructprefix', '=', payment_invitation_com_struct_prefix)])):
            res = {'return_val': False,
                   'msg': "It's not possible to update the activity_categ because there are other activity category with the same prefix used for invoicing or reminder"}
        if len(self.env['extraschool.payment'].search(
            [('structcom_prefix', '=', payment_invitation_com_struct_prefix), ])):
            res = {'return_val': False,
                   'msg': "It's not possible to update the activity_categ because there are payment with the old pre-paid prefix"}
        return res

    def check_reminder_prefix(self, remindercomstructprefix):
        res = {'return_val': True,
               'msg': ''}
        # search for activity category that have invoicecomstructprefix = payment_invitation_com_struct_prefix or remindercomstructprefix = payment_invitation_com_struct_prefix
        if len(self.search(['|', ('invoicecomstructprefix', '=', remindercomstructprefix),
                            ('payment_invitation_com_struct_prefix', '=', remindercomstructprefix)])):
            res = {'return_val': False,
                   'msg': "It's not possible to update the activity_categ because there are other activity category with the same prefix used for invoicing or pre-paid"}
        if len(self.env['extraschool.payment'].search([('structcom_prefix', '=', remindercomstructprefix), ])):
            res = {'return_val': False,
                   'msg': "It's not possible to update the activity_categ because there are payment with the old reminder prefix"}
        return res

        return res

    @api.multi
    def write(self, vals):
        for activity_categ in self:
            if 'invoicecomstructprefix' in vals:
                res = activity_categ.check_invoice_prefix(vals['invoicecomstructprefix'])
                if not res['return_val']:
                    raise Warning(res['msg'])
            if 'remindercomstructprefix' in vals:
                res = activity_categ.check_reminder_prefix(vals['remindercomstructprefix'])
                if not res['return_val']:
                    raise Warning(res['msg'])
            if 'payment_invitation_com_struct_prefix' in vals:
                res = activity_categ.check_pay_invit_prefix(vals['payment_invitation_com_struct_prefix'])
                if not res['return_val']:
                    raise Warning(res['msg'])

            super(extraschool_activitycategory, activity_categ).write(vals)

        return True

    @api.multi
    def get_sequence(self, type, year):
        """
        Get a sequence for this activity category, by type and year
        :param type: invoice or reminder
        :param year: desired year
        :return: sequence
        """
        self.ensure_one()
        sequence_id = self.sequence_ids.search([('type', '=', type),
                                                ('year', '=', year),
                                                ('activity_category_id', '=', self.id),
                                                ])
        if not sequence_id:
            # sequence doesn't exist, look for previous year seq to copy it
            sequence_id = self.sequence_ids.search([('type', '=', type),
                                                    ('year', '=', year - 1)]).sequence
            if not sequence_id:
                sequence_id = self.env['ir.sequence'].create({'name': "%s - %s - %s" % (self.name, type, year),
                                                              'active': True,
                                                              'prefix': "%s" % (("%s" % year)[-2:]),
                                                              'padding': 5})

            sequence_id = self.env["extraschool.activitycategory.sequence"].create({
                "name": "{} - {} - {}".format(self.name.encode('utf8'), type, year),
                "activity_category_id": self.id,
                "year": year,
                "type": type,
                "sequence": sequence_id.id
            })

        return sequence_id.sequence

    @api.multi
    def get_next_sequence_id(self, sequence, type):
        self.ensure_one()
        com_struct_id_str = sequence.next_by_id()
        if type == 'invoice':
            if self.env['extraschool.invoice'].search([], order='number DESC', limit=1).number >= int(
                com_struct_id_str):
                return self.get_next_sequence_id(sequence)
        return com_struct_id_str

    @api.multi
    def get_next_comstruct(self, type, year, sequence_id=False):
        # Added a refund comstruct.
        if type == 'refund':
            next_id = self.env['extraschool.invoice'].search([('structcom', 'like', '+++000')], order='number DESC',
                                                             limit=1).number
            next_id = 1 if not next_id else next_id + 1
            # It will always start with 000 and the rest is the date of the creation.
            return {"num": next_id,
                    "com_struct": '+++000/%s/%s+++' % (datetime.now().strftime("%m%d"), datetime.now().strftime("%Y"),),
                    }
        if not sequence_id:
            sequence_id = self.get_sequence(type, year)

        com_struct_id_str = sequence_id.next_by_id()

        if type == 'reminder':
            com_struct_prefix_str = self.remindercomstructprefix

        if type == 'invoice':
            com_struct_prefix_str = self.invoicecomstructprefix

        com_struct_prefix_str = com_struct_prefix_str.zfill(3)
        com_struct_id_str = ("%s" % (com_struct_id_str)).zfill(7)
        com_struct_check_str = str(long(com_struct_prefix_str + com_struct_id_str) % 97).zfill(2)
        com_struct_check_str = com_struct_check_str if com_struct_check_str != '00' else '97'

        comstruct = '%s%s%s' % (com_struct_prefix_str, com_struct_id_str, com_struct_check_str)

        return {"num": com_struct_id_str,
                "com_struct": '+++%s/%s/%s+++' % (comstruct[0:3], comstruct[3:7], comstruct[7:12]),
                }

    @api.model
    def update_seq(self):
        year = datetime.now().year

        get_sequence = self.env['extraschool.activitycategory.sequence'].search([('year', '=', year)])

        # If there isn't any sequence with this year's date.
        if not get_sequence:
            for categ in self.search([]):
                types = [{'type': 'invoice',
                          'lastcomstruct': categ.invoicelastcomstruct},
                         {'type': 'reminder',
                          'lastcomstruct': categ.reminderlastcomstruct},
                         ]
                for type in types:
                    sequence_id = self.env['ir.sequence'].sudo().create(
                        {'name': "%s - %s - %s" % (categ.name, type['type'], year),
                         'active': True,
                         'prefix': "%s" % (("%s" % (year))[-2:]),
                         'padding': 5,
                         'number_next': type['lastcomstruct'] if type['lastcomstruct'] > 0 else 1})

                    categ_sequence_id = categ.sequence_ids.create(
                        {'name': "%s - %s - %s" % (categ.name, type['type'], year),
                         'activity_category_id': categ.id,
                         'year': "%s" % (year),
                         'type': type['type'],
                         'sequence': sequence_id.id})

    @api.model
    def create(self, vals):
        res = self.check_pay_invit_prefix(vals['payment_invitation_com_struct_prefix'])
        if not res['return_val']:
            raise Warning(res['msg'])
        res = self.check_pay_invit_prefix(vals['payment_invitation_com_struct_prefix'])
        if not res['return_val']:
            raise Warning(res['msg'])
        res = self.check_pay_invit_prefix(vals['payment_invitation_com_struct_prefix'])
        if not res['return_val']:
            raise Warning(res['msg'])

        res = super(extraschool_activitycategory, self).create(vals)

        return res


class extraschool_activitycategory_sequence(models.Model):
    _name = 'extraschool.activitycategory.sequence'
    _description = 'Activities categories sequences'

    name = fields.Char('Name', size=50)
    activity_category_id = fields.Many2one('extraschool.activitycategory', required=True)
    year = fields.Integer('Year', required=True)
    type = fields.Selection((('invoice', 'Invoice'), ('reminder', 'Reminder')), string='Type', required=True)
    sequence = fields.Many2one('ir.sequence', required=True)
