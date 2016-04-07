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

from openerp import models, api, fields
from openerp.api import Environment
import cStringIO
import base64
import os
import lbutils
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
            cr.execute("""select distinct(parentid),schoolimplantationid,extraschool_parent.firstname,
                                extraschool_parent.lastname,extraschool_parent.street,extraschool_parent.zipcode,extraschool_parent.city 
                          from extraschool_invoice 
                          left join extraschool_parent on parentid=extraschool_parent.id  
                          where no_value<amount_total and amount_received > 0 
                              and biller_id in (select id from extraschool_biller where period_from >= %s and period_to <= %s) 
                          order by schoolimplantationid,extraschool_parent.firstname,
                                extraschool_parent.lastname""", 
                          (self.year+'-01-01',self.year+'-12-31'))
        else:
            cr.execute("""select distinct(parentid),schoolimplantationid,
                                extraschool_parent.firstname,extraschool_parent.lastname,
                                extraschool_parent.street,extraschool_parent.zipcode,extraschool_parent.city 
                          from extraschool_invoice left join extraschool_parent on parentid=extraschool_parent.id  
                          where parentid=%s and no_value<amount_total and amount_received > 0 
                              and biller_id in (select id from extraschool_biller where period_from >= %s and period_to <= %s) 
                          order by schoolimplantationid,extraschool_parent.firstname,extraschool_parent.lastname""", 
                              (self.parentid.id,self.year+'-01-01',self.year+'-12-31'))
        parents = cr.dictfetchall()
        print "parents : %s" % (parents)
        childattestation = []
        child_obj  = self.pool.get('extraschool.child')
        childattestations = []
 
        for parent in parents:
            cr.execute("""select sum(amount_received) as total_received 
                          from extraschool_invoice 
                          where parentid=%s and no_value<amount_total and amount_received > 0 
                                and biller_id in (select id from extraschool_biller where period_from >= %s 
                                and period_to <= %s)""", 
                                (parent['parentid'], self.year+'-01-01',self.year+'-12-31'))
            
            amount_received = cr.dictfetchone()['total_received']
            print "amount received:%s" % (amount_received)
            cr.execute("""select childid, sum(quantity*unit_price) as childsum 
                            from extraschool_invoicedprestations 
                            left join extraschool_activity on activityid=extraschool_activity.id 
                            where childid in (select id from extraschool_child where parentid=%s) 
                            and prestation_date >= %s and prestation_date <= %s 
                            and invoiceid is not Null and unit_price > 0 
                            group by childid""", 
                            (parent['parentid'], self.year+'-01-01',self.year+'-12-31'))
            
            childsums=cr.dictfetchall()
            print "childsums:%s" % (childsums)
            totalchildsum=0
            for childsum in childsums:
                totalchildsum = totalchildsum + childsum['childsum']
            for childsum in childsums:
                child=child_obj.read(cr, uid, [childsum['childid']],['lastname','firstname','birthdate'])[0]
                cr.execute("""select distinct(prestation_date) 
                              from extraschool_invoicedprestations left join extraschool_activity on activityid=extraschool_activity.id 
                              where childid=%s and prestation_date >= %s and prestation_date <= %s and invoiceid is not Null 
                                  and unit_price > 0 order by prestation_date""", 
                             (childsum['childid'], self.year+'-01-01',self.year+'-12-31'))
                
                prestation_dates=cr.dictfetchall()
                period_from = lbutils.strdate(prestation_dates[0]['prestation_date'])
                period_to = lbutils.strdate(prestation_dates[len(prestation_dates)-1]['prestation_date'])
                nbdays = len(prestation_dates)
                amount = '%.2f' % round((amount_received / totalchildsum) * childsum['childsum'],2)
                childattestations.append({'parent_firstname':parent['firstname'],
                                          'parent_lastname':parent['lastname'],
                                          'parent_street':parent['street'],
                                          'parent_zipcode':parent['zipcode'],
                                          'parent_city':parent['city'],
                                          'child_firstname':child['firstname'],
                                          'child_lastname':child['lastname'],
                                          'child_birthdate':lbutils.strdate(child['birthdate']),
                                          'period_from':period_from,
                                          'period_to':period_to,
                                          'nbdays':nbdays,
                                          'amount':amount})
        
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
