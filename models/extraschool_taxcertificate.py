# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchial - Imio (<http://www.imio.be>).
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

from odoo import models, api, fields, _
from odoo.api import Environment
from odoo.exceptions import except_orm, Warning, RedirectWarning
from odoo import tools
import threading
import time
import logging
_logger = logging.getLogger(__name__)


class extraschool_taxcertificate(models.Model):
    _name = 'extraschool.taxcertificate'
    _description = 'Taxcertificate'
    _inherit = 'mail.thread'

    title = fields.Char('Title', required=True)
    name = fields.Integer('Fiscal Year', required=True, select = True, track_visibility='onchange')
    doc_date = fields.Date('Document date', required=True, track_visibility='onchange')
    organising_power_id = fields.Many2one(
        'extraschool.organising_power',
        'Organising Power',
    )

    taxcertificate_item_ids = fields.One2many('extraschool.taxcertificate_item', 'taxcertificate_id','Details')
    pdf_ready = fields.Boolean(string="Pdf ready", default=False)

    @api.multi
    def mail_invoices(self):

        return {'name': 'Tax Certificate',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.taxcertificate_item',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('taxcertificate_id.id', '=',self.id),
                           '|',('tax_certificate_send_method','=','onlybymail'),('tax_certificate_send_method','=','emailandmail')]
            }

    @api.multi
    def email_invoices(self):

        return {'name': 'Tax Certificate',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.taxcertificate_item',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('taxcertificate_id.id', '=',self.id),
                           '|',('tax_certificate_send_method','=','onlyemail'),('tax_certificate_send_method','=','emailandmail')],
                'context': {"search_default_actif":1},

            }

    @api.model
    def create(self, vals):
        #check if already exist
        tc = self.search([('name', '=', vals['name'])])
        vals[u'organising_power_id'] = self.env['extraschool.organising_power'].search([]).mapped('id')[0]
        if len(tc):
            raise Warning(_('Taxe certificate already exist'))

        cr,uid = self.env.cr, self.env.user.id

        obj_config = self.env['extraschool.mainsettings']
        config=obj_config.browse([1])

        #UPDATE RECONCIL DATE IF NEEDED
        sql_update_reconcil_date = """
                                    update extraschool_payment_reconciliation
                                    set date = create_date
                                    where date is Null;
                                    """

        cr.execute(sql_update_reconcil_date)

        sql_concerned_invoice = """
                                    select distinct(iii.id) as id
                                            from extraschool_payment_reconciliation ppr
                                            left join extraschool_invoice iii on iii.id = ppr.invoice_id
                                            left join extraschool_payment pp on pp.id = ppr.payment_id
                                            where ppr.paymentdate BETWEEN '%s-01-01' and '%s-12-31'
                                                AND iii.balance = 0 AND (iii.reminder_fees IS NULL OR iii.reminder_fees = false)                                             
                                """ % (vals['name'], vals['name'])


        sql_concerned_attest = """
                                    select i.parentid as parentid,par.firstname as parent_firstname,
                                    par.lastname as parent_lastname,
                                    par.street as parent_street,
                                    par.zipcode as parent_zipcode,
                                    par.city as parent_city,
                                    ip.childid as childid,
                                    c.firstname as child_firstname,
                                    c.lastname as child_lastname,
                                    c.birthdate as child_birthdate,
                                    si.name as implantation,
                                    sc.name as classe, 
                                    sum(total_price - ip.no_value_amount) as amount,
                                    min(ao.occurrence_date) as period_from,
                                    max(ao.occurrence_date) as period_to,
                                    (select count(distinct(aao.occurrence_date)) as nbdays
                                    from extraschool_invoicedprestations iip
                                    left join extraschool_activityoccurrence aao on aao.id = iip.activity_occurrence_id
                                      left join extraschool_activity aa on aa.id = aao.activityid
                                    left join extraschool_invoice ii on ii.id = iip.invoiceid
                                    where invoiceid in (""" + sql_concerned_invoice + """)
                                           and aa.on_tax_certificate = true
                                           and iip.childid = ip.childid
                                    ) as nbdays
                                    from extraschool_invoicedprestations ip
                                    left join extraschool_activityoccurrence ao on ao.id = ip.activity_occurrence_id
                                      left join extraschool_activity a on a.id = ao.activityid
                                    left join extraschool_invoice i on i.id = ip.invoiceid
                                    left join extraschool_parent par on par.id = i.parentid
                                    left join extraschool_child c on c.id = ip.childid
                                    left join extraschool_schoolimplantation si on si.id = c.schoolimplantation
                                    left join extraschool_class sc on sc.id = c.classid
                                    where invoiceid in (""" + sql_concerned_invoice + """)
                                           and a.on_tax_certificate = true
                                           and prestation_date <= c.birthdate + interval '12 year'
                                    group by i.parentid,par.firstname,par.lastname,par.street,par.zipcode,par.city,ip.childid,c.firstname,c.lastname,c.birthdate,si.name,sc.name
                                    having sum(total_price - ip.no_value_amount) > 0
                                    order by si.name,sc.name,i.parentid;                                
                                """

        logging.info("Creation of tax certificates")

        cr.execute(sql_concerned_attest,(sql_concerned_invoice,sql_concerned_invoice))

        childattestations = cr.dictfetchall()

        attest_item_ids = []
        attest_item_obj = self.env['extraschool.taxcertificate_item']
        zz=1
        for attest in childattestations:
            send_method = self.env['extraschool.parent'].search([('id', '=', attest['parentid'])]).mapped('invoicesendmethod')[0].encode("UTF-8")
            attest_item_ids.append(attest_item_obj.create({'name': zz,
                                                           'parent_id': attest['parentid'],
                                                           'child_id': attest['childid'],
                                                           'nbr_day': attest['nbdays'],
                                                           'amount': attest['amount'],
                                                           'tax_certificate_send_method': send_method,
                                                           }).id)
            zz += 1

        vals['taxcertificate_item_ids'] = [(6,0,attest_item_ids)]

        taxe_certif = super(extraschool_taxcertificate, self).create(vals)
        taxe_certif.generate_pdf()

        return taxe_certif

    @api.multi
    def all_taxecertificate(self):

        return {'name': 'Attestation ficale',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.taxcertificate_item',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('taxcertificate_id.id', '=',self.id)],
                'context': {},
            }

    @api.multi
    def all_pdf(self):

        return {'name': 'Docs',
                'type': 'ir.actions.act_window',
                'res_model': 'ir.attachment',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('res_id', 'in',[i.id for i in self.taxcertificate_item_ids]),
                            ('res_model', '=', 'extraschool.taxcertificate_item')],
                'context': {"search_default_actif":1},

            }

    @api.model
    def generate_pdf_thread(self, cr, uid, thread_lock, taxe_ids, context=None):
        """
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: List of IDs selected
        @param context: A standard dictionary
        """
        time.sleep(5)
        with Environment.manage():
            #As this function is in a new thread, i need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            new_env = Environment(new_cr, uid,context)

            report = new_env['report']
            for taxe in new_env['extraschool.taxcertificate_item'].browse(taxe_ids):
                report.get_pdf(taxe ,'extraschool.tpl_taxe_certificate_wizard_report')


            thread_lock[1].acquire()
            thread_lock[0] -= 1
            if thread_lock[0] == 0:
                new_env['extraschool.taxcertificate'].browse(thread_lock[2]).pdf_ready = True

            thread_lock[1].release()
            new_cr.commit()
            new_cr.close()
            return {}

    @api.one
    def generate_pdf(self):

        cr,uid = self.env.cr, self.env.user.id
        threaded_report = []

        self.env['ir.attachment'].search([('res_id', 'in',[i.id for i in self.taxcertificate_item_ids]),
                                           ('res_model', '=', 'extraschool.taxcertificate_item')]).unlink()
        self.pdf_ready = False
        self.env.invalidate_all()

        lock = threading.Lock()
        chunk_size = int(self.env['ir.config_parameter'].get_param('extraschool.report.thread.chunk',200))

        nrb_thread = len(self.taxcertificate_item_ids)/chunk_size+(len(self.taxcertificate_item_ids)%chunk_size > 0)
        thread_lock = [len(self.taxcertificate_item_ids)/chunk_size+(len(self.taxcertificate_item_ids)%chunk_size > 0),
                        threading.Lock(),
                        self.id]
        for zz in range(0, nrb_thread):
            sub_taxes = [i.id for i in self.taxcertificate_item_ids[zz*chunk_size:(zz+1)*chunk_size]]
            if len(sub_taxes):
                thread = threading.Thread(target=self.generate_pdf_thread, args=(cr, uid, thread_lock, sub_taxes,self.env.context))
                threaded_report.append(thread)
                thread.start()


