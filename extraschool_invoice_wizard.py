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
from datetime import date
from dateutil.relativedelta import relativedelta
import datetime
import calendar
import cStringIO
import base64
import os
import math
import xlrd
import lbutils
import re
from math import *
from pyPdf import PdfFileWriter, PdfFileReader
from openerp.exceptions import except_orm, Warning, RedirectWarning
import threading


class extraschool_invoice_wizard(models.TransientModel):
    _name = 'extraschool.invoice_wizard'
    _schoolimplantationids = []

    def _get_defaultfrom(self):
        #to do remove it when test is finished
        cr,uid = self.env.cr, self.env.user.id
        #return '2014-01-01'
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
        #todate=datetime.date(2013,11,1)
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

    def _get_activity_category_id(self):
        return self.env['extraschool.activitycategory'].search([]).filtered('id').id

    schoolimplantationid = fields.Many2many(comodel_name='extraschool.schoolimplantation',
                               relation='extraschool_invoice_wizard_schoolimplantation_rel',
                               column1='invoice_wizard_id',
                               column2='schoolimplantation_id', default=_get_all_schoolimplantation, readonly=True)
    activitycategory = fields.Many2one('extraschool.activitycategory', 'Activity category', required=True, default=_get_activity_category_id)
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
                                        ) 
                                    )
                            """,
                'byparent_nb_childs' : """(select min(id) 
                                from extraschool_childposition
                                where position = (select count(*)
                                 from extraschool_child ec 
                                 where  i.parentid = ec.parentid
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
                            """,

               'byaddress' : """(select min(id)
                                    from extraschool_childposition
                                    where position = (select count(*) + 1
                                     from extraschool_child ec
                                     left join extraschool_parent pp on pp.id = ec.parentid
                                     where  pp.streetcode = p.streetcode
                                        and ec.id <> ip.childid
                                        and ec.birthdate <= (select birthdate from extraschool_child where id = ip.childid)
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
                                        ) 
                                    )
                            """,
               'byaddress_nb_childs' : """(select min(id)
                                    from extraschool_childposition
                                    where position = (select count(*)
                                     from extraschool_child ec
                                     left join extraschool_parent pp on pp.id = ec.parentid
                                     where  pp.streetcode = p.streetcode
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
                                        )) 
                            """,

               }    
        return sql.get(self.activitycategory.childpositiondetermination)
    
    def _new_compute_invoices(self):
        cr,uid = self.env.cr, self.env.user.id
        print "_new_compute_invoices"
        config = self.env['extraschool.mainsettings'].browse([1])
        obj_activitycategory = self.env['extraschool.activitycategory']
        month_name=('','Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre')
        day_name=('Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche')
         
        inv_obj = self.env['extraschool.invoice']
        inv_line_obj = self.env['extraschool.invoicedprestations']
        
        obj_biller = self.env['extraschool.biller']
        
        #create a bille to store invoice
        biller = obj_biller.create({'period_from' : self.period_from,
                                    'period_to' : self.period_to,
                                    'payment_term': self.invoice_term,
                                    'invoices_date': self.invoice_date,
                                    'activitycategoryid': self.activitycategory.id,
                                    })

        
        #check if all manuel encodage are validated
        manuel_encodage_ids = self.env['extraschool.prestation_times_encodage_manuel'].search([('state', '!=', 'validated'),
                                                                                               ('date_of_the_day', '>=', self.period_from),
                                                                                               ('date_of_the_day', '<=', self.period_to),])
        if len(manuel_encodage_ids):
            raise Warning(_("At least one manuel encodage is not validated for this period!!!"))    

        #check if all child registration are validated
        child_reg_ids = self.env['extraschool.child_registration'].search([('state', '!=', 'validated'),
                                                                            '|',
                                                                            '&',('date_from', '>=', self.period_from),
                                                                                ('date_from', '<=', self.period_to),
                                                                            '&',('date_to', '>=', self.period_from),
                                                                                ('date_to', '<=', self.period_to),
                                                                                ])

        if len(child_reg_ids):
            print "child_reg_ids : %s" % (child_reg_ids)
            raise Warning(_("At least one child registration is not validated for this period!!!"))    

        
        #check if all presta are verified
        print "----------------"
        print str(self.schoolimplantationid.ids)
        
        sql_check_verified = """select count(*) as verified_count
                                    from extraschool_prestationtimes ept
                                    left join extraschool_child c on ept.childid = c.id
                                    where ept.prestation_date between %s and %s
                                        and verified = False
                                        and activity_category_id = %s
                                        and c.schoolimplantation in (""" + ','.join(map(str, self.schoolimplantationid.ids))+ """)  
                                ;"""

        self.env.cr.execute(sql_check_verified, (self.period_from, self.period_to, self.activitycategory.id,))
        verified_count = self.env.cr.dictfetchall()
        print "verified_count:" + str(verified_count[0]['verified_count'])
        if verified_count[0]['verified_count']:
            raise Warning(_("At least one prestations is not verified !!!"))

        #check if there are presta to invoice
        sql_check_presta_to_invoice = """select count(*) as to_invoice_count
                                    from extraschool_prestationtimes ept
                                    left join extraschool_child c on ept.childid = c.id
                                    where ept.prestation_date between %s and %s
                                        and verified = True
                                        and invoiced_prestation_id is NULL
                                        and activity_category_id = %s
                                        and c.schoolimplantation in (""" + ','.join(map(str, self.schoolimplantationid.ids))+ """)  
                                ;"""

        self.env.cr.execute(sql_check_presta_to_invoice, (self.period_from, self.period_to, self.activitycategory.id,))
        to_invoice_count = self.env.cr.dictfetchall()
        print "to_invoice_count:" + str(to_invoice_count[0]['to_invoice_count'])
        if not to_invoice_count[0]['to_invoice_count']:
            raise Warning(_("There is no presta to invoice !!!"))
                
        #search parent to be invoiced
        sql_mega_invoicing = """select c.schoolimplantation as schoolimplantation, ept.parent_id as parent_id, childid, min(activity_occurrence_id) activity_occurrence_id,
                                    sum(case when es = 'S' then prestation_time else 0 end) - sum(case when es = 'E' then prestation_time else 0 end) as duration

                                from extraschool_prestationtimes ept
                                left join extraschool_child c on ept.childid = c.id
                                left join extraschool_parent p on p.id = c.parentid
                                left join extraschool_activityoccurrence ao on ao.id = ept.activity_occurrence_id
                                left join extraschool_activity a on a.id = ao.activityid
                                where ept.prestation_date between %s and %s
                                        and verified = True
                                        and ept.activity_category_id = %s
                                        and invoiced_prestation_id is NULL
                                        and c.schoolimplantation in (""" + ','.join(map(str, self.schoolimplantationid.ids))+ """)  
                                group by ept.parent_id,c.schoolimplantation,childid, p.streetcode,case when tarif_group_name = '' or tarif_group_name is NULL then a.name else tarif_group_name  end, ept.prestation_date
                                order by parent_id, c.schoolimplantation, min(activity_occurrence_id);"""

#         print "---------------"
#         print (sql_mega_invoicing) % (self.period_from, self.period_to, self.activitycategory.id)
#         print "---------------"
        
        self.env.cr.execute(sql_mega_invoicing, (self.period_from, self.period_to, self.activitycategory.id,))
        invoice_lines = self.env.cr.dictfetchall()
        
        ctx = self.env.context.copy()
        ctx.update({'defer__compute_balance' : True,
                    })
        
        saved_schoolimplantation_id = -1        
        saved_parent_id = -1
        invoice_ids = []
        invoice_line_ids = []
        payment_obj = self.env['extraschool.payment']
        year = biller.get_from_year()
        sequence_id = self.activitycategory.get_sequence('invoice',year)
        print "Start - Create invoice header"
        args=[]
        invoice = False
        lines = []
        for invoice_line in invoice_lines:
            if saved_parent_id != invoice_line['parent_id']:# or saved_schoolimplantation_id != invoice_line['schoolimplantation']:
                saved_parent_id = invoice_line['parent_id']
                saved_schoolimplantation_id = invoice_line['schoolimplantation']                
                next_invoice_num = self.activitycategory.get_next_comstruct('invoice',year,sequence_id)
#                 invoice = inv_obj.with_context(ctx).create({'name' : _('invoice_%s') % (next_invoice_num['num'],),
#                                             'number' : next_invoice_num['num'],
#                                             'parentid' : saved_parent_id,
#                                             'biller_id' : biller.id,
#                                             'activitycategoryid': self.activitycategory.id,
#                                             'schoolimplantationid': saved_schoolimplantation_id,
#                                             'payment_term': biller.payment_term,
#                                             'structcom': next_invoice_num['com_struct']})
                if invoice:
                    args.append(invoice)
                invoice = {'number': next_invoice_num['num'],
                           'values': (uid,
                                      uid,
                                      ('invoice_%s') % (next_invoice_num['num'],),
                                      next_invoice_num['num'],
                                      saved_parent_id,
                                      biller.id,
                                      self.activitycategory.id,
                                      saved_schoolimplantation_id,
                                      biller.payment_term,
                                      next_invoice_num['com_struct']
                                     ),
                           'lines': []}
                
                
            duration_h = int(invoice_line['duration'])
            duration_m = int(ceil(round((invoice_line['duration']-duration_h)*60)))
            duration = duration_h*60 + duration_m
#             invoice_line_ids.append(inv_line_obj.create({'invoiceid' : invoice.id,
#                                  'childid': invoice_line['childid'],
#                                  'activity_occurrence_id': invoice_line['activity_occurrence_id'],
#                                  'duration': duration,
#                                  #'child_position_id': invoice_line['child_position_id'],
#                                  }).id)
            invoice['lines'].append((uid,
                                     uid,
                                     invoice_line['childid'],
                                     invoice_line['activity_occurrence_id'],
                                     duration,
                                     ))
        
        if len(invoice['lines']):
            args.append(invoice)
            
        print "Stop - Create invoice header"
        print "prepare header sql"
        args_str = ','.join(cr.mogrify("""(%s, current_timestamp, %s, current_timestamp,
                                            %s,%s,%s,%s,%s,
                                            %s,%s,%s)""", x["values"]) for x in args)
        
        print "exec sql create headers"
        #print insert_data               
        invoice_ids = cr.execute("""insert into extraschool_invoice 
                                    (create_uid, create_date, write_uid, write_date,
                                    name, number, parentid, biller_id, activitycategoryid,  
                                    schoolimplantationid, payment_term, structcom) 
                                    VALUES"""  + args_str)
        print "get created invoice ids"
        invoice_ids = cr.execute("""select id, number 
                                   from extraschool_invoice 
                                   where biller_id = %s
                                   order by number""",[biller.id])
        invoice_ids = cr.dictfetchall()
        print "merge header and lines"
        if len(args) - len(invoice_ids):
            raise Warning(_("Error : number of invoice created differ from original"))
        
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
            
        print "exec sql create lines"
        #print insert_data               
        invoice_line_ids = cr.execute("""insert into extraschool_invoicedprestations 
                                        (create_uid, create_date, write_uid, write_date,
                                        invoiceid, childid, activity_occurrence_id, duration) 
                                        VALUES """ + lines_args_str + ";")
        invoice_ids = [i['id'] for i in invoice_ids]

        print "get invoice_line_ids"
        invoice_line_ids = cr.execute("""select ip.id as id 
                                       from extraschool_invoicedprestations ip
                                       left join extraschool_invoice i on i.id = ip.invoiceid 
                                       where biller_id = %s
                                       """,[biller.id])
        invoice_line_ids = [l['id'] for l in cr.dictfetchall()]
        
        #mise à jour de la class 
        print "mise à jour classid"
        sql_update_class = """update extraschool_invoice i
                                set classid = (select classid 
                                from extraschool_invoicedprestations ip
                                left join extraschool_child c on c.id = ip.childid
                                where ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """) 
                                      and invoiceid = i.id and classid is not Null
                                limit 1)                             
                            """
        self.env.cr.execute(sql_update_class)
                            
        #mise à jour activity_activity_id 
        print "mise à jour activity_activity_id"
        sql_update_activity_id = """update extraschool_invoicedprestations ip
                                    set activity_activity_id = ao.activityid
                                    from extraschool_activityoccurrence ao 
                                    where ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    and activity_activity_id is Null
                                    and activity_occurrence_id is not NULL
                                    and ao.id = ip.activity_occurrence_id                
                                    """    
        self.env.cr.execute(sql_update_activity_id)  
        
        print "Mise à jour sendmethod on invoice"
        sql_update_invoice_sendmethod = """update extraschool_invoice i
                                            set invoicesendmethod = p.invoicesendmethod
                                            from extraschool_parent p
                                            where i.invoicesendmethod is null
                                            and i.biller_id = %s
                                            and p.id = i.parentid;        
                                        """
        self.env.cr.execute(sql_update_invoice_sendmethod,[biller.id])
                                              
        print "#Mise à jour lien entre invoice line et presta"                 
        #Mise à jour lien entre invoice line et presta
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
                                        and ept.activity_category_id = %s
                                        and c.schoolimplantation in (""" + ','.join(map(str, self.schoolimplantationid.ids))+ """);
                                    """     
        self.env.cr.execute(sql_update_link_to_presta, (self.period_from, self.period_to, self.activitycategory.id,))

        print "#Mise a jour prestationdate et placeid"
        #Mise à jour position de l'enfant
        sql_update_prestationdate = """
                                        UPDATE extraschool_invoicedprestations ip
                                        SET prestation_date = occurrence_date,
                                            placeid = place_id
                                        from extraschool_activityoccurrence ao
                                        where ao.id = ip.activity_occurrence_id and
                                            ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """); 
                                    """

        self.env.cr.execute(sql_update_prestationdate, ())  

        print "#Mise a jour position de l enfant"
        #Mise à jour position de l'enfant
        sql_update_child_position = """
                                        UPDATE extraschool_invoicedprestations ip
                                        SET child_position_id = """ + self.get_sql_position_querry() + """
                                        from extraschool_invoice i, extraschool_parent p
                                        where i.id = ip.invoiceid and
                                              p.id = i.parentid and
                                            ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """); 
                                    """
#        print sql_update_child_position
        self.env.cr.execute(sql_update_child_position, ())  

        print "#Mise a jour description with"
        #Mise à jour description with 
        sql_update_description = """
                                        UPDATE extraschool_invoicedprestations ip
                                        SET description = a.tarif_group_name || ' - ' || to_char(ip.prestation_date,'DD-MM-YYYY') 
                                        from extraschool_activityoccurrence ao, extraschool_activity a
                                        where ao.id = ip.activity_occurrence_id and
                                        a.id = ao.activityid and
                                        a.tarif_group_name is not Null and a.tarif_group_name <> '' and
                                            ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """); 
                                    """
#        print sql_update_description
        self.env.cr.execute(sql_update_description, ())  

        print "#Mise a jour des pricelist"       
        #Mise à jour des pricelist
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
                                WHERE ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    AND ao.id = ip.activity_occurrence_id
                                    AND ip.childid = c.id;"""
        
#        self.env.invalidate_all()       
        self.env.cr.execute(sql_update_price_list)

        print "#check if pricelist is correctly set"
        #check if pricelist is correctly set
        sql_check_verified = """select count(*) as verified_count
                                from extraschool_invoicedprestations ip
                                where ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    and price_list_version_id is null
                                ;"""

        self.env.cr.execute(sql_check_verified, (self.activitycategory.id,))
        verified_count = self.env.cr.dictfetchall()
        if verified_count[0]['verified_count']:
            print "nbr lines with pricelist not set %s sur un total de %s" % (verified_count, len(invoice_line_ids))

            print "At least one price list is missing !!!\n "
            sql_check_missing_pl = """select c.firstname || ' ' || c.lastname as child_name, ct.name as child_type, cp.name as child_position_id, extraschool_activityoccurrence.name as name,ip.prestation_date as prestation_date
                                from extraschool_invoicedprestations ip 
                                left join extraschool_activityoccurrence on activity_occurrence_id = extraschool_activityoccurrence.id
                                left join extraschool_childposition cp on cp.id = ip.child_position_id
                                left join extraschool_child c on c.id = ip.childid
                                left join extraschool_childtype ct on ct.id = c.childtypeid
                                where ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    and price_list_version_id is null
                                ;"""

            self.env.cr.execute(sql_check_missing_pl, (self.activitycategory.id,))
            missing_pls = self.env.cr.dictfetchall()
            message = _("At least one price list is missing !!!\n ")
            for missing_pl in missing_pls:
                message += "%s - %s - %s - %s -> %s\n" % (missing_pl['child_name'], missing_pl['child_type'], missing_pl['child_position_id'], missing_pl['name'], missing_pl['prestation_date'])

            raise Warning(message)
        #Mise à jour des prix et unité de tps
        invoice_line_ids_sql = (tuple(invoice_line_ids),)        
        print "#Mise à jour des prix et unité de tps"
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
            raise Warning(_("There is a problem with the price list."))
        print "#Mise à jour du quantity et total price"
        #Mise à jour du quantity et total price
        sql_update_total_price = """UPDATE extraschool_invoicedprestations ip
                              SET   quantity = duration / plv.period_duration + (case when duration % plv.period_duration > plv.period_tolerance then 1 else 0 end),
                                    total_price = quantity * unit_price
                              FROM extraschool_price_list_version plv
                              WHERE ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    AND plv.id = ip.price_list_version_id;"""
        
        self.env.cr.execute(sql_update_total_price)
        
        print "#Mise à jour du total sur invoice"
        #Mise à jour du total sur invoice
        sql_update_invoice_total_price = """update extraschool_invoice i
                                        set amount_total = (select sum(ip.total_price) 
                                    from extraschool_invoicedprestations ip
                                    where ip.invoiceid = i.id)
                                    where i.id in (""" + ','.join(map(str, invoice_ids))+ """)
                                    ;"""
        
        self.env.cr.execute(sql_update_invoice_total_price)

        print "#Mise à zero du total sur invoice negegative"
        #Mise à zero du total sur invoice negegative
        sql_update_invoice_total_price = """update extraschool_invoice i
                                        set amount_total = 0,
                                        balance = amount_total
                                    where i.id in (""" + ','.join(map(str, invoice_ids))+ """)
                                    and amount_total <= 0
                                    ;"""
        
        self.env.cr.execute(sql_update_invoice_total_price)

#         #Mise à jour de la balance
#         sql_update_invoice_total_price = """update extraschool_invoice i
#                                         set balance = amount_total
#                                     where i.id in (""" + ','.join(map(str, invoice_ids))+ """)
#                                     ;"""
        
        self.env.cr.execute(sql_update_invoice_total_price)


        self.env.invalidate_all()
        
        invoice_ids_rs = inv_obj.browse(invoice_ids)
        print "Discount ..............."
        self.env['extraschool.discount'].compute(biller)
        print "Discount ..............."
        
        invoice_ids_rs.reconcil()
        
        if self.env['ir.config_parameter'].get_param('extraschool.invoice.generate_pdf',1) == 1:
            biller.generate_pdf()
        else:
            biller.pdf_ready = True
            
        view_id = self.pool.get('ir.ui.view').search(cr,uid,[('model','=','extraschool.biller'),
                                                             ('name','=','Biller.form')])
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.biller',
#                'name': _("Prestations_of_the_day.tree"),
                'res_id': biller.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'nodestroy': True,     
                'target': 'current',                   
#                'context': {'search_default_not_verified':1}
            }  
                                    
        
    @api.multi    
    def action_compute_invoices(self):   
        return self._new_compute_invoices()
            
            