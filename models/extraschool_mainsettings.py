# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
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

from openerp import models, api, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import *
import logging

_logger = logging.getLogger(__name__)

class extraschool_mainsettings(models.Model):
    _name = 'extraschool.mainsettings'
    _description = 'Main Settings'

    def _get_level_ready_status(self):
        biller_id = self.env['extraschool.biller'].search([], order='id DESC', limit=1)
        current_year = datetime.now().year
        if biller_id.period_from == "{}-06-01".format(current_year) and biller_id.period__to == "{}-06-30".format(
            current_year):
            return True
        return False

    lastqrcodenbr = fields.Integer('lastqrcodenbr')
    qrencode = fields.Char('qrencode', size=80)
    tempfolder = fields.Char('tempfolder', size=80)
    templatesfolder = fields.Char('templatesfolder', size=80)
    codasfolder = fields.Char('codasfolder', size=80)
    processedcodasfolder = fields.Char('processedcodasfolder', size=80)
    emailfornotifications = fields.Char('Email for notifications', size=80)
    logo = fields.Binary()
    levelbeforedisable = fields.Many2one('extraschool.level', string='Level to not upgrade')
    last_level_id = fields.Many2one('extraschool.level', string='Last level before disabling')
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
    reminder_journal_id = fields.Many2one(
        'extraschool.remindersjournal'
    )
    date_child_upgrade = fields.Date()
    date_revert_upgrade = fields.Date()
    upgrade_level_ready = fields.Boolean()
    limit_date_delete_presta = fields.Date(string="On supprimer les presta AVANT cette date (non incluse)")

    pdf_true_biller = fields.Boolean(string="Les facturiers")
    pdf_true_tax = fields.Boolean(string="Les attestations fiscales")
    level = fields.Many2one('extraschool.level', string='Level')
    type_child = fields.Many2one('extraschool.childtype', string='Type')

    @api.multi
    def update_comm_struct(self):
        new_prefix = self.env['extraschool.activitycategory'].search([])[0].remindercomstructprefix
        for rec in self:
            for reminder in rec.reminder_journal_id.reminder_ids:
                old_prefix = reminder.structcom[3:6]
                reminder.structcom = reminder.structcom.replace(old_prefix, new_prefix, 1)

    @api.multi
    def re_check_pod(self):
        cr = self.env.cr

        sql_query = """ SELECT DISTINCT(prestation_times_of_the_day_id) AS id
                        FROM extraschool_prestationtimes
                        WHERE activity_occurrence_id IS NULL AND prestation_date BETWEEN %s AND %s"""

        cr.execute(sql_query, (self.date_from, self.date_to))
        prestation_ids = cr.fetchall()

        prestations = self.env['extraschool.prestation_times_of_the_day'].browse([prestation_id[0] for prestation_id in prestation_ids])

        logging.info("#Check POD without occurrence starting {} ....".format(len(prestations)))
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
        logging.info("#Reset and check starting....")
        for prestation_id in prestation_ids:
            test = self.env['extraschool.prestation_times_of_the_day'].search([('prestationtime_ids', 'in', prestation_id)])
            if test:
                count += 1
                test.reset()
                test.check()
                logging.info("## [{}/{}] done".format(count, len(prestation_ids)))

    @api.multi
    def generate_coda(self):
        logging.info("#Generation of CODA file")



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

    # region Children Upgrade Level
    @api.multi
    def childupgradelevels(self):
        """
        This upgrade children to the next level.
        - If we set a date, we only change levels for children created before the date.
        - It's not possible to do this if there are no biller in June.
        - We also need to clean the old_level_id from last year.
        - First we make sure the table level has the correct ordernumber (0,1,2...)
        that correspond to the right level (1ere maternelle, 2eme maternelle, ...).
        - Then we save the current level of each child in case we need a revert.
        - Finally we change the level of each children. If the child is in the last level, we disable it
        :return: True if ok False if not (or a raise)
        """
        for rec in self:
            # Check the level correctness.
            if rec._is_level_table_correct():
                # Clean old_level_id
                rec.clean_old_level_id()

                domain = [('isdisabled', '=', False)]
                last_level = False

                # Change domain if there is a date.
                if rec.date_child_upgrade:
                    domain.append(('create_date', '<=', rec.date_child_upgrade))
                if rec.levelbeforedisable:
                    domain.append(('levelid', '!=', rec.levelbeforedisable.id))
                if rec.last_level_id:
                    last_level = rec.last_level_id

                child_ids = rec.env['extraschool.child'].search(domain)

                # Save current status for revert
                _logger.info("Re-creating old level id")
                for child_id in child_ids:
                    child_id.write({
                        'old_level_id': child_id.levelid.id,
                        'old_class_id': child_id.classid.id
                    })

                # Upgrade child level.
                # If last level put in disable
                # Else upgrade level
                _logger.info("Updating children level")
                level_ids = self.env['extraschool.level'].search([])
                for child_id in child_ids:
                    order_number = level_ids.filtered(lambda r: r.id == child_id.levelid.id).ordernumber
                    next_level_id = level_ids.filtered(lambda r: r.ordernumber == order_number + 1).id
                    if last_level and child_id.levelid.id == last_level.id:
                        child_id.write({
                            'isdisabled': True,
                        })
                    else:
                        class_id = rec.env['extraschool.class'].search(
                            [('schoolimplantation', '=', child_id.schoolimplantation.id),
                             ('levelids', '=', next_level_id)])

                        child_id.write({
                            'levelid': next_level_id,
                            'classid': class_id.id if len(class_id) == 1 else None,
                        })

                _logger.info("Checking if upgrade was successfull")
                if not rec._check_upgrade():
                    _logger.error("The upgrade is not correct.")
                    raise Warning(_("We checked the upgrade and it is not correct."))

                rec.last_child_upgrade_levels = datetime.now()
            else:
                _logger.error("The table of levels is not correctly formated")
                raise Warning(_("The table of levels is not correctly formated. You need to correct that"))

    @api.multi
    def clean_old_level_id(self):
        """
        Select all children with an old level id and class id and remove it.
        :return:
        """
        _logger.info("Cleaning old level id")
        try:
            for child in self.env['extraschool.child'].search([('old_level_id', '!=', None)]):
                child.write({
                    'old_level_id': None,
                    'old_class_id': None,
                })
        except:
            _logger.error("There has been an error on the cleaning of old level id")
            raise Warning(_("There has been an error on the cleaning of old level id"))

    @api.multi
    def _check_upgrade(self):
        """
        First check all upgraded children not disabled that they have been put on a +1 level
        Second check for all disabled children with an old level that they have an old_level_id
        :return: True when everything is ok, else False
        """
        child_ids = self.env['extraschool.child'].search([('old_level_id', '!=', None)])
        level_ids = self.env['extraschool.level'].search([])

        for child_id in child_ids.filtered(lambda r: r.isdisabled is False):
            current_level_id = level_ids.filtered(lambda r: r.id == child_id.levelid.id).ordernumber
            old_level_id = level_ids.filtered(lambda r: r.id == child_id.old_level_id.id).ordernumber

            if current_level_id - old_level_id != 1:
                return False
        # last_level = self.env['extraschool.level'].search([], order='ordernumber DESC', limit=1)

        # for child_id in child_ids.filtered(lambda r: r.old_level_id.id == last_level.id):
        #     if not child_id.isdisabled:
        #         return False

        return True

    @api.multi
    def _is_level_table_correct(self):
        """
        Check if the level table will correspond with our upgrade code.
        :return: True when it's ok, else False
        """
        level_obj = self.env['extraschool.level']
        mapped_level = self._get_mapped_level()

        for order in range(10):
            if level_obj.search([('ordernumber', '=', order)]).name != mapped_level[order]:
                print("{} {}".format(level_obj.search([('ordernumber', '=', order)]).name, mapped_level[order]))
                return False

        return True

    @api.multi
    def _get_mapped_level(self):
        return [
            u'accueil',
            u'1ere maternelle',
            u'2eme maternelle',
            u'3eme maternelle',
            u'1ere primaire',
            u'2eme primaire',
            u'3eme primaire',
            u'4eme primaire',
            u'5eme primaire',
            u'6eme primaire',
        ]

    @api.multi
    def revert_upgrade(self):
        _logger.info("Reverting Upgrade Children")
        child_ids = self.env['extraschool.child'].search([('old_level_id', '!=', None)])

        if not child_ids:
            _logger.error("There are no children to revert")
            raise Warning(_("There are no children to revert"))
        else:
            if self.last_level_id:
                last_level = self.last_level_id
            for child_id in child_ids:
                if child_id.old_level_id.id == last_level.id:
                    child_id.write({
                        'isdisabled': False,
                    })
                else:
                    child_id.write({
                        'levelid': child_id.old_level_id.id,
                        'classid': child_id.old_class_id.id,
                    })

            self.clean_old_level_id()

            self.date_revert_upgrade = datetime.now()
    # endregion

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

    # region Bouton pour Coralie
    @api.multi
    def mettet_grandprimaire(self):
        maternelle = ["1ere maternelle", "2eme maternelle", "3eme maternelle"]
        petit_primaire = ["1ere primaire", "2eme primaire", "3eme primaire"]
        grand_primaire = ["4eme primaire", "5eme primaire", "6eme primaire"]
        child_ids = self.env['extraschool.child'].search([('isdisabled', '=', False)])

        for child_id in child_ids:
            if child_id.levelid.name in maternelle:
                class_id = 136
            elif child_id.levelid.name in petit_primaire:
                class_id = 137
            elif child_id.levelid.name in grand_primaire:
                class_id = 138

            child_id.write({
                'classid': class_id
            })

    @api.multi
    def type_grandprimaire(self):
        type = self.type_child
        level = self.level
        child_ids = self.env['extraschool.child'].search([('isdisabled', '=', False)])

        for child_id in child_ids:
            if child_id.levelid.name == level.name :
                child_id.childtypeid = type

                child_id.write({
                    'childtypeid': type.id
                })

    @api.multi
    def delete_presta_test(self):
        try:
            pda_prestation_time_ids = self.env['extraschool.pdaprestationtimes'].search(
                [('prestation_date', '<', self.limit_date_delete_presta)])
            for pda_prestation in pda_prestation_time_ids:
                pda_prestation.unlink()

            prestation_times_ids = self.env['extraschool.prestationtimes'].search(
                [('prestation_date', '<', self.limit_date_delete_presta)]
            )
            for prestation_times_id in prestation_times_ids:
                prestation_times_id.unlink()

            potd_ids = self.env['extraschool.prestation_times_of_the_day'].search([
                ('date_of_the_day', '<', self.limit_date_delete_presta)
            ])
            for potd in potd_ids:
                potd.unlink()
        except:
            raise Warning("Il y a probablement une inscription ou un encodage manuel non supprimé à cette date.")

    @api.multi
    def put_upper_address(self):
        parent_ids = self.env['extraschool.parent'].search([])
        for parent_id in parent_ids:
            parent_id.write({
                'street': parent_id.street.upper(),
                'city': parent_id.city.upper(),
            })

    @api.multi
    def virgule_address(self):
        parent_ids = self.env['extraschool.parent'].search([])
        for parent_id in parent_ids:
            parent_id.write({
                'street': parent_id.street.replace(',', ''),
            })

    @api.multi
    def put_rn_onyx(self):
        parent_ids = self.env['extraschool.parent'].search([])
        for parent_id in parent_ids:
            print parent_id.rn
            new_rn = parent_id.rn
            if parent_id.rn :
                if ' ' in parent_id.rn:
                    new_rn = parent_id.rn.replace(' ', '')
                if '-' in parent_id.rn :
                    new_rn = parent_id.rn.replace('-','')
                if '.' in parent_id.rn:
                    new_rn = parent_id.rn.replace('.', '')
                print "neeeeeeeeex", new_rn
            parent_id.write({
                    'rn': new_rn,
                })

    @api.multi
    def put_rn_onyx_child(self):
        child_ids = self.env['extraschool.child'].search([])
        for child_id in child_ids:
            print child_id.rn
            new_rn = child_id.rn
            if child_id.rn:
                if ' ' in child_id.rn:
                    new_rn = child_id.rn.replace(' ', '')
                if '-' in child_id.rn:
                    new_rn = child_id.rn.replace('-', '')
                if '.' in child_id.rn:
                    new_rn = child_id.rn.replace('.', '')
                print new_rn
            child_id.write({
                    'rn': new_rn,
                })

    @api.multi
    def pdf_to_true(self):
        if not self.pdf_true_biller and not self.pdf_true_tax:
            raise Warning("Il faut sélectionner un truc !!!")

        if self.pdf_true_biller:
            biller_ids = self.env['extraschool.biller'].search([('pdf_ready', '=', False)])
            for biller_id in biller_ids:
                biller_id.write({
                    'pdf_ready': True,
                    'in_creation': False,
                })

        if self.pdf_true_tax:
            tax_ids = self.env['extraschool.taxcertificate'].search([('pdf_ready', '=', False)])
            for tax_id in tax_ids:
                tax_id.write({
                    'pdf_ready': True,
                })

    @api.multi
    def delete_age_group(self):
        for age_group in self.env['extraschool.age_group'].search([]):
            if age_group.age_from == 0 and age_group.age_to == 0:
                age_group.unlink()

    @api.multi
    def delete_doctors(self):
        for doctor in self.env['extraschool.doctor'].search([]):
            doctor.unlink()

    @api.multi
    def delete_allergies(self):
        for allergy in self.env['extraschool.allergy'].search([]):
            allergy.unlink()

    @api.multi
    def delete_disease_type(self):
        for disease_type in self.env['extraschool.disease_type'].search([]):
            disease_type.unlink()
    # endregion
