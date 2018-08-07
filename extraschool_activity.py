# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia- Imio (<http://www.imio.be>).
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
    #    registration_only = fields.Boolean('Registration only')

from openerp.api import Environment
from openerp.exceptions import except_orm, Warning
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)

from openerp.tools.misc import profile
from datetime import date, datetime, timedelta as td
import time
import pdb
from openerp.exceptions import except_orm, Warning, RedirectWarning

import extraschool_activityplanneddate


class extraschool_activity(models.Model):
    _name = 'extraschool.activity'
    _description = 'activity'
    _inherit = 'mail.thread'

    name = fields.Char('Name', required=True)

    def _get_activity_category_id(self):
        return self.env['extraschool.activitycategory'].search([])[0].filtered('id').id

    category = fields.Many2one('extraschool.activitycategory', 'Category', required=True, track_visibility='onchange', default=_get_activity_category_id)
    parent_id = fields.Many2one('extraschool.activity', 'Parent', index=True, track_visibility='onchange')
    root_id = fields.Many2one('extraschool.activity', 'Root', compute='_compute_root_activity', store=True, index=True, track_visibility='onchange')
    activity_child_ids = fields.One2many('extraschool.activity', 'parent_id', 'Activity child', track_visibility='onchange')
    placeids = fields.Many2many('extraschool.place', 'extraschool_activity_place_rel', 'activity_id', 'place_id', 'Schoolcare place', required=True, track_visibility='onchange')
    schoolimplantationids = fields.Many2many('extraschool.schoolimplantation', 'extraschool_activity_schoolimplantation_rel', 'activity_id', 'schoolimplantation_id', 'Schoolcare schoolimplantation', track_visibility='onchange')
    short_name = fields.Char('Short name', index=True, required=True)
    childtype_ids = fields.Many2many('extraschool.childtype', 'extraschool_activity_childtype_rel', 'activity_id', 'childtype_id', 'Child type', track_visibility='onchange')
    childregistration_ids = fields.One2many('extraschool.activitychildregistration', 'activity_id', 'Child registrations', track_visibility='onchange')
    autoaddchilds = fields.Boolean('Auto add registered', track_visibility='onchange')
    onlyregisteredchilds = fields.Boolean('Only registered childs', index=True, track_visibility='onchange')
    planneddates_ids = fields.Many2many('extraschool.activityplanneddate', 'extraschool_activity_activityplanneddate_rel', 'activity_id', 'activityplanneddate_id', 'Planned dates', track_visibility='onchange')
    exclusiondates_ids = fields.Many2many('extraschool.activityexclusiondates', 'extraschool_activity_activityexclusiondates_rel', 'activity_id', 'activityexclusiondates_id', 'Exclusion dates', track_visibility='onchange')
    days = fields.Selection((('0,1,2,3,4', 'All Monday to Friday'), ('0', 'All Mondays'), ('1', 'All Tuesdays'), ('2', 'All Wednesdays'), ('3', 'All Thursdays'), ('4', 'All Fridays'), ('0,1,3,4', 'All Mondays, Tuesdays, Thursday and Friday')), 'Days', required=True, track_visibility='onchange')
    leveltype = fields.Selection((('M,P', 'Maternelle et Primaire'), ('M', 'Maternelle'), ('P', 'Primaire')), 'Level type', required=True, track_visibility='onchange')
    prest_from = fields.Float('From', index=True, required=True, track_visibility='onchange')
    prest_to = fields.Float('To', index=True, required=True, track_visibility='onchange')
    price = fields.Float('Price', digits=(7, 3), track_visibility='onchange')
    price_list_id = fields.Many2one('extraschool.price_list', 'Price List', track_visibility='onchange')
    period_duration = fields.Integer('Period Duration', track_visibility='onchange')
    default_from_to = fields.Selection((('from', 'default_from_to From'), ('to', 'default_from_to To'), ('from_to', 'default_from_to From and To')), 'default_from_to Default From To', required=True, track_visibility='onchange')
    default_from = fields.Float('Default from', track_visibility='onchange')
    default_to = fields.Float('Default to', track_visibility='onchange')
    fixedperiod = fields.Boolean('Fixed period', default=False)
    subsidizedbyone = fields.Boolean('Subsidized by one')
    on_tax_certificate = fields.Boolean('On tax certificate', select=True, track_visibility='onchange')
    tarif_group_name = fields.Char('Tarif group name', index=True, track_visibility='onchange')
    validity_from = fields.Date('Validity from', index=True, required=True, track_visibility='onchange')
    validity_to = fields.Date('Validity to', index=True, required=True, track_visibility='onchange')
    selectable_on_registration = fields.Boolean('Selectable on registration form')
    selectable_on_registration_multi = fields.Boolean('Selectable on registration multi form')
    warning_date = fields.Char('WARNING', default="ATTENTION, Modifier une activité peut impacter les présences déjà vérifiées ! Pour touts changements, Il est préférabl de contacter directement Imio.", readonly=True)
    warning_visibility = fields.Boolean(track_visibility='onchange')
    expire_soon = fields.Boolean(compute='_get_expired_date')

    @api.multi
    def _get_expired_date(self):
        for rec in self:
            date_to_check = fields.Date.from_string(rec.validity_to) - datetime.now().date()
            if date_to_check.total_seconds() < 2592000:
                rec.expire_soon = True;

    @api.onchange('parent_id')
    @api.depends('parent_id')
    def _compute_root_activity(self):
        # To do à déplacer ds activity
        for activity in self:
            # set root activity_id if
            if activity.parent_id:
                parent = activity.parent_id
                while parent.parent_id:
                    parent = parent.parent_id
                activity.root_id = parent
            else:
                activity.root_id = activity.id

    def build_timestamp(self, tsdate, tstime):
        hour = int(tstime)
        minute = int((tstime - hour) * 60)
        hour = hour - 1 if hour else 0
        return datetime.strptime(tsdate + ' ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00', DEFAULT_SERVER_DATETIME_FORMAT)

    def populate_occurrence(self, date_from=None, date_to=None):
        cr, uid = self.env.cr, self.env.user.id

        activityoccurrence = self.env['extraschool.activityoccurrence']
        for activity in self:
            if len(activity.planneddates_ids):
                for planneddate in activity.planneddates_ids:
                    for place in activity.placeids:
                        activityoccurrence.create({'place_id': place.id,
                                                   'occurrence_date': datetime.strptime(planneddate.activitydate, DEFAULT_SERVER_DATE_FORMAT),
                                                   'activityid': activity.id,
                                                   'prest_from': activity.prest_from,
                                                   'prest_to': activity.prest_to,
                                                   })
            else:
                d1 = activity.validity_from
                if date_from and date_from > activity.validity_from:
                    d1 = date_from

                d2 = date_to if date_to else activity.validity_to
                print "populate_occurrence date_to : %s" % (d2)
                d1 = datetime.strptime(d1, DEFAULT_SERVER_DATE_FORMAT)
                d2 = datetime.strptime(d2, DEFAULT_SERVER_DATE_FORMAT)

                delta = d2 - d1
                # insert_data = ''
                print str(datetime.now())+" START"
                args = []
                for day in range(delta.days + 1):
                    print "day %s" % day
                    current_day_date = d1 + td(days=day)
                    if str(current_day_date.weekday()) in activity.days:
                        cr.execute('select count(*) from extraschool_activity_activityexclusiondates_rel as ear inner join extraschool_activityexclusiondates as ea on ear.activityexclusiondates_id = ea.id where activity_id = %s and date_from <= %s and date_to >= %s', (activity.id, current_day_date, current_day_date))
                        exclu_activity_id = cr.fetchall()
                        if exclu_activity_id[0][0] == 0:
                            for place in activity.placeids:
                                # if insert_data:
                                #     insert_data.join(',')
                                # '''
                                # activityoccurrence.create({'place_id' : place.id,
                                #                           'occurrence_date' : current_day_date,
                                #                           'activityid' : activity.id,
                                #                           'prest_from' : activity.prest_from,
                                #                           'prest_to' : activity.prest_to,
                                #                           })
                                # '''
                                str_current_day_date = str(current_day_date)[:10]
                                args.append((uid,
                                             self.build_timestamp(str_current_day_date, activity.prest_to),
                                             self.build_timestamp(str_current_day_date, activity.prest_from),
                                             activity.name + ' - ' + str_current_day_date,
                                             uid,
                                             activity.category.id,
                                             place.id,
                                             current_day_date,
                                             activity.id,
                                             activity.prest_from,
                                             activity.prest_to))

                                # insert_data = insert_data.join('('+str(place.id)+','+str(current_day_date)+','+str(activity.id)+','+str(activity.prest_from)+','+str(activity.prest_to)+')')
                if len(args):
                    print str(datetime.now())+" Build query2"
                    args_str = ','.join(cr.mogrify("(%s,%s,%s,current_timestamp,%s,%s,current_timestamp,%s,%s,%s,%s,%s,%s)", x) for x in args)
                    print str(datetime.now())+" START QUERY"
                    # print insert_data
                    cr.execute("insert into extraschool_activityoccurrence (create_uid,date_stop,date_start,create_date,name,write_uid,write_date,activity_category_id,place_id,occurrence_date,activityid,prest_from,prest_to) VALUES "+args_str)
                    print str(datetime.now())+" END"
                    # get ids of created occu
                    cr.execute("""select id 
                                from extraschool_activityoccurrence 
                                where create_uid = %s
                                and activityid = %s
                                """, (uid, activity.id))
                    occurrence_ids = [id['id'] for id in cr.dictfetchall()]
                    print "ids created : %s" % (occurrence_ids)
                    for occu in self.env['extraschool.activityoccurrence'].search([('id', 'in', occurrence_ids)]):
                        occu.auto_add_registered_childs()

    def check_if_modifiable(self, vals):
        print "# Start of the modification process........"
        start_time = time.time()
        invoiced_obj = self.env['extraschool.invoicedprestations']
        # There goes the rabbit hole
        # # If there is an invoiced prestation for the activity.
        if (invoiced_obj.search(
                [('activity_occurrence_id.activityid', '=', self.id)])):
            date_last_invoice = vals['validity_from'] if 'validity_from' in vals else self.validity_from
            activity_occurrence_ids = self.env['extraschool.activityoccurrence'].search([('activityid', '=', self.id),
                ('occurrence_date', '>=', date_last_invoice),
            ])
        else:
            activity_occurrence_ids = self.env['extraschool.activityoccurrence'].search([('activityid', '=', self.id)])
            date_last_invoice = self.validity_from

        child_registration_id__list = []
        # For each Activity Occurence get the list of the activity_occurrence_child_registration IDs.
        child_registration_ids = self.env['extraschool.activity_occurrence_child_registration'] \
            .search([('activity_occurrence_id', 'in', activity_occurrence_ids.ids)])

        print "# Building children's list"
        for child_registration_id in child_registration_ids:
            # For each Child Registration Line get Child Registration ID.
            child_registration = child_registration_id.child_registration_line_id.child_registration_id.id

            if child_registration not in child_registration_id__list:
                child_registration_id__list.append(child_registration)

        print "# Getting registration of children"
        # Set the child registration to draft.
        child_registration_compute = self.env['extraschool.child_registration'].search([
            ('id', 'in', child_registration_id__list)
        ])

        print "# Putting children to: set to draft"
        child_registration_compute.set_to_draft()

        prestation_time_id_list = []
        prestation_time_ids = self.env['extraschool.prestationtimes'].search([
            ('activity_occurrence_id', 'in', activity_occurrence_ids.ids)
        ])

        print "# Building Prestation Time of the Day list"
        for prestation_time_id in prestation_time_ids:
            prestation_time_of_the_day = prestation_time_id.prestation_times_of_the_day_id.id

            if prestation_time_of_the_day not in prestation_time_id_list:
                # Add DISTINCT ID to the Prestation Time Of The Day ID
                prestation_time_id_list.append(prestation_time_of_the_day)

        print "# Getting POD that we need"
        # Reset Prestation Times of the Day
        prestation_time_compute = self.env['extraschool.prestation_times_of_the_day'].search([
            ('id', 'in', prestation_time_id_list)
        ])

        print "# Number of reset required: ", len(prestation_time_compute)
        prestation_time_compute.reset()

        print "# Unlink occurrences"
        activity_occurrence_ids.unlink()

        super(extraschool_activity, self).write(vals)

        print "# Populate occurrences"
        self.populate_occurrence(date_last_invoice)

        print "# Validate children's registration"
        child_registration_compute.validate_multi()

        if 'multi_write' not in vals:
            print "# Check Prestations"
            total = len(prestation_time_compute)
            for presta in prestation_time_compute:
                print total
                total -= 1
                presta.check()

        print "Final time: ", time.strftime('%M:%S', time.gmtime((time.time() - start_time)))
        self.warning_visibility = False

    @api.multi
    def check_validity_date(self, vals):
        # Check if values has passed (create or write). If not take from parent Object.
        validity_from = vals['validity_from'] if 'validity_from' in vals else self.validity_from
        validity_to = vals['validity_to'] if 'validity_to' in vals else self.validity_to
        prest_from = vals['prest_from'] if 'prest_from' in vals else self.prest_from
        prest_to = vals['prest_to'] if 'prest_to' in vals else self.prest_to

        planneddates_ids = self.env['extraschool.activityplanneddate'].browse(
            vals['planneddates_ids'][0][-1]) if vals.get('planneddates_ids') else self.planneddates_ids
        exclusiondates_ids = self.env['extraschool.activityexclusiondates'].browse(
            vals['exclusiondates_ids'][0][-1]) if vals.get('exclusiondates_ids') else self.exclusiondates_ids

        # Check Valid Hour.
        if prest_from == 0:
            raise Warning(_("Hour must be greater than 0"))

        if prest_to == prest_from:
            raise Warning(_("Debut hour is equal to final hour"))

        # Check Date.
        if validity_from > validity_to:
            raise Warning(_("Validity to must be greater than validity from (date)"))

        # Check Hour.
        if prest_from > prest_to:
            raise Warning(_("Validity to must be greater than validity from (hours)"))

        # Check Planned Dates
        for planneddates_id in planneddates_ids:
            if planneddates_id.activitydate < validity_from or planneddates_id.activitydate > validity_to:
                raise Warning(_("Planned Dates must be in the range of Validity_to and Validity_from (Planned)"))

        # Check Exclusion Dates
        for exclusiondates_id in exclusiondates_ids:
            if exclusiondates_id.date_from < validity_from or exclusiondates_id.date_to > validity_to:
                raise Warning(_("Date_from must be in range of Validity_from and Validity_to (Exclusion)"))

    @api.onchange('validity_from','validity_to','planneddates_ids','exclusiondates_ids','parent_id','placeids','leveltype','prest_from','prest_to','days')
    @api.multi
    def check_validity_from_invoice(self,origin_id=0):
        if not origin_id:
            origin_id = self._origin.id
        else:
            origin_id = self.id
        print "# Check if there is an invoice prestation at the current date"
        cr = self.env.cr
        invoiced_obj = self.env['extraschool.invoicedprestations']
        # If there is an invoiced prestation for the activity.
        if (invoiced_obj.search(
                [('activity_occurrence_id.activityid', '=', origin_id)])):
            # Get the date of the last invoice for this activity.
            cr.execute("SELECT prestation_date FROM extraschool_invoicedprestations WHERE activity_activity_id = %s ORDER BY prestation_date DESC LIMIT 1" % (origin_id))
            # Trop lent.
            # date_last_invoice = invoiced_obj.search([('activity_activity_id', '=', self._origin.id)],
            #                                         order='prestation_date DESC', limit=1).prestation_date
            date_last_invoice = cr.fetchone()
            date_last_invoice = fields.Date.from_string(date_last_invoice[0]) + td(days=1)
            self.warning_visibility = True
            if fields.Date.from_string(self.validity_from) < date_last_invoice:
                self.validity_from = date_last_invoice

        return self.validity_from

    @api.multi
    def write(self, vals):
        for activity in self:
            print "# Modification of an activity -------------------"
            # Check Validity Date & Hour.
            self.check_validity_date(vals)

            # This will go through a specific process if there is one change in these fields.
            if 'validity_from' in vals \
                    or 'validity_to' in vals \
                    or 'planneddates_ids' in vals \
                    or 'exclusiondates_ids' in vals \
                    or 'parent_id' in vals \
                    or 'placeids' in vals \
                    or 'leveltype' in vals \
                    or 'prest_from' in vals \
                    or 'prest_to' in vals \
                    or 'days' in vals:
                # Follow the white rabbit.
                self.check_if_modifiable(vals)

            else:
                super(extraschool_activity, self).write(vals)

        return True

    @api.model
    def create(self, vals):
        # Check Validity Date & Hour.
        self.check_validity_date(vals)

        res = super(extraschool_activity, self).create(vals)

        if res:
            res.populate_occurrence()

        return res

    def get_start(self, activity):
        if activity.default_from_to == 'from' or activity.default_from_to == 'from_to':
            return activity.prest_from
        else:
            return False

    def get_stop(self, activity):
        if activity.default_from_to == 'to' or activity.default_from_to == 'from_to':
            return activity.prest_to
        else:
            return False

extraschool_activity()

