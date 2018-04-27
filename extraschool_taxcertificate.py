from openerp import models, api, fields, _
from openerp.api import Environment
from openerp.exceptions import except_orm, Warning, RedirectWarning

import threading
import time

class extraschool_taxcertificate(models.Model):
    _name = 'extraschool.taxcertificate'
    _description = 'Taxcertificate'
    _inherit = 'mail.thread'

    def _get_activity_category_id(self):
        return self.env['extraschool.activitycategory'].search([]).filtered('id').id

    name = fields.Integer('Fiscal Year', required=True, select = True, track_visibility='onchange')
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity category', required=True, default=_get_activity_category_id, track_visibility='onchange')
    doc_date = fields.Date('Document date', required=True, track_visibility='onchange')

    taxcertificate_item_ids = fields.One2many('extraschool.taxcertificate_item', 'taxcertificate_id','Details')
    pdf_ready = fields.Boolean(string="Pdf ready", default=False)

    @api.model
    def create(self, vals):
        #check if already exist
        tc = self.search([('name', '=', vals['name']),
                          ('activity_category_id.id', '=', vals['activity_category_id']),
                          ])
        if len(tc):
            raise Warning(_('Taxe certificate already exist'))

        cr,uid = self.env.cr, self.env.user.id

        obj_config = self.env['extraschool.mainsettings']
        config=obj_config.browse([1])
        activitycat= vals['activity_category_id']

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
                                                AND iii.balance = 0 AND iii.last_reminder_id IS NULL                                            
                                """ % (vals['name'], vals['name'])


        sql_concerned_attest = """
                                    select i.parentid as parentid,par.firstname as parent_firstname,par.lastname as parent_lastname,par.street as parent_street,par.zipcode as parent_zipcode,par.city as parent_city,ip.childid as childid,c.firstname as child_firstname,c.lastname as child_lastname,c.birthdate as child_birthdate,si.name as implantation,sc.name as classe, sum(total_price) as amount,min(ao.occurrence_date) as period_from,max(ao.occurrence_date) as period_to,
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
                                    having sum(total_price) > 0
                                    order by si.name,sc.name,i.parentid;                                
                                """

        print "sql_concerned_attest : %s" % sql_concerned_attest

        cr.execute(sql_concerned_attest,(sql_concerned_invoice,sql_concerned_invoice))

        childattestations = cr.dictfetchall()

        attest_item_ids = []
        attest_item_obj = self.env['extraschool.taxcertificate_item']
        zz=1
        for attest in childattestations:
            attest_item_ids.append(attest_item_obj.create({'name': zz,
                                                           'parent_id': attest['parentid'],
                                                           'child_id': attest['childid'],
                                                           'nbr_day': attest['nbdays'],
                                                           'amount': attest['amount']}).id)
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
            print "start thread for ids : %s" % (sub_taxes)
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
    amount = fields.Float(string ='Amount')
