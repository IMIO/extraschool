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

from openerp import models, api, fields
#import appy.pod.renderer
from datetime import datetime


class extraschool_taxcertificates_wizard(models.TransientModel):
    _name = 'extraschool.taxcertificates_wizard'

    year = fields.Char('Year', size=4)
    activitycategory = fields.Many2one('extraschool.activitycategory', 'Activity category', required=True)
    parentid = fields.Many2one('extraschool.parent', 'Parent')
    name = fields.Char('File Name', size=50, readonly=True)
    taxcertificates = fields.Binary('File', readonly=True)
    state = fields.Selection([('init', 'Init'),
                              ('compute_taxcertificates', 'Compute taxcertificates')],
                             'State', required=True, default = 'init'
                             )

    def get_taxe_certificates(self):
        cr,uid = self.env.cr, self.env.user.id

        obj_config = self.env['extraschool.mainsettings']
        config=obj_config.browse([1])
        activitycat= self.activitycategory

        if not self.parentid:
            parent_select = ""
        else:
            parent_select = "AND parentid = %s" % (self.parentid.id)

        sql_concerned_invoice = """
                                    select distinct(iii.id) as id
                                            from extraschool_payment_reconciliation ppr
                                            left join extraschool_invoice iii on iii.id = ppr.invoice_id
                                            left join extraschool_payment pp on pp.id = ppr.payment_id
                                            where ppr.date BETWEEN '%s' and '%s'
                                                AND iii.balance = 0                                            
                                """ % (self.year+'-01-01',self.year+'-12-31')

        sql_concerned_invoice += parent_select

        sql_concerned_attest = """
                                    select i.parentid,par.firstname as parent_firstname,par.lastname as parent_lastname,par.street as parent_street,par.zipcode as parent_zipcode,par.city as parent_city,ip.childid,c.firstname as child_firstname,c.lastname as child_lastname,c.birthdate as child_birthdate,si.name as implantation,sc.name as classe, sum(total_price) as amount,min(ao.occurrence_date) as period_from,max(ao.occurrence_date) as period_to,
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
                                    group by i.parentid,par.firstname,par.lastname,par.street,par.zipcode,par.city,ip.childid,c.firstname,c.lastname,c.birthdate,si.name,sc.name
                                    having sum(total_price) > 0
                                    order by si.name,sc.name,i.parentid;
                                
                                """

        if not self.parentid:
            parent_select = ""
        else:
            parent_select = "p.parent_id = %s" % (self.parentid.id)

        cr.execute(sql_concerned_attest,(sql_concerned_invoice,sql_concerned_invoice))
        childattestations = cr.dictfetchall()

        return childattestations

    def get_date(self):
        return datetime.today().strftime('%d/%m/%Y')

    @api.multi
    def action_compute_taxcertificates(self):

        report = self.env['report']._get_report_from_name('extraschool.tpl_taxe_certificate_wizard_report')
        datas = {
        'ids': self.ids,
        'model': report.model,
        }

        return {
               'type': 'ir.actions.report.xml',
               'report_name': 'extraschool.tpl_taxe_certificate_wizard_report',
               'datas': datas,
               'report_type': 'qweb-pdf',
           }
