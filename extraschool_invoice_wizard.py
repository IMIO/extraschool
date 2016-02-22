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


class extraschool_invoice_wizard(models.TransientModel):
    _name = 'extraschool.invoice_wizard'
    _schoolimplantationids = []

    def _get_defaultfrom(self):
        #to do remove it when test is finished
        cr,uid = self.env.cr, self.env.user.id
        return '2014-01-01'
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
            todate=datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,1)-datetime.timedelta(1)
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
        self.period_from = str(termdate)

    schoolimplantationid = fields.Many2many(comodel_name='extraschool.schoolimplantation',
                               relation='extraschool_invoice_wizard_schoolimplantation_rel',
                               column1='invoice_wizard_id',
                               column2='schoolimplantation_id')
    activitycategory = fields.Many2one('extraschool.activitycategory', 'Activity category', required=True, default=1)        
    period_from = fields.Date('Period from', required=True, default=_get_defaultfrom)
    period_to = fields.Date('Period to', required=True, default=_get_defaultto)
    invoice_date = fields.Date('invoice date', required=True, default=_get_defaultto)
    invoice_term = fields.Date('invoice term', required=True, default=_get_defaultto)
    name = fields.Char('File Name', size=16, readonly=True)
    invoices = fields.Binary('File', readonly=True)
    state = fields.Selection([('init', 'Init'),
                              ('compute_invoices', 'Compute invoices')],
                             'State', required=True, default='init'
                             )

    def computediscount(self, cr, uid,childid,period,childtypeid,childactivities):
        amount=0.0
        if childactivities:
            cr.execute('select * from "extraschool_discount" where period = %s and id in (select discount_id from extraschool_discount_childtype_rel where childtype_id = %s) and id in (select discount_id from extraschool_discount_activity_rel where activity_id in '+str(childactivities.keys()).replace('[','(').replace(']',')')+')', (period,childtypeid,))                
            discounts=cr.dictfetchall()                  
            for discount in discounts:
                totactivities=0.0
                havediscount=False
                cr.execute('select activity_id from "extraschool_discount_activity_rel" where discount_id = %s', (discount['id'],))                
                discountactivities=cr.dictfetchall()
                discountactivitiesids=[]
                for discountactivity in discountactivities:
                    if str(discountactivity['activity_id']) in childactivities.keys():
                        discountactivitiesids.append(str(discountactivity['activity_id']))
                for childactivityid in discountactivitiesids:
                    if (havediscount == False) or (discount['wichactivities'] != 'OneOf'):
                        rulesok=True
                        cr.execute('select * from "extraschool_discountrule" where id in (select discountrule_id from extraschool_discount_discountrule_rel where discount_id = %s)', (discount['id'],))                
                        discountrules=cr.dictfetchall()
                        if discountrules:
                            for discountrule in discountrules:
                                cr.execute('select id from extraschool_child where id= %s and '+discountrule['field']+' '+discountrule['operator']+' '+discountrule['value'],(childid,))
                                rulecount = cr.dictfetchall()
                                if not rulecount:
                                    rulesok=False
                        else:
                            havediscount=True
                        if rulesok:
                            havediscount=True
                            if discount['wichactivities'] != 'Sum':
                                if discount['discounttype'] == 'sub':
                                    amount=amount+float(discount['discount'])
                                elif discount['discounttype'] == 'prc': 
                                    amount=amount+((childactivities[childactivityid] * float(discount['discount'].split('%')[0])) / 100)
                                elif discount['discounttype'] == 'max':
                                    if childactivities[childactivityid] > float(discount['discount']):
                                        amount=amount+(childactivities[childactivityid]-float(discount['discount']))
                            else:
                                totactivities=totactivities+childactivities[childactivityid]
                if discount['wichactivities'] == 'Sum':
                    if discount['discounttype'] == 'sub':
                        amount=amount+float(discount['discount'])
                    elif discount['discounttype'] == 'prc':
                        amount=amount+((totactivities * discount['discount'].split('%')[0]) / 100)
                    elif discount['discounttype'] == 'max':
                        if totactivities > float(discount['discount']):
                                amount=amount+(totactivities-float(discount['discount']))
        return amount
    
    def _compute_invoices(self):
        cr,uid = self.env.cr, self.env.user.id
        
    def get_sql_position_querry(self):
        sql = {'byparent' : """(select min(id) 
                                from extraschool_childposition
                                where position = (select count(*) + 1
                                 from extraschool_child ec 
                                 where  parent_id = ec.parentid
                                    and id <> ept.childid
                                    and ec.birthdate < (select birthdate from extraschool_child where id = ept.childid)
                                    )) as child_position_id
                            """,
               'byparentwp' : """(select min(id) 
                                from extraschool_childposition
                                where position = (select count(distinct childid) + 1
                                 from extraschool_prestationtimes ep
                                 left join extraschool_child ec on ep.childid = ec.id
                                 where  parent_id = ept.parent_id 
                                    and activity_occurrence_id = ept.activity_occurrence_id
                                    and childid <> ept.childid
                                    and ec.birthdate < (select birthdate from extraschool_child where id = ept.childid)
                                    )) as child_position_id
                            """,
                'byparent_nb_childs' : """(select min(id) 
                                from extraschool_childposition
                                where position = (select count(*)
                                 from extraschool_child ec 
                                 where  parent_id = ec.parentid
                                    )) as child_position_id
                            """,

                'byparent_nb_childs_wp' : """(select min(id) 
                                from extraschool_childposition
                                where position = (select count(distinct childid)
                                 from extraschool_prestationtimes ep
                                 left join extraschool_child ec on ep.childid = ec.id
                                 where  parent_id = ept.parent_id 
                                    and activity_occurrence_id = ept.activity_occurrence_id
                                    )) as child_position_id
                            """,

               'byaddress' : """(select min(id)
                                    from extraschool_childposition
                                    where position = (select count(*) + 1
                                     from extraschool_child ec
                                     left join extraschool_parent pp on pp.id = ec.parentid
                                     where  pp.streetcode = p.streetcode
                                        and ec.id <> ept.childid
                                        and ec.birthdate < (select birthdate from extraschool_child where id = ept.childid)
                                        )) as child_position_id
                            """,
               'byaddresswp' : """(select min(id)
                                    from extraschool_childposition
                                    where position = (select count(distinct childid) + 1
                                     from extraschool_prestationtimes ep
                                     left join extraschool_child ec on ep.childid = ec.id
                                     left join extraschool_parent pp on pp.id = ec.parentid
                                     where  pp.streetcode = p.streetcode
                                        and activity_occurrence_id = ept.activity_occurrence_id
                                        and childid <> ept.childid
                                        and ec.birthdate < (select birthdate from extraschool_child where id = ept.childid)
                                        )) as child_position_id
                            """,
               'byaddress_nb_childs' : """(select min(id)
                                    from extraschool_childposition
                                    where position = (select count(*)
                                     from extraschool_child ec
                                     left join extraschool_parent pp on pp.id = ec.parentid
                                     where  pp.streetcode = p.streetcode
                                        )) as child_position_id
                            """,
                                                        
               'byaddress_nb_childs_wp' : """(select min(id)
                                    from extraschool_childposition
                                    where position = (select count(distinct childid)
                                     from extraschool_prestationtimes ep
                                     left join extraschool_child ec on ep.childid = ec.id
                                     left join extraschool_parent pp on pp.id = ec.parentid
                                     where  pp.streetcode = p.streetcode
                                        and activity_occurrence_id = ept.activity_occurrence_id
                                        )) as child_position_id
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
                                    })

        
        
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

        
        #search parent to be invoiced
        sql_mega_invoicing = """select c.schoolimplantation as schoolimplantation, parent_id, childid, activity_occurrence_id,
                                    sum(case when es = 'S' then prestation_time else 0 end) - sum(case when es = 'E' then prestation_time else 0 end) as duration,
                                    """ + self.get_sql_position_querry() + """
                                from extraschool_prestationtimes ept
                                left join extraschool_child c on ept.childid = c.id
                                left join extraschool_parent p on p.id = c.parentid
                                where ept.prestation_date between %s and %s
                                        and verified = True
                                        and activity_category_id = %s
                                        and c.schoolimplantation in (""" + ','.join(map(str, self.schoolimplantationid.ids))+ """)  
                                group by c.schoolimplantation,parent_id,childid, activity_occurrence_id,p.streetcode
                                order by c.schoolimplantation,parent_id, activity_occurrence_id;"""

        self.env.cr.execute(sql_mega_invoicing, (self.period_from, self.period_to, self.activitycategory.id,))
        invoice_lines = self.env.cr.dictfetchall()

        saved_schoolimplantation_id = -1        
        saved_parent_id = -1
        invoice_ids = []
        invoice_line_ids = []
        payment_obj = self.env['extraschool.payment']
        next_invoice_num = self.activitycategory.invoicelastcomstruct
        for invoice_line in invoice_lines:
            if saved_parent_id != invoice_line['parent_id'] or saved_schoolimplantation_id != invoice_line['schoolimplantation']:
                saved_parent_id = invoice_line['parent_id']
                saved_schoolimplantation_id = invoice_line['schoolimplantation']
                next_invoice_num += 1
                com_struct_prefix_str = self.activitycategory.invoicecomstructprefix
                com_struct_id_str = str(next_invoice_num).zfill(7)
                com_struct_check_str = str(long(com_struct_prefix_str+com_struct_id_str) % 97).zfill(2)
                com_struct_check_str = com_struct_check_str if com_struct_check_str != '00' else '97'
                             
                invoice = inv_obj.create({'name' : _('invoice_%s') % (str(next_invoice_num).zfill(7),),
                                            'number' : next_invoice_num,
                                            'parentid' : saved_parent_id,
                                            'biller_id' : biller.id,
                                            'activitycategoryid': self.activitycategory.id,
                                            'schoolimplantationid': saved_schoolimplantation_id,
                                            'structcom': payment_obj.format_comstruct('%s%s%s' % (com_struct_prefix_str,com_struct_id_str,com_struct_check_str))})
                invoice_ids.append(invoice.id)

            duration_h = int(invoice_line['duration'])
            duration_m = int(ceil(round((invoice_line['duration']-duration_h)*60)))
            duration = duration_h*60 + duration_m
            invoice_line_ids.append(inv_line_obj.create({'invoiceid' : invoice.id,
                                 'childid': invoice_line['childid'],
                                 'activity_occurrence_id': invoice_line['activity_occurrence_id'],
                                 'duration': duration,
                                 'child_position_id': invoice_line['child_position_id'],
                                 }).id)
        
        self.activitycategory.invoicelastcomstruct = next_invoice_num + 1
        #Mise à jour lien entre invoice line et presta
        sql_update_link_to_presta = """update extraschool_prestationtimes ept
                                    set invoiced_prestation_id = (select id from extraschool_invoicedprestations where childid = ept.childid and activity_occurrence_id = ept.activity_occurrence_id)
                                    from extraschool_child c 
                                    where c.id = ept.childid and
                                        ept.prestation_date between %s and %s
                                        and verified = True
                                        and activity_category_id = %s
                                        and c.schoolimplantation in (""" + ','.join(map(str, self.schoolimplantationid.ids))+ """);
                                    """     
        self.env.cr.execute(sql_update_link_to_presta, (self.period_from, self.period_to, self.activitycategory.id,))

        
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

            print "At least one price list is missing !!!\n "
            sql_check_missing_pl = """select extraschool_activityoccurrence.name
                                from extraschool_invoicedprestations ip 
                                left join extraschool_activityoccurrence on activity_occurrence_id = extraschool_activityoccurrence.id
                                where ip.id in (""" + ','.join(map(str, invoice_line_ids))+ """)
                                    and price_list_version_id is null
                                ;"""

            self.env.cr.execute(sql_check_missing_pl, (self.activitycategory.id,))
            missing_pls = self.env.cr.dictfetchall()
            message = _("At least one price list is missing !!!\n ")
            for missing_pl in missing_pls:
                message += "%s\n" % (missing_pl['name'])
            print "+++++++++++++++++======================="
            print message
            raise Warning(message)
        #Mise à jour des prix et unité de tps
        invoice_line_ids_sql = (tuple(invoice_line_ids),)
        print str(invoice_line_ids_sql)
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
        
        self.env.cr.execute(sql_update_price)
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
        
        inv_obj.browse(invoice_ids).reconcil()
        
        
#         #payment reconcil
#         payment = self.env['extraschool.payment']
#         payment_reconcil = self.env['extraschool.payment_reconciliation']
#         print "%s invoices to reconcil" % (len(invoice_ids))
#         #get invoice amount
# 
#         #Mise à jour balance
#         sql_update_invoice_balance = """update extraschool_invoice i                                        
#                                         set balance = amount_total
#                                     where i.id in (""" + ','.join(map(str, invoice_ids))+ """)                                    
#                                     ;"""
#         
#         self.env.cr.execute(sql_update_invoice_balance)
#                 
#         sql_select_invoice_amount_total = """    select i.id as id, i.parentid as parentid, amount_total, ac.payment_invitation_com_struct_prefix as payment_invitation_com_struct_prefix
#                                                 from extraschool_invoice i
#                                                 left join extraschool_biller b on i.biller_id = b.id
#                                                 left join extraschool_activitycategory ac on b.activitycategoryid = ac.id
#                                                 where i.id in (""" + ','.join(map(str, invoice_ids))+ """)
#                                             ;"""
#         
# 
#         
#         self.env.cr.execute(sql_select_invoice_amount_total)
#         invoices = self.env.cr.dictfetchall()
#         for invoice in invoices:
#             #search for open payment
#             payments = payment.search([('parent_id','=',invoice['parentid']),
#                             ('structcom_prefix','=',invoice['payment_invitation_com_struct_prefix']),
#                             ('solde','>',0),
#                             ]).sorted(key=lambda r: r.paymentdate)
#             print "%s payments found for invoice %s" % (len(payments),invoice['id'])
#             print payments
#             zz = 0
#             print "invoice balance = %s" % (invoice['amount_total'])
#             solde = invoice['amount_total']
#             while zz < len(payments) and solde > 0:
#                 amount = solde if payments[zz].solde >= solde else payments[zz].solde
#                 print "Add payment reconcil - amount : %s" % (amount)
#                 payment_reconcil.create({'payment_id': payments[zz].id,
#                                          'invoice_id': invoice['id'],
#                                          'amount': amount,
#                                          })
#                 solde -= amount
#                 zz += 1
                                    
        
    @api.multi    
    def action_compute_invoices(self):   
        self._new_compute_invoices()
            