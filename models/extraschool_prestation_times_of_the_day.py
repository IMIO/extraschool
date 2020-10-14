# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
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
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
import datetime
import time
import logging

_logger = logging.getLogger(__name__)


class extraschool_prestation_times_of_the_day(models.Model):
    _name = 'extraschool.prestation_times_of_the_day'
    _order = 'date_of_the_day desc, child_lastname, child_firstname'

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []

        res = []
        for presta in self.browse(cr, uid, ids, context=context):
            res.append((presta.id, presta.child_id.name + ' - ' + datetime.datetime.strptime(presta.date_of_the_day,
                                                                                             DEFAULT_SERVER_DATE_FORMAT).strftime(
                "%d-%m-%Y")))

        return res

    date_of_the_day = fields.Date(required=True, select=True)
    child_id = fields.Many2one('extraschool.child', required=True, select=True)
    prestationtime_ids = fields.One2many(comodel_name="extraschool.prestationtimes",
                                         inverse_name="prestation_times_of_the_day_id")
    pda_prestationtime_ids = fields.One2many(comodel_name="extraschool.pdaprestationtimes",
                                             inverse_name="prestation_times_of_the_day_id",
                                             domain=['|', ('active', '=', False), ('active', '=', True)])
    verified = fields.Boolean(select=True)
    place_check = fields.Boolean(default=True)
    comment = fields.Text()
    checked = fields.Boolean(default=False)
    child_level = fields.Many2one('extraschool.level', related="child_id.levelid", index=True)
    parent_id = fields.Many2one(related='child_id.parentid', store=True, select=True)
    schoolimplantation = fields.Many2one(related="child_id.schoolimplantation", store=True)
    child_firstname = fields.Char(related="child_id.firstname", store=True)
    child_lastname = fields.Char(related="child_id.lastname", store=True)

    @api.multi
    def uniform_school(self):
        self.reset()

        if self.prestationtime_ids[0].placeid.name == 'AES':
            school_id = self.prestationtime_ids[1].placeid.id
        else:
            school_id = self.prestationtime_ids[0].placeid.id

        for presta in self.prestationtime_ids:
            presta.write({'placeid': school_id})

        self.check()

    @api.multi
    def delete_pod(self):
        for prestation in self.prestationtime_ids:
            if not prestation.invoiced_prestation_id:
                prestation.unlink()
        self.check()

    def merge_duplicate_pod(self):
        cr, uid = self.env.cr, self.env.user.id

        dup_sql = """
                    select min(id) as id
                    from extraschool_prestation_times_of_the_day pod
                    where date_of_the_day > '2016-09-01'
                    group by child_id, date_of_the_day
                    having count(*) > 1
                    """

        self.env.cr.execute(dup_sql, ())
        pod_ids = self.env.cr.dictfetchall()

        pod_ids = self.browse([pod['id'] for pod in pod_ids])

        for pod in pod_ids:
            dup_pod_ids = self.search([('id', '!=', pod.id),
                                       ('child_id.id', '=', pod.child_id.id),
                                       # ('activity_category_id.id', '=', pod.activity_category_id.id),
                                       ('date_of_the_day', '=', pod.date_of_the_day), ])
            for dup_pod in dup_pod_ids:
                dup_pod.prestationtime_ids.unlink()
                for presta in dup_pod.pda_prestationtime_ids:
                    if len(pod.pda_prestationtime_ids.filtered(lambda
                                                                   r: r.es == presta.es and r.placeid == presta.placeid and r.prestation_time == presta.prestation_time)) == 0:
                        presta.prestation_times_of_the_day_id = pod.id
                for pda_unlink in dup_pod.pda_prestationtime_ids:
                    pda_unlink.unlink()

            dup_pod_ids.unlink()
            pod.reset()

    @api.multi
    def reset(self):
        for rec in self:
            rec.place_check = True
            total = len(rec)
            time_list = []
            for presta in rec:
                start_time = time.time()

                if len(time_list) == 50:
                    avg_time = float(sum(time_list) / len(time_list)) * total
                    avg_time = time.strftime('%M:%S', time.gmtime(avg_time))
                    logging.info("Temps estimé restant: {}".format(avg_time))
                    time_list = []
                total -= 1
                invoiced_activity_category = self.get_invoiced_activity_category(rec)
                presta.prestationtime_ids.filtered(lambda r: r.invoiced_prestation_id.id is False).unlink()
                for pda_presta in presta.pda_prestationtime_ids.filtered(
                    lambda r: r.active and r.activitycategoryid.id not in invoiced_activity_category):
                    presta.prestationtime_ids.create({'placeid': pda_presta.placeid.id,
                                                      'childid': pda_presta.childid.id,
                                                      'prestation_date': pda_presta.prestation_date,
                                                      'prestation_time': pda_presta.prestation_time,
                                                      'es': pda_presta.es,
                                                      'activity_category_id': pda_presta.activitycategoryid.id,
                                                      })

                reg_ids = self.env['extraschool.activity_occurrence_child_registration'].search(
                    [('child_id', '=', presta.child_id.id),
                     ('activity_occurrence_id.occurrence_date', '=', presta.date_of_the_day),
                     ('activity_occurrence_id.activity_category_id.id', 'not in', invoiced_activity_category),
                     ])
                for reg in reg_ids:
                    if reg.activity_occurrence_id.activityid.autoaddchilds:
                        reg.activity_occurrence_id.add_presta(reg.activity_occurrence_id, reg.child_id.id, None,
                                                              False)
                presta.verified = False
                presta.checked = False

                time_list.append(time.time() - start_time)

    @api.onchange('prestationtime_ids', 'pda_prestationtime_ids')
    def on_change_prestationtime_ids(self):
        if self.verified:
            self.verified = False

        if self.checked:
            self.checked = False

    def _check_duplicate(self, strict=False):
        prestation_time_ids = [prestation_time.id for prestation_time in self.prestationtime_ids]

        saved_prestation_time = None
        verified = True
        for prestation_time in self.env['extraschool.prestationtimes'].browse(prestation_time_ids):
            if prestation_time.error_msg:
                self.verified = False
                return self
            # check doublon
            if saved_prestation_time == None:
                saved_prestation_time = prestation_time
            else:
                if (
                    prestation_time.activity_occurrence_id == saved_prestation_time.activity_occurrence_id and prestation_time.es == saved_prestation_time.es) \
                    or (prestation_time.es == saved_prestation_time.es and strict == True):
                    prestation_time.error_msg = "Duplicate"
                    saved_prestation_time.error_msg = "Duplicate"
                    saved_prestation_time.verified = False
                    verified = False

        self.verified = verified
        return self

    @api.multi
    def last_check_entry_exit(self):
        """
        This will check one last time if the check has been done right.
        This also check if the activities (from the prestations) have the same prest_to and prest_from.
        If so, it checks if one of those activities has autoaddchilds.
        If so, it will remove the prestations that has the activity without autoaddchilds.
        :return: None
        """
        es = ['E', 'S']
        last_occu = None
        zz = 0
        self.activity_to_delete = 0

        # Get all the activity ID from the prestations.
        activity_range = self.prestationtime_ids.mapped("activity_occurrence_id").mapped("activityid").sorted(
            lambda r: r.prest_to)

        # Compare 2 activities at a time. If they have the same prest_to and prest_from
        # And if one of them has autoaddchilds=True it will delete the prestation from the other activity.
        for i in range(len(activity_range) - 1):
            if activity_range[i].prest_to == activity_range[i + 1].prest_to and activity_range[i].prest_from == \
                activity_range[i + 1].prest_from:
                if activity_range[i].autoaddchilds and not activity_range[i + 1].autoaddchilds:
                    self.activity_to_delete = activity_range[i + 1].id
                elif not activity_range[i].autoaddchilds and activity_range[i + 1].autoaddchilds:
                    self.activity_to_delete = activity_range[i].id

            if not self.activity_to_delete and activity_range[i].leveltype != u'M,P':
                if activity_range[i].leveltype != self.child_id.levelid.leveltype:
                    self.activity_to_delete = activity_range[i].id

            if self.activity_to_delete:
                self.prestationtime_ids.filtered(
                    lambda r: r.activity_occurrence_id.activityid.id == self.activity_to_delete).unlink()

        for presta in self.prestationtime_ids.sorted(
            lambda r: ("%s%s" % (('%.2f' % r.prestation_time).zfill(5), 1 if r.es == 'E' else 0))):
            i = zz % 2
            # check alternate E / S

            if presta.es != es[i]:
                presta.verified = False
                return
            elif presta.activity_occurrence_id:
                presta.verified = True
            else:
                presta.verified = False
                return

            if i and presta.es != 'S' and presta.activity_occurrence_id.id != last_occu:
                presta.verified = False
                return

            zz += 1
            last_occu = presta.activity_occurrence_id.id

    def _add_comment(self, comment, reset=False):
        if (not self.comment) or (not comment in self.comment):
            tmp_comment = self.comment
            if not tmp_comment:
                tmp_comment = ""
            if reset:
                tmp_comment = ""
            tmp_comment = tmp_comment + "\n" if tmp_comment else tmp_comment

            self.comment = tmp_comment + comment

            return self
        else:
            return self

    def _completion_entry(self, root_activity):
        activity_occurrence_obj = self.env['extraschool.activityoccurrence']

        # get presta matching the root_activity
        prestation_times_rs = self.prestationtime_ids.filtered(
            lambda r: r.activity_occurrence_id.activityid.root_id.id == root_activity.id)
        prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
        # check if first presta is an entry
        first_prestation_time = prestation_times_rs[0]
        first_prestation_time.activity_category_id = root_activity.category_id
        if first_prestation_time.es == 'E':
            # correction if default_from_to
            if first_prestation_time.activity_occurrence_id.activityid.default_from_to == 'from_to':
                if first_prestation_time.prestation_time != first_prestation_time.activity_occurrence_id.prest_from:
                    first_prestation_time.prestation_time = first_prestation_time.activity_occurrence_id.prest_from
                else:
                    if first_prestation_time.activity_occurrence_id.activityid.parent_id:
                        occurrence = self.env['extraschool.activityoccurrence'].search([('activityid.id', '=',
                                                                                         first_prestation_time.activity_occurrence_id.activityid.parent_id.id),
                                                                                        ('occurrence_date', '=',
                                                                                         self.date_of_the_day),
                                                                                        ('place_id.id', '=',
                                                                                         first_prestation_time.placeid.id)])
                        if occurrence:
                            res = occurrence.add_presta(occurrence, self.child_id.id, None, True, False, True, False)

                            if res:
                                self._completion_entry(root_activity)

            return first_prestation_time
        else:
            # get the default start
            entry_time = root_activity.get_start(root_activity)
            if entry_time:
                # get the occurrence of the root activity
                occurrence = self.env['extraschool.activityoccurrence'].search(
                    [('activityid.id', '=', root_activity.id),
                     ('occurrence_date', '=', self.date_of_the_day),
                     ('place_id.id', '=', first_prestation_time.placeid.id)])
                # add missing entry presta
                activity_occurrence_obj.add_presta(occurrence, self.child_id.id, None, True, False, True, False)
                # return presta added - the first one in prestationtime_ids
                prestation_times_rs = self.prestationtime_ids.filtered(
                    lambda r: r.activity_occurrence_id.activityid.id == root_activity.id)
                prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
                return prestation_times_rs[0]
            else:
                self._add_comment("Unable to define an entry")
                return False

    def _completion_exit(self, root_activity):
        activity_occurrence_obj = self.env['extraschool.activityoccurrence']

        # get presta matching the root_activity
        prestation_times_rs = self.prestationtime_ids.filtered(
            lambda r: r.activity_occurrence_id.activityid.root_id.id == root_activity.id)
        prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
        # check if last presta is an exit
        last_prestation_time = prestation_times_rs[len(prestation_times_rs) - 1]
        last_prestation_time.activity_category_id = root_activity.category_id
        if last_prestation_time.es == 'S':
            # correction if default_from_to
            if last_prestation_time.activity_occurrence_id.activityid.default_from_to == 'from_to':
                last_prestation_time.prestation_time = last_prestation_time.activity_occurrence_id.prest_to
            return last_prestation_time
        else:
            # get the default stop
            exit_time = root_activity.get_stop(root_activity)
            if exit_time:
                # get the occurrence of the root activity
                occurrence = self.env['extraschool.activityoccurrence'].search(
                    [('activityid.root_id.id', '=', root_activity.id),
                     ('occurrence_date', '=', self.date_of_the_day),
                     ('place_id.id', '=', last_prestation_time.placeid.id)])
                occurrence = occurrence.sorted(key=lambda r: r.prest_to, reverse=True)[0]
                # add missing exit presta
                activity_occurrence_obj.add_presta(occurrence, self.child_id.id, None, True, False, False, True)
                # return presta added
                prestation_times_rs = self.prestationtime_ids.filtered(
                    lambda r: r.activity_occurrence_id.id == occurrence.id)
                prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
                return prestation_times_rs[len(prestation_times_rs) - 1]
            else:
                self._add_comment("Unable to define an entry")
                return False

    def _occu_start_stop_completion(self, start_time, stop_time, occurrence, down, from_occurrence):
        occurrence_obj = self.env['extraschool.activityoccurrence']
        cr, uid = self.env.cr, self.env.user.id

        # init used to avoid adding presta in parent if not needed
        prest_from = -1
        prest_to = -1

        looked_activity = None
        add_prest_to = False
        # if start occurrence than entry is OK so do something ONLY if it's not entry occurrence
        if not start_time.activity_occurrence_id.id == occurrence.id:
            # This is NOT the start occurrence.
            if not down:  # "UP"
                # if we are going up, start is exit of the occurrence that we are coming from
                prest_from = from_occurrence.prest_to
            else:
                prest_from = occurrence.prest_from
            # add entry presta
            occurrence_obj.add_presta(occurrence, self.child_id.id, None, True, False, True, False, prest_from)

        # if stop occurrence than exit is OK so do something ONLY if it's not exit occurrence
        if not stop_time.activity_occurrence_id.id == occurrence.id:
            # This is NOT the exit occurrence.
            if not down:  # "UP"
                # in we are not in the root
                if occurrence.activityid.id != occurrence.activityid.root_id.id:
                    prest_to = occurrence.prest_to
                else:
                    # we are in the root and the exit is in an other occurrence so the exit is the entry of first occurrence in the way to the exit occurrence
                    # go up from exit occurrence until the last occurrence just before the root"
                    looked_activity = stop_time.activity_occurrence_id.activityid.parent_id
                    while looked_activity.parent_id.id != looked_activity.root_id.id:
                        looked_activity = looked_activity.parent_id

                    prest_to = looked_activity.prest_from
            else:
                if occurrence.prest_to <= stop_time.prestation_time:
                    prest_to = occurrence.prest_to
                    add_prest_to = True
                else:
                    prest_to = stop_time.prestation_time

            # add exit presta
            occurrence_obj.add_presta(occurrence, self.child_id.id, None, True, False, False, add_prest_to, None,
                                      prest_to)

        # add parent entry and exit if needed
        if down and occurrence.activityid.id != occurrence.activityid.root_id.id and from_occurrence:  # Down and Not in root
            # if level >=2
            if occurrence.activityid.parent_id and occurrence.activityid.parent_id.id != occurrence.activityid.root_id.id:

                occurrence_obj.add_presta(from_occurrence, self.child_id.id, None, True, False,
                                          True if prest_to > 0 else False, True if prest_from > 0 else False, prest_to,
                                          prest_from)  # from & to are inverted it's normal it's for parent
            else:  # just under the root level 1
                if not looked_activity:
                    looked_activity = stop_time.activity_occurrence_id.activityid.parent_id
                    while looked_activity.parent_id.id != looked_activity.root_id.id:
                        looked_activity = looked_activity.parent_id
                if occurrence.id != looked_activity.id:
                    occurrence_obj.add_presta(from_occurrence, self.child_id.id, None, True, False,
                                              True if prest_to > 0 else False, True if prest_from > 0 else False,
                                              prest_to,
                                              prest_from)  # from & to are inverted it's normal it's for parent

    def _occu_completion(self, start_time, stop_time, occurrence, down, from_occurrence):
        if not occurrence:
            # first call of the fct .... Here we are .... let's go
            down = True
            occurrence = start_time.activity_occurrence_id

        last_occu = False
        self._occu_start_stop_completion(start_time, stop_time, occurrence, down, from_occurrence)

        # compute entry before going down
        if start_time.activity_occurrence_id.id == occurrence.id:
            # "this is the start"
            prest_from = start_time.prestation_time
        else:  #
            if not down:
                # if we are going up, start is exit of the occurrence that we are comming from
                prest_from = from_occurrence.prest_to
            else:
                # to do check if entry presta exist in occurrence, check it with from_to
                #                prest_from = from_occurrence.prest_from
                prest_from = occurrence.prest_from

        # compute exit before going down
        if stop_time.activity_occurrence_id.id == occurrence.id:
            # "this is almost the end, we have reached the last occurrence"
            last_occu = True
            prest_to = stop_time.prestation_time
        else:
            # to do check if EXIT exist in occurrence and check from_to
            # prest_to = stop_time.prestation_time if occurrence.prest_to <= stop_time.prestation_time else occurrence.prest_to
            prest_to = stop_time.prestation_time

        # get child occurrence starting after current occu
        from_occurrence_id = from_occurrence if from_occurrence else None
        if not last_occu:
            child_occurrences = self.env['extraschool.activityoccurrence'].search(
                [('activityid.id', 'in', occurrence.activityid.activity_child_ids.ids),
                 ('activityid.id', '!=', from_occurrence_id.activityid.id if from_occurrence_id else -1),
                 ('occurrence_date', '=', self.date_of_the_day),
                 ('place_id.id', '=', occurrence.place_id.id),
                 ('prest_from', '>=', prest_from),
                 ('prest_from', '<=', prest_to),
                 ])
        else:
            child_occurrences = self.env['extraschool.activityoccurrence'].search(
                [('activityid.id', 'in', occurrence.activityid.activity_child_ids.ids),
                 ('activityid.id', '!=', from_occurrence_id.activityid.id if from_occurrence_id else -1),
                 ('occurrence_date', '=', self.date_of_the_day),
                 ('place_id.id', '=', occurrence.place_id.id),
                 ('prest_from', '>=', prest_from),
                 ('prest_to', '<=', prest_to),
                 ])

        for child_occurrence in child_occurrences:
            if child_occurrence.check_if_child_take_part_to(self.child_id):
                self._occu_completion(start_time, stop_time, child_occurrence, True, occurrence)

        # try to go up
        # if occu is start occu stop
        if occurrence.id == start_time.activity_occurrence_id.id:
            return self
        # if entry and exit is in the current occurrence STOP
        if occurrence.id != start_time.activity_occurrence_id.id or occurrence.id != stop_time.activity_occurrence_id.id:
            if (from_occurrence == None and occurrence.activityid.parent_id) or (
                from_occurrence and occurrence.activityid.parent_id and occurrence.activityid.parent_id.id != from_occurrence.activityid.id):
                from_occurrence_id = from_occurrence.id if from_occurrence else -1
                parent_occurrences = self.env['extraschool.activityoccurrence'].search(
                    [('activityid.id', '=', occurrence.activityid.parent_id.id),
                     ('activityid.id', '!=', from_occurrence_id),
                     ('occurrence_date', '=', self.date_of_the_day),
                     ('place_id.id', '=', occurrence.place_id.id),
                     ])

                self._occu_completion(start_time, stop_time, parent_occurrences, False, occurrence)
        else:
            return self

        return self

    @api.multi
    def check(self):
        if len(self.prestationtime_ids) > 0:
            # match prestation with activity occurrence
            for prestation in self.prestationtime_ids.filtered(lambda r: not r.activity_occurrence_id):
                self.env['extraschool.prestationscheck_wizard']._prestation_activity_occurrence_completion(prestation)
            # use in sql query
            str_prestation_ids = str(self.prestationtime_ids.ids).replace('[', '(').replace(']', ')')
            # Get list of distinct root_id of prestation time for those occurrence activities.
            self.env.cr.execute(
                "SELECT DISTINCT(root_id) "
                "FROM extraschool_prestationtimes ep "
                "LEFT JOIN extraschool_activityoccurrence o "
                "ON ep.activity_occurrence_id = o.id "
                "LEFT JOIN extraschool_activity a "
                "ON o.activityid = a.id "
                "WHERE a.root_id > 0 AND ep.id IN " + str_prestation_ids)

            prestationtimes = self.env.cr.dictfetchall()
            root_ids = [r['root_id'] for r in prestationtimes]
            #
            for root_activity in self.env['extraschool.activity'].browse(root_ids):
                start_time = self._completion_entry(root_activity)
                stop_time = self._completion_exit(root_activity)

                if start_time and stop_time:
                    start_time.verified = True
                    stop_time.verified = True
                    self._occu_completion(start_time, stop_time, None, True, None)
                else:
                    # an error has been found and added to comment field
                    self.verified = False
        else:
            self._add_comment(_("Warning : No presta found"), True)
            self.verified = True

        self.last_check_entry_exit()

        if len(self.prestationtime_ids.filtered(lambda r: r.verified is False).ids) or len(self.prestationtime_ids) % 2:
            self.verified = False
        # Check if the place_ids are correct.
        elif not self.check_place():
            self.verified = False
            self.place_check = False
        else:
            self.verified = True
            self.env.cr.commit()

        return self.verified

    ##############################################################################
    #   Verification that all place ids are the same for the occurrence activity #
    #   https://support.imio.be/browse/AESS-98                                   #
    ##############################################################################
    @api.multi
    def check_place(self):
        # We need to make sure that for every activity occurrence, they have the same schoolimplantation
        activity_occurrence_ids = set(map(self.get_activity_occurrence, self.prestationtime_ids))

        for activity_occurrence in activity_occurrence_ids:
            prestation_ids = self.prestationtime_ids.filtered(
                lambda r: r.activity_occurrence_id.id == activity_occurrence)
            if not self.is_same_place(prestation_ids):
                return False

        return True

    @api.multi
    def is_same_place(self, prestation_ids):
        # If we have less than 1, there has been an error on the verification
        if len(prestation_ids) <= 1:
            return False
        # They don't have the same place id
        elif len(prestation_ids.mapped('placeid')) > 1:
            return False
        else:
            return True

    @api.multi
    def get_activity_occurrence(self, prestation):
        # Return the id of the activity occurrence
        return prestation.activity_occurrence_id.id

    ##############################################################################

    @api.model
    def check_all(self):
        # first set correction for old bug
        # some presta are not verified but invoiced
        # the concerning pod must not be reseted
        # too late
        # so set verified = True
        presta_correction = """
                            update extraschool_prestationtimes p
                            set verified = True
                            from extraschool_prestation_times_of_the_day pod
                            where p.invoiced_prestation_id is not NULL
                            and p.verified = False
                            and p.prestation_times_of_the_day_id = pod.id
                            and pod.verified = True;
                            """
        self.env.cr.execute(presta_correction)

        self.merge_duplicate_pod()
        for presta in self.search([('verified', '=', False), ('checked', '=', False)]):
            presta.check()
            presta.checked = True

    @staticmethod
    def get_prestationtimes_by_activity_category(self, activity_category):
        return self.prestationtime_ids.filtered(lambda r: r.activity_category_id.id == activity_category.id)

    @staticmethod
    def get_invoiced_prestationtimes_by_activity_category(self, activity_category):
        return self.get_prestationtimes_by_activity_category(self, activity_category).filtered(
            lambda r: r.invoiced_prestation_id.id is not False)

    @staticmethod
    def get_invoiced_activity_category(self):
        activities_categories = []
        for activity_category in self.prestationtime_ids.mapped("activity_category_id"):
            if len(self.get_invoiced_prestationtimes_by_activity_category(self, activity_category)) > 0:
                activities_categories.append(activity_category.id)
        return activities_categories


class extraschool_prestation_times_history(models.Model):
    _name = 'extraschool.prestation_times_history'

    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place')
    childid = fields.Many2one('extraschool.child', 'Child')
    parent_id = fields.Many2one(related='childid.parentid')
    prestation_date = fields.Date('Date')
    prestation_time = fields.Float('Time')
    es = fields.Selection((('E', 'In'), ('S', 'Out')), 'es')
    exit_all = fields.Boolean('Exit all', default=False)
    manualy_encoded = fields.Boolean('Manualy encoded')
    verified = fields.Boolean('Verified', default=False)
    error_msg = fields.Char('Error', size=255)
    activity_occurrence_id = fields.Many2one('extraschool.activityoccurrence', 'Activity occurrence')
    activity_name = fields.Char(related='activity_occurrence_id.activityname')
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity Category')
    prestation_times_of_the_day_id = fields.Many2one('extraschool.prestation_times_of_the_day',
                                                     'Prestation of the day')
    invoiced_prestation_id = fields.Many2one('extraschool.invoicedprestations', string='Invoiced prestation')