class extraschool_taxcertificate_item(models.Model):
    _name = 'extraschool.taxcertificate_item'
    _description = 'Taxcertificate item'

    name = fields.Char('Name')
    taxcertificate_id = fields.Many2one('extraschool.taxcertificate', string ='Taxe certif',ondelete='cascade', index=True)
    parent_id = fields.Many2one('extraschool.parent',  string ='Parent', required=True, select = True)
    child_id = fields.Many2one('extraschool.child',  string ='Child', required=True, select=True)
    implantation = fields.Many2one(related='child_id.schoolimplantation', invisible=True, store=True)
    niveau = fields.Many2one(related='child_id.levelid', invisible=True, store=True)
    nbr_day = fields.Integer( string ='Nbr day')
    prest_from = fields.Float('From')
    prest_to = fields.Float('To')
    amount = fields.Float('Amount')
    tax_certificate_detail_ids = fields.One2many('extraschool.tax_certificate_detail', 'tax_certificate_item_id')
    tax_certificate_send_method = fields.Char()
    annee = fields.Integer(String='Annee' , related="taxcertificate_id.name", index=True)
    organising_power_id = fields.Many2one(
        'extraschool.organising_power',
        'Organising Power',
    )


class extraschool_tax_certificate_detail(models.Model):
    _name = 'extraschool.tax_certificate_detail'
    _description = 'Tax Certificate Detail'
    _auto = False  # Disable creation of table.
    _order = ''

    tax_certificate_item_id = fields.Many2one('extraschool.taxcertificate_item', 'tax_certificate_detail_ids', select=True)
    amount = fields.Float('Amount')
    time_scan = fields.Char('time_scan')
    activity_name = fields.Char('activity_name')
    prestation_date = fields.Date('prestation_date')
    invoice_number = fields.Char('invoice_number')
    child_name = fields.Char('child_name')
    entry_exit = fields.Char('entry_exit')

    # This is the view we use.
    def init(self):
        cr = self.env.cr
        # Drop before a new view.
        tools.sql.drop_view_if_exists(cr, 'extraschool_tax_certificate_detail')

        try:
            cr.execute("""
                CREATE view extraschool_tax_certificate_detail as
                    SELECT  row_number() over() AS id,
                            tax_item.id AS tax_certificate_item_id,
                            c.lastname || ' ' || c.firstname AS child_name,
                            inv.number AS invoice_number, 
                            prest.prestation_date AS prestation_date, 
                            act.short_name AS activity_name, 
                            to_char(to_timestamp((prest.prestation_time) * 60), 'MI:SS') AS time_scan, 
                            CASE 
                                WHEN 
                                    prest.es = 'E' 
                                    THEN 'Entree' 
                                    ELSE 'Sortie' 
                                END AS entry_exit, 
                            to_char(total_price, '999.99') AS amount
                    FROM extraschool_prestationtimes AS prest
                    INNER JOIN extraschool_invoicedprestations AS inv_prest
                    ON prest.invoiced_prestation_id = inv_prest.id
                    INNER JOIN extraschool_invoice AS inv
                    ON inv.id = inv_prest.invoiceid
                    INNER JOIN extraschool_parent AS p
                    ON p.id = prest.parent_id
                    INNER JOIN extraschool_child AS c
                    ON c.id = prest.childid
                    INNER JOIN extraschool_taxcertificate_item AS tax_item
                    ON c.id = tax_item.child_id
                    INNER JOIN extraschool_activity AS act
                    ON act.id = inv_prest.activity_activity_id
                    WHERE inv_prest.invoiceid IN (	SELECT DISTINCT(inv.id) AS id
                                    FROM extraschool_payment_reconciliation AS pay_rec
                                    LEFT JOIN extraschool_invoice AS inv 
                                    ON inv.id = pay_rec.invoice_id
                                    LEFT JOIN extraschool_payment AS pay 
                                    ON pay.id = pay_rec.payment_id
                                    WHERE pay_rec.paymentdate BETWEEN '2019-01-01' AND '2019-12-31'
                                    AND inv.balance = 0 AND (inv.reminder_fees IS NULL OR inv.reminder_fees = false)) 
                                    AND act.on_tax_certificate = TRUE
                                    AND prest.prestation_date <= c.birthdate + interval '12 year'
                    ORDER BY inv.number, prest.prestation_date, act.short_name, prest.prestation_time
                    
            """)
        except:
            pass
