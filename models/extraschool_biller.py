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

import smtplib
import threading
import uuid
import openerp
import openerp.release
import openerp.sql_db
import openerp.tools

# from __future__ import division
from datetime import datetime
from email.MIMEText import MIMEText

from email.MIMEMultipart import MIMEMultipart
from openerp import models, api, fields, _
from openerp.addons.extraschool.helper import extraschool_helper
from openerp.exceptions import Warning
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT)

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import time
import logging

_logger = logging.getLogger(__name__)


class extraschool_biller(models.Model):
    _name = 'extraschool.biller'
    _description = 'Biller'
    _inherit = 'mail.thread'
    _order = "id desc"

    activitycategoryid = fields.Many2many('extraschool.activitycategory', 'extraschool_biller_activity_category_rel',
                                          string='Activity Category', track_visibility='onchange')
    accrued_ids = fields.One2many('extraschool.accrued', 'biller_id')
    period_from = fields.Date('Period from')
    period_to = fields.Date('Period to')
    payment_term = fields.Date('Payment term')
    invoices_date = fields.Date('Invoices date')
    invoice_ids = fields.One2many('extraschool.invoice', 'biller_id', 'invoices')
    total = fields.Float(compute='_compute_total', string="Total", track_visibility='onchange')
    received = fields.Float(compute='_compute_received', string="Received", track_visibility='onchange')
    novalue = fields.Float(compute='_compute_novalue', string="No Value", track_visibility='onchange')
    balance = fields.Float(compute='_compute_balance', string="Balance", track_visibility='onchange')
    nbinvoices = fields.Integer(compute='_compute_nbinvoices', string="Nb of invoices", )
    other_ref = fields.Char("Ref")
    comment = fields.Text("Comment", default="")
    filename = fields.Char('filename', size=20, readonly=True)
    biller_file = fields.Binary('File', readonly=True)
    pdf_ready = fields.Boolean(string="Pdf ready", default=False)
    oldid = fields.Integer('oldid')
    reminder_journal_id = fields.Many2one(
        'extraschool.remindersjournal',
        'Reminders journal',
        ondelete='cascade',
        required=False)

    @api.multi
    def name_get(self):
        """
        Create a name for this record based on period
        :return: Textual representation for this record
        """
        res = []
        for biller in self:
            res.append((biller.id, _("Biller from {} to {}".format(
                datetime.strptime(biller.period_from, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y"),
                datetime.strptime(biller.period_to, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y")))))
        return res

    @api.depends('invoice_ids.amount_total')
    def _compute_total(self):
        """
        Compute for each biller, sum of all invoices.
        :return: None
        """
        for biller in self:
            biller.total = sum(invoice.amount_total for invoice in biller.invoice_ids)

    @api.depends('invoice_ids.amount_received')
    def _compute_received(self):
        """
        Compute amount received for each invoice
        :return: None
        """
        for biller in self:
            biller.received = sum(invoice.amount_received for invoice in biller.invoice_ids)

    @api.depends('invoice_ids.balance')
    def _compute_balance(self):
        """
        Compute balance for each invoice
        :return: None
        """
        for biller in self:
            biller.balance = sum(invoice.balance for invoice in biller.invoice_ids)

    @api.depends('invoice_ids.no_value_amount')
    def _compute_novalue(self):
        """
        Compute no value for each invoice
        :return: None
        """
        for biller in self:
            biller.novalue = sum(invoice.no_value_amount for invoice in biller.invoice_ids)

    @api.depends('invoice_ids')
    def _compute_nbinvoices(self):
        """
        Compute invoices number
        :return: None
        """
        for biller in self:
            biller.nbinvoices = len(self.invoice_ids)

    @api.multi
    def _ensure_delete_one_biller(self):
        """
        Check if only one biller is selected, raise warning otherwise
        :return: None
        """
        if len(self) > 1:
            raise Warning(_("You can delete only one biller at a time !"))

    @api.multi
    def _ensure_delete_last_biller(self):
        """
        Check if this is the last biller, raise warning otherwise
        :return: None
        """
        if self.search([]).sorted(key=lambda r: r.id)[-1].id != self.id:
            raise Warning(_("You can only delete the last biller !"))

    @api.multi
    def _unlink_invoices(self):
        """
        Delete invoices's payments reconciliation and invoices
        :return: None
        """
        count = 1
        # we use a variable because size of invoice_ids is decremented for each invoice deleted
        nb_invoices = len(self.invoice_ids)
        for invoice in self.invoice_ids:
            invoice.payment_ids.unlink()
            invoice.unlink()
            _logger.info("[{}/{}] invoices deleted".format(count, nb_invoices))
            count += 1

    @api.multi
    def unlink(self):
        """
        Delete the biller (included invoices, payments)
        :return: id of biller
        """
        self.env.invalidate_all()
        self._ensure_delete_one_biller()
        self._ensure_delete_last_biller()
        self._unlink_invoices()
        return super(extraschool_biller, self).unlink()

    @api.multi
    def mail_invoices(self):
        """
        Get invoices to send by mail
        :return: Tree and form view with invoices to send by mail
        """
        return {'name': 'Invoices',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('biller_id.id', '=', self.id),
                           ('balance', '>', 0),
                           '|', ('invoicesendmethod', '=', 'onlybymail'), ('invoicesendmethod', '=', 'emailandmail')]
                }

    @api.multi
    def email_invoices(self):
        """
        Get invoices to send by email
        :return: Tree and form view with invoices to send by email
        """
        return {'name': 'Invoices',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('biller_id.id', '=', self.id),
                           '|', ('invoicesendmethod', '=', 'onlyemail'), ('invoicesendmethod', '=', 'emailandmail')],
                'context': {"search_default_actif": 1},

                }

    @api.multi
    def all_invoices(self):
        """
        Get all biller's invoices
        :return: Tree and form view with all biller's invoices
        """
        return {'name': 'Invoices',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('biller_id.id', '=', self.id)],
                'context': {"search_default_actif": 1},
                }

    @api.multi
    def all_pdf(self):
        """
        Get all invoices's PDF
        :return: Tree and form view with all invoices's PDF
        """
        return {'name': 'Docs',
                'type': 'ir.actions.act_window',
                'res_model': 'ir.attachment',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('res_id', 'in', [i.id for i in self.invoice_ids]),
                           ('res_model', '=', 'extraschool.invoice')],
                'context': {"search_default_actif": 1},

                }

    # todo refactoring
    def get_concerned_months(self):
        """
        Get concerned months by biller
        :return: months
        """
        start_month = fields.Date.from_string(self.period_from).month
        end_months = (fields.Date.from_string(self.period_to).year - fields.Date.from_string(
            self.period_from).year) * 12 + fields.Date.from_string(self.period_to).month + 1
        months = [{'year': yr, 'month': mn} for (yr, mn) in (
            ((m - 1) / 12 + fields.Date.from_string(self.period_from).year, (m - 1) % 12 + 1) for m in
            range(start_month, end_months)
        )]

        return months

    @api.multi
    def get_from_year(self):
        """
        Get from year of biller
        :return: from year
        """
        return fields.Date.from_string(self.period_from).year

    @api.multi
    def generate_pdf(self):
        """
        Generate PDF for biller's invoices
        :return: None
        """
        # cr, uid = self.env.cr, self.env.user.id
        # threaded_report = []
        self.ensure_one()
        self._delete_pdf()
        self.pdf_ready = False
        # clear cache
        self.env.invalidate_all()
        # count = 0
        # for invoice in self.invoice_ids:
        #     count = count + 1
        #     self.env['report'].get_pdf(invoice, 'extraschool.invoice_report_layout')
        #     _logger.info("generate pdf {} count: {}".format(invoice.id, count))
        A, B, C = extraschool_helper.split_list(self.invoice_ids.ids, 3)
        A_calculation = threading.Thread(target=self._run_process, args=(self.id, A))
        B_calculation = threading.Thread(target=self._run_process, args=(self.id, B))
        C_calculation = threading.Thread(target=self._run_process, args=(self.id, C))
        A_calculation.start()
        B_calculation.start()
        C_calculation.start()

        self.pdf_ready = True
        # self.send_mail_completed()

    def _run_process(self, active_id, list_of_ids):
        with api.Environment.manage():
            with openerp.registry(self.env.cr.dbname).cursor() as new_cr:
                new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                for invoice in new_env["extraschool.invoice"].browse(list_of_ids):
                    new_env['report'].get_pdf(invoice, 'extraschool.invoice_report_layout')

    # @api.model
    # def generate_pdf_thread(self, cr, uid, thread_lock, invoices_ids, context=None):
    #     """
    #     @param self: The object pointer.
    #     @param cr: A database cursor
    #     @param uid: ID of the user currently logged in
    #     @param ids: List of IDs selected
    #     @param context: A standard dictionary
    #     """
    #     time.sleep(5)
    #     with Environment.manage():
    #         # As this function is in a new thread, i need to open a new cursor, because the old one may be closed
    #         new_cr = self.pool.cursor()
    #         new_env = Environment(new_cr, uid, context)
    #         count = 0
    #         report = new_env['report']
    #         for invoice in new_env['extraschool.invoice'].browse(invoices_ids):
    #             count = count + 1
    #             _logger.info("generate pdf %s count: %s" % (invoice.id, count))
    #             report.get_pdf(invoice, 'extraschool.invoice_report_layout')
    #
    #         thread_lock[1].acquire()
    #         thread_lock[0] -= 1
    #         if thread_lock[0] == 0:
    #             new_env['extraschool.biller'].browse(thread_lock[2]).pdf_ready = True
    #
    #         thread_lock[1].release()
    #         new_cr.commit()
    #         new_cr.close()
    #         return {}

    @api.multi
    def _delete_pdf(self):
        """
        Delete all of biller's invoices
        :return: None
        """
        self.ensure_one()
        self.env['ir.attachment'].search([('res_id', 'in', self.invoice_ids.mapped("id")),
                                          ('res_model', '=', 'extraschool.invoice')]).unlink()

    @api.multi
    def send_email(self, message):
        """
        Send an email to user who billing (billing status information)
        :param message: Message to send to user
        :return: None
        """
        email_from = "noreply@imio.be"
        email_to = self.env["res.users"].browse(self.env.uid).partner_id.email.encode('utf-8')

        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = "Support Imio - Accueil Extrascolaire"

        msg.attach(MIMEText(message))

        server = smtplib.SMTP(self.env['ir.mail_server'].search([])[0].smtp_host.encode('utf-8'),
                              self.env['ir.mail_server'].search([])[0].smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.sendmail(email_from, email_to, msg.as_string())
        server.quit()

    @api.multi
    def send_mail_error(self, error):
        """
        Send an email while an error occurred
        :param error: error occurred
        :return: None
        """
        message = """
        Cet Email automatique vous a été envoyé car il y a eu un erreur lors de la facturation (voir ci-dessous):\n
        Raison: {}\n
        """.format(error.encode('utf-8'))
        self.send_email(message)

    @api.multi
    def send_mail_completed(self):
        """
        Send an email while billing finished
        :return: None
        """
        message = "Cet Email automatique vous a été envoyé pour vous informez que votre facturier a bien été créé."
        self.send_email(message)

    # todo refactoring
    @api.multi
    def export_onyx(self):
        """
        Export biller's invoices to a file for ONYX
        (See https://www.civadis.be/index.php/297-produits-services/logiciels/finances/taxes/onyx) for information
        about ONYX.
        :return: None
        """
        self.ensure_one()
        self.env["extraschool.activity"].check_activities_on_tax_certificate()
        output = ""
        output += u"MATRICULE\tNom du Responsable\tPrénom du Responsable\tCode rue\tLibellé rue\t"
        output += u"Numéro\tBoîte\tIndex\tCode postal\tLocalité\tPays\tLangue du redevable\tCivilité\tCode rue\tLibellé rue\t"
        output += u"Numéro\tBoîte\tIndex\tCode postal\tLocalité\tDate debut\tdate fin\tCommentaires\tsepar\tN fact\tN°\tM/P\t"
        output += u"NOM\tPRENOM\tDATE DE NAISSANCE\tN° REGISTRE NATIONAL\tANNEE D'ETUDE\tDate accueil\t"
        output += u"activité\tNbr j presences\tfisc\ttotal\tquantité\n"
        total = 0
        for invoice in self.invoice_ids.sorted(lambda r: r.parentid.rn):
            export = invoice.export_onyx()
            total += export['exported_amount']
            for r in export['lines']:
                output += "%s\n" % (r)

        attachment_obj = self.env['ir.attachment']
        filename = "Facturier_du_%s_au_%s__%s_aes_onyx.txt" % (
            time.strftime('%d/%m/%Y', time.strptime(self.period_from, '%Y-%m-%d')),
            time.strftime('%d/%m/%Y', time.strptime(self.period_to, '%Y-%m-%d')), total)
        attachment_obj.create({'res_model': 'extraschool.biller',
                               'res_id': self.id,
                               'datas': output.encode('utf-8').encode('base64'),
                               'datas_fname': filename,
                               'name': filename,
                               })

    @api.multi
    def compute_discount(self):
        """
        Compute discount
        :return: None
        """
        self.ensure_one()
        for discount in self.env['extraschool.discount.version'].search([]):
            discount.discount_forfait_week(self)

    @api.multi
    def pay_all(self):
        """
        Pay all biller's invoices (create payment and reconciliation)
        :return: None
        """
        for invoice_id in self.invoice_ids:
            payment_id = self.env['extraschool.payment'].create({
                'parent_id': invoice_id.parentid.id,
                'paymentdate': self.period_to,  # This is Coda date.
                'structcom_prefix': self.activitycategoryid.payment_invitation_com_struct_prefix,
                'amount': invoice_id.balance,
                'reject_id': False,
                'comment': 'Paiement automatique',
                'activity_category_id': [(6, 0, [invoice_id.activitycategoryid.id])],
            })

            reconciliation = self.env['extraschool.payment_reconciliation'].create({'payment_id': payment_id.id,
                                                                                    'invoice_id': invoice_id.id,
                                                                                    'amount': invoice_id.balance,
                                                                                    'date': self.period_to})
            reconciliation.invoice_id._compute_balance()
