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
from openerp.api import Environment
from datetime import date, datetime, timedelta as td
from dateutil.relativedelta import relativedelta
import datetime
from math import *
from pyPdf import PdfFileWriter, PdfFileReader
from openerp.exceptions import except_orm, Warning, RedirectWarning
import threading
import logging
_logger = logging.getLogger(__name__)


class extraschool_invoice_wizard(models.TransientModel):
    _name = 'extraschool.invoice_wizard'
    _schoolimplantationids = []

    def _get_defaultfrom(self):
        #to do remove it when test is finished
        cr,uid = self.env.cr, self.env.user.id
        cr.execute('select max(prestation_date) as prestation_date from extraschool_invoicedprestations')
        rec=cr.dictfetchall()[0]
        try:
            fromdate=datetime.datetime.strptime(rec['prestation_date'], '%Y-%m-%d').date()
            frommonth=fromdate.month+1
            fromyear=fromdate.year
            if frommonth == 13:
                frommonth = 12
                fromyear = fromyear +1
            strfrommonth=str(frommonth)
            if len(strfrommonth) == 1:
                strfrommonth='0'+strfrommonth
            return str(fromyear)+'-'+strfrommonth+'-01'
        except:
            return str(datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,1))

    def _get_defaultto(self):
        cr,uid = self.env.cr, self.env.user.id
        cr.execute('select max(prestation_date) as prestation_date from extraschool_invoicedprestations')
        lastdate = cr.dictfetchall()[0]['prestation_date']
        if lastdate and (lastdate < datetime.datetime.now().strftime("%Y-%m-%d")):
            todate=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,1)+relativedelta(months=1)-relativedelta(days=1)
        else:
            month=datetime.datetime.now().month
            if month == 12:
                month=1
            else:
                month=month+1
            todate=datetime.date(datetime.datetime.now().year,month,1)-datetime.timedelta(1)

        return str(todate)


    @api.one
    def _get_defaultinvdate(self):
        invdate=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)+datetime.timedelta(1)
        self.invoice_date = str(invdate)

    @api.one
    def _get_defaultinvterm(self):
        termdate=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)+datetime.timedelta(16)
        self.invoice_term = str(termdate)

    def _get_all_schoolimplantation(self):
        school_implantation_ids = self.env['extraschool.schoolimplantation'].search([]).mapped('id')
        return school_implantation_ids

    def _get_status(self):
        return True if self.env['extraschool.biller'].search([('in_creation', '=', True)]) else False

    schoolimplantationid = fields.Many2many(comodel_name='extraschool.schoolimplantation',
                               relation='extraschool_invoice_wizard_schoolimplantation_rel',
                               column1='invoice_wizard_id',
                               column2='schoolimplantation_id', default=_get_all_schoolimplantation, readonly=True)
    activitycategory = fields.Many2many(comodel_name='extraschool.activitycategory',
                                        relation='extraschool_invoice_wizard_activity_category_rel', column1='invoice_wizard_id',
                                        column2='activity_category_id', string='activity category')
    period_from = fields.Date('Period from', required=True, default=_get_defaultfrom, help='Date où l\'on va commencer la facturation')
    period_to = fields.Date('Period to', required=True, default=_get_defaultto, help='Date où l\'on va terminer la facturation')
    invoice_date = fields.Date('invoice date', required=True, default=_get_defaultto)
    invoice_term = fields.Date('invoice term', required=True, default=_get_defaultto)
    name = fields.Char('File Name', size=16, readonly=True)
    invoices = fields.Binary('File', readonly=True)
    state = fields.Selection([('init', 'Init'),
                              ('compute_invoices', 'Compute invoices')],
                             'State', required=True, default='init'
                             )
    isready = fields.Boolean(default=_get_status)
    warning_smartphone = fields.Char('WARNING',
                                 default="Attention, il y a un ou plusieurs smartphone(s) qui n'a / n'ont pas transmis. Vérifier avant de générer votre facturier ! ",
                                 readonly=True)
    warning_visibility = fields.Boolean(track_visibility='onchange')
    check_manual = fields.Boolean(default=True)
    check_registration = fields.Boolean(default=True)
    check_prestation = fields.Boolean(default=True)
    check_invoice = fields.Boolean(default=True)
    generate_pdf = fields.Boolean(default=True)

