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
from openerp.exceptions import Warning
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import *
import logging

_logger = logging.getLogger(__name__)

class extraschool_mainsettings(models.Model):
    _name = 'extraschool.mainsettings'
    _description = 'Main Settings'

    lastqrcodenbr = fields.Integer('lastqrcodenbr')
    qrencode = fields.Char('qrencode', size=80)
    tempfolder = fields.Char('tempfolder', size=80)
    templatesfolder = fields.Char('templatesfolder', size=80)
    codasfolder = fields.Char('codasfolder', size=80)
    processedcodasfolder = fields.Char('processedcodasfolder', size=80)
    emailfornotifications = fields.Char('Email for notifications', size=80)
    logo = fields.Binary()
    levelbeforedisable = fields.Many2one('extraschool.level', 'Level')
    last_child_upgrade_levels = fields.Date('Last child upgrade level', readonly=True)
    query_sql = fields.Text('Query Sql')
    sql_query_ids = fields.Many2one('extraschool.query_sql', 'Query SQL')
    parent_id = fields.Many2one('extraschool.parent', 'Parent')
    coda_date = fields.Date('CODA\'s date')
    amount = fields.Char('Amount')
    communication = fields.Char('Structured Communication')
    date_from = fields.Date('Date from')
    date_to = fields.Date('Date to')
    # Simulate PDA Transmission
    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place')
    activitycategoryid = fields.Many2one('extraschool.activitycategory', 'Activity Category')
    childid = fields.Many2one('extraschool.child', 'Child')
    prestation_date = fields.Date('Date')
    prestation_time = fields.Float('Time')
    type = fields.Selection((('pda','Smartphone'),
                           ('manuel','Encodage manuel')),'Type', default='pda' )
    prestation_times_encodage_manuel_id = fields.Many2one('extraschool.prestation_times_encodage_manuel', 'Encodage Manuel',ondelete='cascade')
    es = fields.Selection((('E','In'),
                           ('S','Out')),'ES' )
    prestation_times_of_the_day_id = fields.Many2one('extraschool.prestation_times_of_the_day', 'Prestation of the day',ondelete='cascade')
    pda_transmission_id = fields.Many2one('extraschool.pda_transmission', 'Transmission')

    @api.multi
    def send_presta(self):
        print "Hello World !"

    @api.multi
    def re_check_pod(self):
        cr = self.env.cr

        sql_query = """ SELECT DISTINCT(prestation_times_of_the_day_id) AS id
                        FROM extraschool_prestationtimes
                        WHERE activity_occurrence_id IS NULL AND prestation_date BETWEEN %s AND %s"""

        cr.execute(sql_query, (self.date_from, self.date_to))
        prestation_ids = cr.fetchall()

        prestations = self.env['extraschool.prestation_times_of_the_day'].browse([prestation_id[0] for prestation_id in prestation_ids])

        print "#Check POD without occurrence starting %s ...." % (len(prestations))
        for presta in prestations:
            presta.reset()
            presta.check()

    @api.multi
    def reset_check(self):
        cr = self.env.cr

        sql_query = """ SELECT id
                        FROM extraschool_prestationtimes
                        WHERE prestation_date BETWEEN %s AND %s"""

        cr.execute(sql_query, (self.date_from, self.date_to))
        prestation_ids = cr.fetchall()
        count = 0
        print "#Reset and check starting...."
        for prestation_id in prestation_ids:
            test = self.env['extraschool.prestation_times_of_the_day'].search([('prestationtime_ids', 'in', prestation_id)])
            if test:
                count += 1
                test.reset()
                test.check()
                print "## [%s/%s] done" % (count,len(prestation_ids))

    @api.multi
    def generate_coda(self):
        print "#Generation of CODA file"



        header_1 = "00000" + self.coda_date[8:10] + self.coda_date[5:7] + self.coda_date[2:4] + "30005        57181261  COMMUNE D'ASSESSE         BBRUBEBB   00000000000 00000                                       2"
        header_2 = "12171BE22363125809747                  EUR0000000160997990140917COMMUNE D'ASSESSE         Compte  vue                       171"

        amount = self.amount.split('.')
        euros = "0000000000000"
        euros = euros[0:(13 - len(amount[0]))] + amount[0]
        cents = "00"
        cents = cents[0:(2 - len(amount[1]))] + amount[1]
        naked_comm = ''
        for char in self.communication:
            if char != '/':
                naked_comm += char
        amount_line = "2100010000090545069I099002624  " + euros + cents +"0190917001500001101" + naked_comm + "                                      19091717101 0"

        filler = "2200010000                                                     NOTPROVIDED                        GKCCBEBB                   1 0"

        name = "                          "
        name = self.parent_id.name.upper() + name[len(self.parent_id.name):26]
        parent_name = "2300010000BE83063587614315                  " + name + "                                                       0 1"

        parent_address = "3200020001RUE DE BRIONSART        21         5340  GESVES                                                                    0 1"
        virement_line = "3100010002090545069I099002624  001500000Virement europen De: ISTA - FRAJER RUE DE BRIONSART 21 5340 GESVES Belgi            0 1"

        comm_line = "3100020003090546519I079002625  001500000que IBAN: BE83063587614315 Communication: ***" + self.communication + "***                       0 0"

        footer = "21000300003101983094049002623  0000000000000800190917001500001101200160019857                                      19091717101 0"

        file = open("/opt/coda/coda", "wb+")

        file.write(header_1 + "\n")
        file.write(header_2 + "\n")
        file.write(amount_line + "\n")
        file.write(filler + "\n")
        file.write(parent_name + "\n")
        file.write(parent_address + "\n")
        file.write(virement_line + "\n")
        file.write(comm_line + "\n")
        file.write(footer + "\n")

        file.close()

    @api.onchange('sql_query_ids')
    def _get_query_sql(self):
        self.query_sql = self.env['extraschool.query_sql'].browse(self.sql_query_ids.id).query

    @api.one
    def childupgradelevels(self):
        cr, uid = self.env.cr, self.env.user.id
        obj_child = self.pool.get('extraschool.child')
        obj_class = self.pool.get('extraschool.class')

        obj_level = self.pool.get('extraschool.level')
        obj_child = self.pool.get('extraschool.child')
        levelbeforedisable = obj_level.read(cr, uid, [self.levelbeforedisable.id], ['ordernumber'])[0]['ordernumber']
        cr.execute('select * from extraschool_child where create_date < %s', (str(datetime.now().year)+'-08-20',))
        print 'select * from extraschool_child where create_date < %s' % (str(datetime.now().year)+'-08-20')
        childs = cr.dictfetchall()
        cr.execute('select * from extraschool_level')
        levels = cr.dictfetchall()
        for child in childs:
            # if child['id'] == 403:
            #     import pdb;pdb.set_trace()
            cr.execute('select * from extraschool_class where id in (select class_id from extraschool_class_level_rel where level_id=%s) order by name',(str(child['levelid']),))
            childClasses = cr.dictfetchall()
            currentClassPosition = 0
            i=1
            for childClass in childClasses:
                if child['classid'] == childClass['id']:
                    currentClassPosition=i
                i=i+1
            childlevel = obj_level.read(cr, uid, [child['levelid']], ['ordernumber'])[0]
            newlevelid=0
            if childlevel['ordernumber'] < levelbeforedisable:
                for level in levels:
                    if newlevelid==0 and level['ordernumber'] > childlevel['ordernumber']:
                        newlevelid=level['id']
                cr.execute('select * from extraschool_class where id in (select class_id from extraschool_class_level_rel where level_id=%s) order by name',(str(newlevelid),))
                childClasses = cr.dictfetchall()
                newclassid=0
                if currentClassPosition > 0 and len(childClasses) != 0:
                    if len(childClasses) >= currentClassPosition:
                        newclassid = childClasses[currentClassPosition-1]['id']
                    else:
                        newclassid = childClasses[0]['id']
                    print "update child %s  oldclass: %s - old level : %s - class : %s - level : %s" % (child['id'],child['classid'],child['levelid'],newclassid,newlevelid)
                    obj_child.write(cr, uid, [child['id']], {'classid': newclassid,'levelid':newlevelid})
                else:
                    print "update child %s - old level : %s - level : %s" % (child['id'],child['levelid'],newlevelid)
                    obj_child.write(cr, uid, [child['id']], {'levelid':newlevelid})
            else:
                print "disable child %s" % (child['id'])
                obj_child.write(cr, uid, [child['id']], {'isdisabled': True})

        self.last_child_upgrade_levels = datetime.now()

    @api.one
    def update_presta_stat(self):
        self.env['extraschool.presta_stat'].compute()

    @api.multi
    def reset(self):
        for reg in self.env['extraschool.prestation_times_of_the_day'].browse(self._context.get('active_ids')):
            reg.reset()

        return True

    @api.multi
    def check(self):
        self.merge_pod_dup()
        for reg in self.env['extraschool.prestation_times_of_the_day'].search(
                [('id', 'in', self._context.get('active_ids')), ]):
            reg.check()

        return True

    @api.multi
    def last_check_entry_exit(self):
        for reg in self.env['extraschool.prestation_times_of_the_day'].browse(self._context.get('active_ids')):
            reg.last_check_entry_exit()

        return True

    @api.multi
    def execute_sql(self):
        self.env.cr.execute(self.query_sql)

    @api.multi
    def del_pod_doublon(self):
        pda_doublon = """
                        select id, activity_category_id, date_of_the_day, child_id
                        from extraschool_prestation_times_of_the_day
                        where ('' || CASE WHEN activity_category_id is NULL 
                                THEN ''
                                ELSE activity_category_id::text END || to_char(date_of_the_day,'YYYY-MM-DD') || child_id) in ( 
                        select ('' || CASE WHEN activity_category_id is NULL 
                                THEN ''
                                ELSE activity_category_id::text END || to_char(date_of_the_day,'YYYY-MM-DD') || child_id) as zz
                        from extraschool_prestation_times_of_the_day
                        where date_of_the_day > '2016-02-01' 
                        group by zz
                        having count(*) > 1);
                    """
        self.env.cr.execute(pda_doublon)

        prestation_times_of_the_day_obj = self.env['extraschool.prestation_times_of_the_day']
        prestation_times_obj = self.env['extraschool.prestationtimes']
        pdaprestation_times_obj = self.env['extraschool.pdaprestationtimes']

        doublons = self.env.cr.dictfetchall()
        saved_activity_category_id = ''
        saved_date = ''
        saved_child = ''
        for doublon in doublons:
            if saved_activity_category_id != doublon['activity_category_id'] or saved_date != doublon[
                'date_of_the_day'] or saved_child != doublon['child_id']:
                saved_activity_category_id = doublon['activity_category_id']
                saved_date = doublon['date_of_the_day']
                saved_child = doublon['child_id']
            else:
                prestation_times_obj.search([('prestation_times_of_the_day_id', '=', doublon['id'])]).unlink()
                pdaprestation_times_obj.search([('prestation_times_of_the_day_id', '=', doublon['id'])]).unlink()
                prestation_times_of_the_day_obj.search([('id', '=', doublon['id'])]).unlink()

    @api.multi
    def merge_pod_dup(self):
        self.env['extraschool.prestation_times_of_the_day'].merge_duplicate_pod()

    @api.multi
    def reset_verified_pod_with_non_verified_presta(self):
        pod_error = """
                        select distinct(prestation_times_of_the_day_id) as id
                        from extraschool_prestationtimes p
                        left join extraschool_prestation_times_of_the_day pod on pod.id = p.prestation_times_of_the_day_id
                        where p.verified = False and pod.verified = False;
                    """
        self.env.cr.execute(pod_error)

        pod_errors = self.env.cr.dictfetchall()
        pod_error_ids = [doublon['id'] for doublon in pod_errors]

        self.env['extraschool.prestation_times_of_the_day'].browse(pod_error_ids).reset()


    @api.multi
    def reset_biller(self):
        self.env['extraschool.biller'].search([]).write({'in_creation': False})

    @api.multi
    def reconcil_all(self):
        invoice_ids = self.env['extraschool.invoice'].search([('balance', '!=', 0), ('tag', '=', None)])

        _logger.info("Start of reconcil: %s needed", (len(invoice_ids)))
        for invoice in invoice_ids:
            invoice.reconcil()
        _logger.info("End of reconcil")

    @api.multi
    def update_commstruct(self):
        self.env['extraschool.parent'].update_commstruct()

    @api.multi
    def reprise_signaletic(self):
        """
        First phase. Get all the infos from activity category and put them in organising power.
        :return:
        """
        activity_category = self.env['extraschool.activitycategory'].search([])[0]

        self.env['extraschool.organising_power'].search([])[0].write({
            'po_name': activity_category.po_name,
            'po_street': activity_category.po_street,
            'po_email': activity_category.po_email,
            'po_zipcode': activity_category.po_zipcode,
            'po_city': activity_category.po_city,
            'po_sign': activity_category.po_sign,
            'po_stamp': activity_category.po_stamp,
            'po_tel': activity_category.po_tel,
            'po_addresse_free_text': activity_category.po_addresse_free_text,
            'po_addresse_free_text2': activity_category.po_addresse_free_text2,
            'po_resp_name': activity_category.po_resp_name,
            'po_resp_fct': activity_category.po_resp_fct,
            'po_sign_img': activity_category.po_sign_img,
            'po_resp2_name': activity_category.po_resp2_name,
            'po_resp2_fct': activity_category.po_resp2_fct,
            'po_resp2_sign': activity_category.po_resp2_sign,
            'po_rappel_name': activity_category.po_rappel_name,
            'po_rappel_fct': activity_category.po_rappel_fct,
            'po_rappel_sign': activity_category.po_rappel_sign,
            'po_attestation_name': activity_category.po_attestation_name,
            'po_attestation_fct': activity_category.po_attestation_fct,
            'po_attestation_sign': activity_category.po_attestation_sign,
            'logo': activity_category.logo,
            'slogan': activity_category.slogan,
            'taxcertificatetemplate': activity_category.taxcertificatetemplate,
            'max_school_implantation': activity_category.max_school_implantation,
            'town': activity_category.po_city,
            'qrcode_report_id': activity_category.qrcode_report_id.id,
        })
