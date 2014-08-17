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

from openerp.osv import osv, fields
import cStringIO
import base64
import appy.pod.renderer
import os
import lbutils

class extraschool_taxcertificates_wizard(osv.osv_memory):
    _name = 'extraschool.taxcertificates_wizard'

    _columns = {
        'year' : fields.char('Year', size=4),
        'activitycategory' : fields.many2one('extraschool.activitycategory', 'Activity category', required=True),
        'parentid' : fields.many2one('extraschool.parent', 'Parent'),
        'name': fields.char('File Name', 50, readonly=True),
        'taxcertificates': fields.binary('File', readonly=True),
        'state' : fields.selection(
            [('init', 'Init'),('compute_taxcertificates', 'Compute taxcertificates')],
            'State', required=True
        ),
    }

    _defaults = {
        'state' : lambda *a: 'init'
    }

    def action_compute_taxcertificates(self, cr, uid, ids, context=None):
        form = self.read(cr,uid,ids,)[-1]
        obj_config = self.pool.get('extraschool.mainsettings')
        obj_activitycategory = self.pool.get('extraschool.activitycategory')
        config=obj_config.read(cr, uid, [1],['lastqrcodenbr','qrencode','tempfolder','templatesfolder'])[0]      
        activitycat= obj_activitycategory.read(cr, uid, [form['activitycategory'][0]],['taxcertificatetemplate'])[0]
        if not form['parentid']:      
            cr.execute('select distinct(parentid),schoolimplantationid,extraschool_parent.name,extraschool_parent.firstname,extraschool_parent.lastname,extraschool_parent.street,extraschool_parent.zipcode,extraschool_parent.city from extraschool_invoice left join extraschool_parent on parentid=extraschool_parent.id  where no_value<amount_total and amount_received > 0 and biller_id in (select id from extraschool_biller where period_from >= %s and period_to <= %s) order by schoolimplantationid,extraschool_parent.name', (form['year']+'-01-01',form['year']+'-12-31'))
        else:
            cr.execute('select distinct(parentid),schoolimplantationid,extraschool_parent.name,extraschool_parent.firstname,extraschool_parent.lastname,extraschool_parent.street,extraschool_parent.zipcode,extraschool_parent.city from extraschool_invoice left join extraschool_parent on parentid=extraschool_parent.id  where parentid=%s and no_value<amount_total and amount_received > 0 and biller_id in (select id from extraschool_biller where period_from >= %s and period_to <= %s) order by schoolimplantationid,extraschool_parent.name', (form['parentid'][0],form['year']+'-01-01',form['year']+'-12-31'))
        parents = cr.dictfetchall()
        childattestation = []
        child_obj  = self.pool.get('extraschool.child')
        childattestations = []
        for parent in parents:
            cr.execute('select sum(amount_received) as total_received from extraschool_invoice where parentid=%s and no_value<amount_total and amount_received > 0 and biller_id in (select id from extraschool_biller where period_from >= %s and period_to <= %s)', (parent['parentid'], form['year']+'-01-01',form['year']+'-12-31'))
            amount_received = cr.dictfetchone()['total_received']
            cr.execute('select childid, sum(quantity*price) as childsum from extraschool_invoicedprestations left join extraschool_activity on activityid=extraschool_activity.id where childid in (select id from extraschool_child where parentid=%s) and prestation_date >= %s and prestation_date <= %s and invoiceid is not Null and price > 0 group by childid', (parent['parentid'], form['year']+'-01-01',form['year']+'-12-31'))
            childsums=cr.dictfetchall()
            totalchildsum=0
            for childsum in childsums:
                totalchildsum = totalchildsum + childsum['childsum']
            for childsum in childsums:
                child=child_obj.read(cr, uid, [childsum['childid']],['lastname','firstname','birthdate'])[0]
                cr.execute('select distinct(prestation_date) from extraschool_invoicedprestations left join extraschool_activity on activityid=extraschool_activity.id where childid=%s and prestation_date >= %s and prestation_date <= %s and invoiceid is not Null and price > 0 order by prestation_date', (childsum['childid'], form['year']+'-01-01',form['year']+'-12-31'))
                prestation_dates=cr.dictfetchall()
                period_from = lbutils.strdate(prestation_dates[0]['prestation_date'])
                period_to = lbutils.strdate(prestation_dates[len(prestation_dates)-1]['prestation_date'])
                nbdays = len(prestation_dates)
                amount = '%.2f' % round((amount_received / totalchildsum) * childsum['childsum'],2)
                childattestations.append({'parent_firstname':parent['firstname'],'parent_lastname':parent['lastname'],'parent_street':parent['street'],'parent_zipcode':parent['zipcode'],'parent_city':parent['city'],'child_firstname':child['firstname'],'child_lastname':child['lastname'],'child_birthdate':lbutils.strdate(child['birthdate']),'period_from':period_from,'period_to':period_to,'nbdays':nbdays,'amount':amount})
        try:
            os.remove(config['tempfolder']+'taxcertificates.pdf')
        except:
            pass
        renderer = appy.pod.renderer.Renderer(config['templatesfolder']+activitycat['taxcertificatetemplate'], {'childattestations':childattestations}, config['tempfolder']+'taxcertificates.pdf')                
        renderer.run()
        outfile = open(config['tempfolder']+"taxcertificates.pdf","r").read()
        out=base64.b64encode(outfile)
            
        return self.write(cr, uid, ids,{'state' : 'compute_taxcertificates','name':'taxcertificates.pdf','taxcertificates':out}, context=context)
extraschool_taxcertificates_wizard()