########################################################################################################################
#   HELPER to the invoicing and output to the user what needs to be done before invoicing.
########################################################################################################################

    @api.onchange('activitycategory', 'period_from', 'period_to')
    @api.multi
    def check_all(self):
        """
        Method that unite all checks before pushing the button for invoicing.
        Instead of having a warning during the invoicing, it shows before (and still during in case of errors).
        :return: None
        """
        smartphone_ids = self.env['extraschool.smartphone'].search([])
        self.warning_visibility = False
        for smartphone in smartphone_ids :
            if not smartphone.lasttransmissiondate > self.period_from:
                self.warning_visibility = True

        self.check_manual = self._check_manual_encodage()
        self.check_registration = self._check_registration()

        if self.activitycategory:
            self.check_prestation = self._check_prestation()
            self.check_invoice = self._check_invoice()

    @api.multi
    def _check_invoice(self):
        """
        Check if there are any invoices to to compute.
        :return: False if no invoices to compute. True if so.
        """
        sql_check_presta_to_invoice = """select count(*) as to_invoice_count
                                    from extraschool_prestationtimes ept
                                    left join extraschool_child c on ept.childid = c.id
                                    where ept.prestation_date between %s and %s
                                        and verified = True
                                        and invoiced_prestation_id is NULL
                                        and activity_category_id IN %s
                                        and c.schoolimplantation in %s
                                ;"""

        self.env.cr.execute(sql_check_presta_to_invoice, (self.period_from, self.period_to, tuple(self.activitycategory.ids), tuple(self.schoolimplantationid.ids),))
        to_invoice_count = self.env.cr.dictfetchall()

        if not to_invoice_count[0]['to_invoice_count']:
            return False
        else:
            return True

    @api.multi
    def _check_prestation(self):
        """
        Check if all prestation have been verified
        :return: False if prestation to be verified. True if not.
        """
        sql_check_verified = """select count(*) as verified_count
                                    from extraschool_prestationtimes ept
                                    left join extraschool_child c on ept.childid = c.id
                                    where ept.prestation_date between %s and %s
                                        and verified = False
                                        and activity_category_id IN %s
                                        and c.schoolimplantation in %s 
                                ;"""

        self.env.cr.execute(sql_check_verified, (self.period_from, self.period_to, tuple(self.activitycategory.ids), tuple(self.schoolimplantationid.ids),))
        verified_count = self.env.cr.dictfetchall()

        if verified_count[0]['verified_count']:
            return False
        else:
            return True

    @api.multi
    def _check_manual_encodage(self):
        """
        Check if manual scan needs to be validated
        :return: False if so. True if not.
        """
        manuel_encodage_ids = self.env['extraschool.prestation_times_encodage_manuel'].search([('state', '!=', 'validated'),
                                                                                               ('date_of_the_day', '>=', self.period_from),
                                                                                               ('date_of_the_day', '<=', self.period_to),])
        if len(manuel_encodage_ids):
            return False
        else:
            return True

    @api.multi
    def _check_registration(self):
        """
        Check if registration needs to be validated
        :return: False if so. True if not.
        """
        child_reg_ids = self.env['extraschool.child_registration'].search([('state', '!=', 'validated'),
                                                                            '|',
                                                                            '&',('date_from', '>=', self.period_from),
                                                                                ('date_from', '<=', self.period_to),
                                                                            '&',('date_to', '>=', self.period_from),
                                                                                ('date_to', '<=', self.period_to),
                                                                                ])

        if len(child_reg_ids):
            return False
        else:
            return True

########################################################################################################################
#   Start of the invoicing.
########################################################################################################################
    def _compute_invoices(self):
        cr,uid = self.env.cr, self.env.user.id

    def get_sql_position_querry(self):
        sql = {'byparent' : """(select min(id) 
                                from extraschool_childposition
                                where position = (select count(*) + 1
                                 from extraschool_child ec 
                                 where  i.parentid = ec.parentid
                                    and ec.id <> ip.childid
                                    and ec.birthdate <= (select birthdate from extraschool_child where id = ip.childid)
                                    and ec.rn <> (select rn from extraschool_child where id = ip.childid)
                                    and ec.isdisabled = False
                                    ))
                            """,
               'byparentwp' : """(select min(cp.id) 
                                from extraschool_childposition cp
                                where position = (select count(distinct ep.childid) + 1
                                 from extraschool_prestationtimes ep
                                 left join extraschool_child ec on ep.childid = ec.id
                                 left join extraschool_activityoccurrence aao on aao.id = ep.activity_occurrence_id
                                 left join extraschool_activity aa on aa.id = aao.activityid   
                                 where  ep.parent_id = i.parentid 
                                    and (
                                          (
                                            tarif_group_name is null and  
                                            ep.activity_occurrence_id = ip.activity_occurrence_id
                                          ) or
                                          ( 
                                            tarif_group_name is not null 
                                            and tarif_group_name = aa.tarif_group_name 
                                            and ep.prestation_date = ip.prestation_date)
                                          
                                        )
                                    and invoiced_prestation_id is not NULL
                                    and ep.childid <> ip.childid
                                    and ec.birthdate <= (select birthdate from extraschool_child where id = ip.childid)
                                    and ec.isdisabled = False
                                    )
                                    -
                                    (select count(distinct ep.childid)
                                     from extraschool_prestationtimes ep
                                     left join extraschool_child ec on ep.childid = ec.id
                                     left join extraschool_activityoccurrence aao on aao.id = ep.activity_occurrence_id
                                     left join extraschool_activity aa on aa.id = aao.activityid   
                                     where  ep.parent_id = i.parentid 
                                        and (
                                              (
                                                tarif_group_name is null and  
                                                ep.activity_occurrence_id = ip.activity_occurrence_id
                                              ) or
                                              ( 
                                                tarif_group_name is not null 
                                                and tarif_group_name = aa.tarif_group_name 
                                                and ep.prestation_date = ip.prestation_date)
                                              
                                            )
                                        and invoiced_prestation_id is not NULL
                                        and ep.childid > ip.childid
                                        and ec.birthdate = (select birthdate from extraschool_child where id = ip.childid)
                                        and ec.isdisabled = False
                                        ) 
                                    )
                            """,
                'byparent_nb_childs' : """(select min(id) 
                                from extraschool_childposition
                                where position = (select count(*)
                                 from extraschool_child ec 
                                 where  i.parentid = ec.parentid
                                 and ec.isdisabled = False
                                    ))
                            """,

                'byparent_nb_childs_wp' : """(select min(id) 
                                from extraschool_childposition
                                where position = (select count(distinct childid)
                                 from extraschool_prestationtimes ep
                                 left join extraschool_child ec on ep.childid = ec.id
                                 left join extraschool_activityoccurrence aao on aao.id = ep.activity_occurrence_id
                                 left join extraschool_activity aa on aa.id = aao.activityid   
                                 where  ep.parent_id = i.parentid 
                                    and (
                                          (
                                            tarif_group_name is null and  
                                            ep.activity_occurrence_id = ip.activity_occurrence_id
                                          ) or
                                          ( 
                                            tarif_group_name is not null 
                                            and tarif_group_name = aa.tarif_group_name 
                                            and ep.prestation_date = ip.prestation_date)
                                          
                                        )
                                    and invoiced_prestation_id is not NULL
                                    and ec.isdisabled = False
                            """,

               'byaddress' : """(select min(id)
                                    from extraschool_childposition
                                    where position = (select count(*) + 1
                                     from extraschool_child ec
                                     left join extraschool_parent pp on pp.id = ec.parentid
                                     where  pp.streetcode = p.streetcode
                                        and ec.id <> ip.childid
                                        and ec.birthdate <= (select birthdate from extraschool_child where id = ip.childid)
                                        and ec.isdisabled = False
                                        ))
                            """,
               'byaddresswp' : """(select min(cp.id) 
                                from extraschool_childposition cp
                                where position = (select count(distinct ep.childid) + 1
                                 from extraschool_prestationtimes ep
                                 left join extraschool_child ec on ep.childid = ec.id
                                 left join extraschool_parent pp on pp.id = ep.parent_id
                                 left join extraschool_activityoccurrence aao on aao.id = ep.activity_occurrence_id
                                 left join extraschool_activity aa on aa.id = aao.activityid   
                                 where  pp.streetcode = p.streetcode 
                                    and (
                                          (
                                            tarif_group_name is null and  
                                            ep.activity_occurrence_id = ip.activity_occurrence_id
                                          ) or
                                          ( 
                                            tarif_group_name is not null 
                                            and tarif_group_name = aa.tarif_group_name 
                                            and ep.prestation_date = ip.prestation_date)
                                          
                                        )
                                    and invoiced_prestation_id is not NULL
                                    and ep.childid <> ip.childid
                                    and ec.birthdate <= (select birthdate from extraschool_child where id = ip.childid)
                                    and ec.isdisabled = False
                                    )
                                    -
                                    (select count(distinct ep.childid)
                                     from extraschool_prestationtimes ep
                                     left join extraschool_child ec on ep.childid = ec.id
                                     left join extraschool_parent pp on pp.id = ep.parent_id
                                     left join extraschool_activityoccurrence aao on aao.id = ep.activity_occurrence_id
                                     left join extraschool_activity aa on aa.id = aao.activityid   
                                     where  pp.streetcode = p.streetcode 
                                        and (
                                              (
                                                tarif_group_name is null and  
                                                ep.activity_occurrence_id = ip.activity_occurrence_id
                                              ) or
                                              ( 
                                                tarif_group_name is not null 
                                                and tarif_group_name = aa.tarif_group_name 
                                                and ep.prestation_date = ip.prestation_date)
                                              
                                            )
                                        and invoiced_prestation_id is not NULL
                                        and ep.childid > ip.childid
                                        and ec.birthdate = (select birthdate from extraschool_child where id = ip.childid)
                                        and ec.isdisabled = False
                                        ) 
                                    )
                            """,
               'by_address_by_activity': """(select min(cp.id) 
                         from extraschool_childposition cp
                         where position = (select count(distinct ep.childid) + 1
                          from extraschool_prestationtimes ep
                          left join extraschool_child ec on ep.childid = ec.id
                          left join extraschool_parent pp on pp.id = ep.parent_id
                          left join extraschool_activityoccurrence aao on aao.id = ep.activity_occurrence_id
                          left join extraschool_activity aa on aa.id = aao.activityid   
                          where  pp.streetcode = p.streetcode 
                             and (
                                   (
                                     tarif_group_name is null and  
                                     (ep.activity_occurrence_id = ip.activity_occurrence_id
                                     or
                                     ip.activity_activity_id = (select activityid from extraschool_activityoccurrence where id = ep.activity_occurrence_id)
                                     )
                                   ) or
                                   ( 
                                     tarif_group_name is not null 
                                     and tarif_group_name = aa.tarif_group_name 
                                     and ep.prestation_date = ip.prestation_date)

                                 )
                             and invoiced_prestation_id is not NULL
                             and ep.childid <> ip.childid
                             and ec.birthdate <= (select birthdate from extraschool_child where id = ip.childid)
                             and ec.isdisabled = False
                             AND ip.prestation_date = ep.prestation_date
                             )
                             -
                             (select count(distinct ep.childid)
                              from extraschool_prestationtimes ep
                              left join extraschool_child ec on ep.childid = ec.id
                              left join extraschool_parent pp on pp.id = ep.parent_id
                              left join extraschool_activityoccurrence aao on aao.id = ep.activity_occurrence_id
                              left join extraschool_activity aa on aa.id = aao.activityid   
                              where  pp.streetcode = p.streetcode 
                                 and (
                                       (
                                         tarif_group_name is null and  
                                         (ep.activity_occurrence_id = ip.activity_occurrence_id
                                         or
                                         ip.activity_activity_id = (select activityid from extraschool_activityoccurrence where id = ep.activity_occurrence_id)
                                         )
                                       ) or
                                       ( 
                                         tarif_group_name is not null 
                                         and tarif_group_name = aa.tarif_group_name 
                                         and ep.prestation_date = ip.prestation_date)

                                     )
                                 and invoiced_prestation_id is not NULL
                                 and ep.childid > ip.childid
                                 and ec.birthdate = (select birthdate from extraschool_child where id = ip.childid)
                                 and ec.isdisabled = False
                                 AND ip.prestation_date = ep.prestation_date
                                 ) 
                             )
                     """,
               'byaddress_nb_childs' : """(select min(id)
                                    from extraschool_childposition
                                    where position = (select count(*)
                                     from extraschool_child ec
                                     left join extraschool_parent pp on pp.id = ec.parentid
                                     where  pp.streetcode = p.streetcode
                                     and ec.isdisabled = False
                                        ))
                            """,

               'byaddress_nb_childs_wp' : """(select min(id)
                                    from extraschool_childposition
                                    where position = (select count(distinct childid)
                                     from extraschool_prestationtimes ep
                                     left join extraschool_child ec on ep.childid = ec.id
                                     left join extraschool_parent pp on pp.id = ec.parentid
                                     left join extraschool_activityoccurrence aao on aao.id = ep.activity_occurrence_id
                                     left join extraschool_activity aa on aa.id = aao.activityid   
                                     where  pp.streetcode = p.streetcode
                                        and (
                                          (
                                            tarif_group_name is null and  
                                            ep.activity_occurrence_id = ip.activity_occurrence_id
                                          ) or
                                          ( 
                                            tarif_group_name is not null 
                                            and tarif_group_name = aa.tarif_group_name 
                                            and ep.prestation_date = ip.prestation_date)
                                          
                                        )
                                        and invoiced_prestation_id is not NULL
                                        and ec.isdisabled = False
                                        )) 
                            """,

               }

        return sql.get(self.env['extraschool.activitycategory'].search([])[0].childpositiondetermination)

    @api.multi
    def _new_compute_invoices(self):
        _logger.info("Start of invoicing")

        cr,uid = self.env.cr, self.env.user.id
        config = self.env['extraschool.mainsettings'].browse([1])
        obj_activitycategory = self.env['extraschool.activitycategory']
        month_name=('','Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre')
        day_name=('Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche')

        inv_obj = self.env['extraschool.invoice']
        inv_line_obj = self.env['extraschool.invoicedprestations']

        obj_biller = self.env['extraschool.biller']
        obj_accrued = self.env['extraschool.accrued']

        #create a bille to store invoice
        biller = obj_biller.create({'period_from' : self.period_from,
                                    'period_to' : self.period_to,
                                    'payment_term': self.invoice_term,
                                    'invoices_date': self.invoice_date,
                                    'activitycategoryid': [(6, False, self.activitycategory.ids)]
                                    })

        # Check if all manuel encodage are validated.
        if (not self._check_manual_encodage()):
            message = "Il y a au moins un encodage manuel non vérifié pour cette période"
            biller.send_mail_error(_(message))
            raise Warning(_(message))

        # Check if all child registration are validated.
        if (not self._check_registration()):
            message = "Il y a au moins une fiche d'inscription non validée pour cette période"
            biller.send_mail_error(_(message))
            raise Warning(_(message))

        #check if all presta are verified
        sql_check_verified = """select count(*) as verified_count
                                    from extraschool_prestationtimes ept
                                    left join extraschool_child c on ept.childid = c.id
                                    where ept.prestation_date between %s and %s
                                        and verified = False
                                        and activity_category_id IN %s
                                        and c.schoolimplantation IN %s  
                                ;"""

        self.env.cr.execute(sql_check_verified, (self.period_from,
                                                 self.period_to,
                                                 tuple(self.activitycategory.ids),
                                                 tuple(self.schoolimplantationid.ids),
                                                 )
                            )

        verified_count = self.env.cr.dictfetchall()

        if verified_count[0]['verified_count']:
            message = "At least one prestations is not verified !!!"
            biller.send_mail_error(_(message))
            raise Warning(_(message))

        #check if there are presta to invoice
        sql_check_presta_to_invoice = """select count(*) as to_invoice_count
                                    from extraschool_prestationtimes ept
                                    left join extraschool_child c on ept.childid = c.id
                                    where ept.prestation_date between %s and %s
                                        and verified = True
                                        and invoiced_prestation_id is NULL
                                        and activity_category_id IN %s
                                        and c.schoolimplantation IN %s  
                                ;"""

        self.env.cr.execute(sql_check_presta_to_invoice, (self.period_from,
                                                          self.period_to,
                                                          tuple(self.activitycategory.ids),
                                                          tuple(self.schoolimplantationid.ids),
                                                          )
                            )
        to_invoice_count = self.env.cr.dictfetchall()

        if not to_invoice_count[0]['to_invoice_count']:
            message = "There is no presta to invoice !!!"
            biller.send_mail_error(_(message))
            raise Warning(_(message))


        #search parent to be invoiced
        sql_mega_invoicing = """select c.schoolimplantation as schoolimplantation, ept.parent_id as parent_id, childid, min(activity_occurrence_id) activity_occurrence_id,
                                    sum(case when es = 'S' then prestation_time else 0 end) - sum(case when es = 'E' then prestation_time else 0 end) as duration
                                    ,ept.activity_category_id AS activity_category_id
                                from extraschool_prestationtimes ept
                                left join extraschool_child c on ept.childid = c.id
                                left join extraschool_parent p on p.id = c.parentid
                                left join extraschool_activityoccurrence ao on ao.id = ept.activity_occurrence_id
                                left join extraschool_activity a on a.id = ao.activityid
                                where ept.prestation_date between %s and %s
                                        and verified = True
                                        and ept.activity_category_id IN %s
                                        and invoiced_prestation_id is NULL
                                        and c.schoolimplantation IN %s 
                                group by ept.parent_id,c.schoolimplantation,childid, p.streetcode,case when tarif_group_name = '' or tarif_group_name is NULL then a.name else tarif_group_name  end, ept.prestation_date, ept.activity_category_id
                                order by parent_id, c.schoolimplantation, min(activity_occurrence_id);"""

        self.env.cr.execute(sql_mega_invoicing, (self.period_from,
                                                 self.period_to,
                                                 tuple(self.activitycategory.ids),
                                                 tuple(self.schoolimplantationid.ids),
                                                 )
                            )
        invoice_lines = self.env.cr.dictfetchall()

        _logger.info("End mega invoicing")

        ctx = self.env.context.copy()
        ctx.update({'defer__compute_balance' : True,
                    })

        saved_schoolimplantation_id = -1
        saved_parent_id = -1
        invoice_ids = []
        invoice_line_ids = []
        payment_obj = self.env['extraschool.payment']
        year = biller.get_from_year()

        sequence_id = self.env['extraschool.activitycategory'].get_sequence('invoice',year)

        args=[]
        invoice = False
        lines = []
        # invoice_id = [] NEW WAY
        for invoice_line in invoice_lines:
            if saved_parent_id != invoice_line['parent_id']:# or saved_schoolimplantation_id != invoice_line['schoolimplantation']:
                saved_parent_id = invoice_line['parent_id']
                saved_schoolimplantation_id = invoice_line['schoolimplantation']
                next_invoice_num = self.env['extraschool.activitycategory'].search(
                    [('id', '=', invoice_line['activity_category_id'])]).get_next_comstruct('invoice', year,
                                                                                            sequence_id, )
                #                 invoice = inv_obj.with_context(ctx).create({'name' : _('invoice_%s') % (next_invoice_num['num'],),
                #                                             'number' : next_invoice_num['num'],
                #                                             'parentid' : saved_parent_id,
                #                                             'biller_id' : biller.id,
                #                                             'activitycategoryid': self.activitycategory.id,
                #                                             'schoolimplantationid': saved_schoolimplantation_id,
                #                                             'payment_term': biller.payment_term,
                #                                             'structcom': next_invoice_num['com_struct']})
                #NEW WAY
                # id = self.env['extraschool.invoice'].create({
                #     'name': ('invoice_%s') % (next_invoice_num['num'],),
                #     'number': next_invoice_num['num'],
                #     'parentid': saved_parent_id,
                #     'biller_id': biller.id,
                #     'activitycategoryid': self.activitycategory,
                #     'schoolimplantationid': saved_schoolimplantation_id,
                #     'payment_term': biller.payment_term,
                #     'structcom': next_invoice_num['com_struct'],
                # })
                #
                # invoice_id.append(id)

                if invoice:
                    args.append(invoice)
                invoice = {'number': next_invoice_num['num'],
                           'values': (uid,
                                      uid,
                                      ('invoice_%s') % (next_invoice_num['num'],),
                                      next_invoice_num['num'],
                                      saved_parent_id,
                                      biller.id,
                                      invoice_line['activity_category_id'],
                                      saved_schoolimplantation_id,
                                      biller.payment_term,
                                      next_invoice_num['com_struct']
                                      ),
                           'lines': []}


            duration_h = int(invoice_line['duration'])
            duration_m = int(ceil(round((invoice_line['duration']-duration_h)*60)))
            duration = duration_h*60 + duration_m

            invoice['lines'].append((uid,
                                     uid,
                                     invoice_line['childid'],
                                     invoice_line['activity_occurrence_id'],
                                     duration,
                                     ))

        if len(invoice['lines']):
            args.append(invoice)

        args_str = ','.join(cr.mogrify("""(%s, current_timestamp, %s, current_timestamp,
                                            %s,%s,%s,%s,%s,
                                            %s,%s,%s)""", x["values"]) for x in args)

        invoice_ids = cr.execute("""insert into extraschool_invoice
                                    (create_uid, create_date, write_uid, write_date,
                                    name, number, parentid, biller_id, activitycategoryid,
                                    schoolimplantationid, payment_term, structcom)
                                    VALUES"""  + args_str)

        invoice_ids = cr.execute("""select id, number 
                                   from extraschool_invoice 
                                   where biller_id = %s
                                   order by number""",[biller.id])
        invoice_ids = cr.dictfetchall()

        _logger.info("End creation of Invoices")

        if len(args) - len(invoice_ids):
            message = "Error : number of invoice created differ from original"
            biller.send_mail_error(_(message))
            raise Warning(_(message))

        lines_args_str = ""
        i=0
        while i < len(args):
            if str(invoice_ids[i]['number']) == str(args[i]['number']):
                if len(lines_args_str):
                    lines_args_str += ","
                lines_args_str += ','.join(cr.mogrify("""(%s, current_timestamp, %s, current_timestamp,
                                                            """ + str(invoice_ids[i]['id']) +
                                                      """,%s,%s,%s)""", x) for x in args[i]['lines'])

            i+=1

        invoice_line_ids = cr.execute("""insert into extraschool_invoicedprestations 
                                        (create_uid, create_date, write_uid, write_date,
                                        invoiceid, childid, activity_occurrence_id, duration) 
                                        VALUES """ + lines_args_str + ";")
        invoice_ids = [i['id'] for i in invoice_ids]

        invoice_line_ids = cr.execute("""select ip.id as id 
                                       from extraschool_invoicedprestations ip
                                       left join extraschool_invoice i on i.id = ip.invoiceid 
                                       where biller_id = %s
                                       """,[biller.id])
        invoice_line_ids = [l['id'] for l in cr.dictfetchall()]

        # Mise à jour de la class.
        sql_update_class = """update extraschool_invoice i
                                set classid = (select classid 
                                from extraschool_invoicedprestations ip
                                left join extraschool_child c on c.id = ip.childid
                                where ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """) 
                                      and invoiceid = i.id and classid is not Null
                                limit 1)                             
                            """
        self.env.cr.execute(sql_update_class)

        _logger.info("End update class")

        # Mise à jour activity_activity_id.
        sql_update_activity_id = """update extraschool_invoicedprestations ip
                                    set activity_activity_id = ao.activityid
                                    from extraschool_activityoccurrence ao 
                                    where ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    and activity_activity_id is Null
                                    and activity_occurrence_id is not NULL
                                    and ao.id = ip.activity_occurrence_id                
                                    """
        self.env.cr.execute(sql_update_activity_id)

        _logger.info("End update activity")

        # Mise à jour sendmethod on invoice.
        sql_update_invoice_sendmethod = """update extraschool_invoice i
                                            set invoicesendmethod = p.invoicesendmethod
                                            from extraschool_parent p
                                            where i.invoicesendmethod is null
                                            and i.biller_id = %s
                                            and p.id = i.parentid;        
                                        """
        self.env.cr.execute(sql_update_invoice_sendmethod,[biller.id])

        _logger.info("End update send method")

        # Mise à jour lien entre invoice line et presta.
        sql_update_link_to_presta = """update extraschool_prestationtimes ept
                                    set invoiced_prestation_id = (select max(iiip.id) 
                                                                  from extraschool_invoicedprestations iiip
                                                                  left join extraschool_activity aa on aa.id = activity_activity_id  
                                                                  where childid = ept.childid and 
                                                                        (iiip.activity_occurrence_id = ept.activity_occurrence_id or
                                                                        (a.tarif_group_name is not NULL and a.tarif_group_name = aa.tarif_group_name
                                                                        and ept.prestation_date = iiip.prestation_date))
                                                                        )
                                    from extraschool_child c, extraschool_activityoccurrence ao, extraschool_activity a
                                    where c.id = ept.childid and
                                        ao.id = ept.activity_occurrence_id and
                                        a.id = ao.activityid and
                                        ept.prestation_date between %s and %s
                                        and verified = True
                                        and ept.activity_category_id IN %s
                                        and c.schoolimplantation IN %s;
                                    """
        self.env.cr.execute(sql_update_link_to_presta, (self.period_from,
                                                        self.period_to,
                                                        tuple(self.activitycategory.ids),
                                                        tuple(self.schoolimplantationid.ids),
                                                        )
                            )

        _logger.info("End update link to prestattions")

        # Mise à jour position de l'enfant.
        sql_update_prestationdate = """
                                        UPDATE extraschool_invoicedprestations ip
                                        SET prestation_date = occurrence_date,
                                            placeid = place_id
                                        from extraschool_activityoccurrence ao
                                        where ao.id = ip.activity_occurrence_id and
                                            ip.id IN %s; 
                                    """

        self.env.cr.execute(sql_update_prestationdate, (tuple(invoice_line_ids),))

        _logger.info("End update prestation date")

        # Mise à jour position de l'enfant.
        sql_update_child_position = """
                                        UPDATE extraschool_invoicedprestations ip
                                        SET child_position_id = """ + self.get_sql_position_querry() + """
                                        from extraschool_invoice i, extraschool_parent p
                                        where i.id = ip.invoiceid and
                                              p.id = i.parentid and
                                            ip.id IN %s; 
                                    """

        self.env.cr.execute(sql_update_child_position, (tuple(invoice_line_ids),))

        _logger.info("End update child postition")

        # Mise à jour description with.
        sql_update_description = """
                                        UPDATE extraschool_invoicedprestations ip
                                        SET description = a.tarif_group_name || ' - ' || to_char(ip.prestation_date,'DD-MM-YYYY') 
                                        from extraschool_activityoccurrence ao, extraschool_activity a
                                        where ao.id = ip.activity_occurrence_id and
                                        a.id = ao.activityid and
                                        a.tarif_group_name is not Null and a.tarif_group_name <> '' and
                                            ip.id IN %s; 
                                    """

        self.env.cr.execute(sql_update_description, (tuple(invoice_line_ids),))


        _logger.info("End update description")

        # Mise à jour des pricelist.
        sql_update_price_list = """UPDATE extraschool_invoicedprestations ip
                                SET price_list_version_id = 
                                    (select min(id)
                                    from extraschool_price_list_version plv
                                    left join extraschool_activity_pricelist_rel ap_rel on ap_rel.extraschool_price_list_version_id = plv.id
                                    left join extraschool_childposition_pricelist_rel cpl_rel on cpl_rel.extraschool_price_list_version_id = plv.id
                                    left join extraschool_childtype_pricelist_rel ct_rel on ct_rel.extraschool_price_list_version_id = plv.id
                                    where validity_from <= prestation_date and validity_to >= prestation_date
                                    AND ct_rel.extraschool_childtype_id = c.childtypeid
                                    AND ap_rel.extraschool_activity_id = ao.activityid
                                    AND cpl_rel.extraschool_childposition_id = ip.child_position_id
                                    )
                                
                                FROM extraschool_activityoccurrence ao, extraschool_child c
                                WHERE ip.id IN %s
                                    AND ao.id = ip.activity_occurrence_id
                                    AND ip.childid = c.id;"""


#        self.env.invalidate_all()
        self.env.cr.execute(sql_update_price_list, (tuple(invoice_line_ids),))


        _logger.info("End update price list")

        # Check if pricelist is correctly set.
        sql_check_verified = """select count(*) as verified_count
                                from extraschool_invoicedprestations ip
                                where ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    and price_list_version_id is null
                                ;"""

        self.env.cr.execute(sql_check_verified, (tuple(self.activitycategory.ids),))
        verified_count = self.env.cr.dictfetchall()
        if verified_count[0]['verified_count']:
            sql_check_missing_pl = """select c.firstname || ' ' || c.lastname as child_name, ct.name as child_type, cp.name as child_position_id, extraschool_activityoccurrence.name as name,ip.prestation_date as prestation_date
                                from extraschool_invoicedprestations ip 
                                left join extraschool_activityoccurrence on activity_occurrence_id = extraschool_activityoccurrence.id
                                left join extraschool_childposition cp on cp.id = ip.child_position_id
                                left join extraschool_child c on c.id = ip.childid
                                left join extraschool_childtype ct on ct.id = c.childtypeid
                                where ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    and price_list_version_id is null
                                ;"""

            self.env.cr.execute(sql_check_missing_pl, (tuple(self.activitycategory.ids),))
            missing_pls = self.env.cr.dictfetchall()
            message = _("At least one price list is missing !!!\n ")
            for missing_pl in missing_pls:
                message += "%s - %s - %s - %s -> %s\n" % (
                missing_pl['child_name'],
                missing_pl['child_type'],
                missing_pl['child_position_id'],
                missing_pl['name'],
                missing_pl['prestation_date']
                )
            biller.send_mail_error(_(message))
            raise Warning(_(message))

        # Mise à jour des prix et unité de tps.
        invoice_line_ids_sql = (tuple(invoice_line_ids),)

        sql_update_price = """UPDATE extraschool_invoicedprestations ip
                              SET period_duration = plv.period_duration,
                                    period_tolerance = plv.period_tolerance,
                                    unit_price = plv.price,
                                    quantity = duration / plv.period_duration + (case when duration % plv.period_duration > plv.period_tolerance then 1 else 0 end),
                                    total_price = quantity * unit_price
                              FROM extraschool_price_list_version plv
                              WHERE ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    AND plv.id = ip.price_list_version_id;"""

        try:
            self.env.cr.execute(sql_update_price)
        except:
            message = "There is a problem with the price list."
            biller.send_mail_error(_(message))
            raise Warning(_(message))

        # Mise à jour du quantity et total price.
        sql_update_total_price = """UPDATE extraschool_invoicedprestations ip
                              SET   quantity = duration / plv.period_duration + (case when duration % plv.period_duration > plv.period_tolerance then 1 else 0 end),
                                    total_price = round(quantity * unit_price, 2)
                              FROM extraschool_price_list_version plv
                              WHERE ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    AND plv.id = ip.price_list_version_id;"""

        self.env.cr.execute(sql_update_total_price)

        # Mise à jour du total sur invoice.
        sql_update_invoice_total_price = """update extraschool_invoice i
                                        set amount_total = (select sum(round(ip.total_price, 2)) 
                                    from extraschool_invoicedprestations ip
                                    where ip.invoiceid = i.id)
                                    where i.id in (""" + ','.join(map(str, invoice_ids))+ """)
                                    ;"""

        self.env.cr.execute(sql_update_invoice_total_price)

        # Mise à zero du total sur invoice negegative.
        sql_update_invoice_total_price = """update extraschool_invoice i
                                        set amount_total = 0,
                                        balance = amount_total
                                    where i.id in (""" + ','.join(map(str, invoice_ids))+ """)
                                    and amount_total <= 0
                                    ;"""

        self.env.cr.execute(sql_update_invoice_total_price)


        self.env.invalidate_all()

        invoice_ids_rs = inv_obj.browse(invoice_ids)

        # Put activity categories in invoices
        for invoice in invoice_ids_rs:
            invoice.activitycategoryid = [(6, False, self.activitycategory.ids)]

        logging.info("Computing Discount")
        self.env['extraschool.discount'].compute(biller)

        invoice_ids_rs.reconcil()

        # Create the accrued for the biller
        invoice_ids = self.env['extraschool.invoice'].search([('biller_id', '=', biller.id)])

        for activity_category in self.activitycategory.ids:
            amount = 0
            for invoice in invoice_ids:
                total = sum(invoice_line.total_price for invoice_line in invoice.invoice_line_ids.filtered(lambda r: r.activity_occurrence_id.activity_category_id.id == activity_category))
                amount += 0 if total < 0.0001 else total

            obj_accrued.create({
                'biller_id': biller.id,
                'activity_category_id': activity_category,
                'amount': amount,
            })

        _logger.info("End invoicing")
        if self.generate_pdf:
            _logger.info("Start generation of PDF")
            if self.env['ir.config_parameter'].get_param('extraschool.invoice.generate_pdf',1) == 1:
                biller.generate_pdf()
            else:
                biller.pdf_ready = True
                biller.in_creation = False
                biller.send_mail_completed()
            _logger.info("ALL PDF GENERATED")
        else:
            biller.pdf_ready = True
            biller.in_creation = False
            biller.send_mail_completed()
        view_id = self.pool.get('ir.ui.view').search(cr,uid,[('model','=','extraschool.biller'),
                                                             ('name','=','Biller.form')])

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'extraschool.biller',
            'res_id': biller.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'nodestroy': True,
            'target': 'current',
        }

    @api.multi
    def action_compute_invoices(self):
        return self._new_compute_invoices()
