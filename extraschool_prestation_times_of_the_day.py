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
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
from datetime import date
import datetime
import time



class extraschool_prestation_times_of_the_day(models.Model):
    _name = 'extraschool.prestation_times_of_the_day'

    _order = 'date_of_the_day desc, child_lastname, child_firstname'

#         _sql_constraints = [
#             ('pod_uniq', 'unique(activity_category_id,date_of_the_day,child_id)', 'Presta of the day must be uniq'),
#             ]

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []

        res=[]
        for presta in self.browse(cr, uid, ids,context=context):
            res.append((presta.id, presta.child_id.name + ' - ' + datetime.datetime.strptime(presta.date_of_the_day, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y")  ))

#        print str(res)

        return res

    # activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=False)
    date_of_the_day = fields.Date(required=True, select=True)
    child_id = fields.Many2one('extraschool.child', required=True, select=True)
    child_firstname = fields.Char(related="child_id.firstname", store=True)
    child_lastname = fields.Char(related="child_id.lastname", store=True)
    child_level= fields.Many2one('extraschool.level', related="child_id.levelid", index=True)
    parent_id = fields.Many2one(related='child_id.parentid', store=True, select=True)
    # place_id = fields.Many2one(related='child_id.schoolimplantation', store=True, select=True)
    prestationtime_ids = fields.One2many('extraschool.prestationtimes','prestation_times_of_the_day_id')
    pda_prestationtime_ids = fields.One2many('extraschool.pdaprestationtimes','prestation_times_of_the_day_id',domain=['|',('active','=',False),('active','=',True)])
    verified = fields.Boolean(select=True)
    comment = fields.Text()
    checked = fields.Boolean(default=False)
    # schoolimplantation = fields.Many2one(related="child_id.schoolimplantation", store=True)

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
        cr,uid = self.env.cr, self.env.user.id

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
                                       ('date_of_the_day', '=', pod.date_of_the_day),])
            for dup_pod in dup_pod_ids:
                dup_pod.prestationtime_ids.unlink()
                for presta in dup_pod.pda_prestationtime_ids:
                    if len(pod.pda_prestationtime_ids.filtered(lambda r: r.es == presta.es and r.placeid == presta.placeid and r.prestation_time == presta.prestation_time)) == 0:
                        presta.prestation_times_of_the_day_id = pod.id
                dup_pod.pda_prestationtime_ids.unlink()

            dup_pod_ids.unlink()
            pod.reset()




    @api.multi
    def reset(self):
        total = len(self)
        time_list = []
        for presta in self:
            start_time = time.time()

            if len(time_list) == 50:
                avg_time = float(sum(time_list) / len(time_list)) * total
                avg_time = time.strftime('%M:%S', time.gmtime(avg_time))
                print "Temps estimé restant: ", avg_time
                time_list = []
            total -= 1
            #Check if presta is not invoiced
            if len(presta.prestationtime_ids.filtered(lambda r: r.invoiced_prestation_id.id is not False).ids) == 0:
                presta.prestationtime_ids.unlink()
                for pda_presta in presta.pda_prestationtime_ids.filtered(lambda r: r.active):
                    # import wdb;wdb.set_trace()
                    presta.prestationtime_ids.create({'placeid': pda_presta.placeid.id,
                                                      'childid': pda_presta.childid.id,
                                                      'prestation_date': pda_presta.prestation_date,
                                                      'prestation_time': pda_presta.prestation_time,
                                                      'es': pda_presta.es,
                                                      'activity_category_id': pda_presta.activitycategoryid.id,
                                                      })

                reg_ids = self.env['extraschool.activity_occurrence_child_registration'].search([('child_id', '=',presta.child_id.id),
                                                                                                 ('activity_occurrence_id.occurrence_date', '=', presta.date_of_the_day),
                                                                                                 # ('activity_occurrence_id.activity_category_id', '=', presta.activity_category_id.id),
                                                                                                 ])
                for reg in reg_ids:
                    if reg.activity_occurrence_id.activityid.autoaddchilds:
                        reg.activity_occurrence_id.add_presta(reg.activity_occurrence_id, reg.child_id.id, None,False)
                presta.verified = False
                presta.checked = False

            time_list.append(time.time() - start_time)

    @api.onchange('prestationtime_ids', 'pda_prestationtime_ids')
    def on_change_prestationtime_ids(self):
        if self.verified:
            self.verified = False

        if self.checked:
            self.checked = False

    def _check_duplicate(self,strict=False):
        prestation_time_ids = [prestation_time.id for prestation_time in self.prestationtime_ids]

        saved_prestation_time = None
        verified = True
        for prestation_time in self.env['extraschool.prestationtimes'].browse(prestation_time_ids):
            if prestation_time.error_msg:
                self.verified = False
                return self
            #check doublon
            if saved_prestation_time == None:
                saved_prestation_time = prestation_time
            else:
                if (prestation_time.activity_occurrence_id == saved_prestation_time.activity_occurrence_id and prestation_time.es == saved_prestation_time.es) \
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
        zz=0
        activity_ids = []
        self.activity_to_delete = 0

        # Get all the activity ID from the prestations.
        for presta in self.prestationtime_ids.sorted(key=lambda r: (r.prestation_time)):
            if presta.activity_occurrence_id.activityid.id not in activity_ids:
                activity_ids.append(presta.activity_occurrence_id.activityid.id)

        # Get the activity object sorted by prest_to for better search.
        activity_range = self.env['extraschool.activity'].search([('id', 'in', activity_ids)]).sorted(key=lambda r: (r.prest_to))

        # Compare 2 activities at a time. If they have the same prest_to and prest_from
        # And if one of them has autoaddchilds=True it will delete the prestation from the other activity.
        for i in range(len(activity_range)-1):
            if activity_range[i].prest_to == activity_range[i+1].prest_to and activity_range[i].prest_from == activity_range[i+1].prest_from:
                if activity_range[i].autoaddchilds and not activity_range[i+1].autoaddchilds:
                    self.activity_to_delete = activity_range[i+1].id
                elif not activity_range[i].autoaddchilds and activity_range[i+1].autoaddchilds:
                    self.activity_to_delete = activity_range[i].id

            if not self.activity_to_delete and activity_range[i].leveltype != u'M,P':
                if activity_range[i].leveltype != self.child_id.levelid.leveltype:
                    self.activity_to_delete = activity_range[i].id

            if self.activity_to_delete:
                self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.id == self.activity_to_delete).unlink()

        for presta in self.prestationtime_ids.sorted(key=lambda r: ("%s%s" % (('%.2f' % (r.prestation_time)).zfill(5), 1 if r.es == 'E' else 0))):
            # print "presta : %s %s %s" % (presta.activity_occurrence_id.id, presta.activity_occurrence_id.name, ('%.2f' % (presta.prestation_time)).zfill(5))
            i = zz % 2
            #check alternate E / S

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

    def _add_comment(self,comment,reset=False):
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

    def _completion_entry(self,root_activity):
#        print "_completion_entry : %s" % (root_activity)

        activity_occurrence_obj = self.env['extraschool.activityoccurrence']

        #get presta matching the root_activity
        prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.root_id.id == root_activity.id)
        prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
        #check if first presta is an entry
        first_prestation_time = prestation_times_rs[0]
        first_prestation_time.activity_category_id = root_activity.category_id
        if first_prestation_time.es == 'E':
            #correction if default_from_to
            if first_prestation_time.activity_occurrence_id.activityid.default_from_to == 'from_to':
                if first_prestation_time.prestation_time != first_prestation_time.activity_occurrence_id.prest_from:
                    first_prestation_time.prestation_time = first_prestation_time.activity_occurrence_id.prest_from
                else:
                    if first_prestation_time.activity_occurrence_id.activityid.parent_id:
                        occurrence = self.env['extraschool.activityoccurrence'].search([('activityid.id', '=',first_prestation_time.activity_occurrence_id.activityid.parent_id.id),
                                                                                    ('occurrence_date', '=', self.date_of_the_day),
                                                                                    ('place_id.id', '=', first_prestation_time.placeid.id)])
                        if occurrence:
                            res = occurrence.add_presta(occurrence, self.child_id.id, None,True,False,True,False)

                            if res:
                                self._completion_entry(root_activity)


            return first_prestation_time
        else:
            #get the default start
            entry_time = root_activity.get_start(root_activity)
            if entry_time:
                #get the occurrence of the root activity
                occurrence = self.env['extraschool.activityoccurrence'].search([('activityid.id', '=',root_activity.id),
                                                                                ('occurrence_date', '=', self.date_of_the_day),
                                                                                ('place_id.id', '=', first_prestation_time.placeid.id)])
                #add missing entry presta
                activity_occurrence_obj.add_presta(occurrence, self.child_id.id, None,True,False,True,False)
                #return presta added - the first one in prestationtime_ids
                prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.id == root_activity.id)
                prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
                return prestation_times_rs[0]
            else:
                self._add_comment("Unable to define an entry")
                return False

    def _completion_exit(self,root_activity):
#        print "_completion_exit : %s" % (root_activity)
        activity_occurrence_obj = self.env['extraschool.activityoccurrence']

        #get presta matching the root_activity
        prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.activityid.root_id.id == root_activity.id)
        prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
        #check if last presta is an exit
        last_prestation_time = prestation_times_rs[len(prestation_times_rs)-1]
        last_prestation_time.activity_category_id = root_activity.category_id
        if last_prestation_time.es == 'S':
            #correction if default_from_to
            if last_prestation_time.activity_occurrence_id.activityid.default_from_to == 'from_to':
                last_prestation_time.prestation_time = last_prestation_time.activity_occurrence_id.prest_to

#            print "exit : %s" % (last_prestation_time.prestation_time)
            return last_prestation_time
        else:
            #get the default stop
            exit_time = root_activity.get_stop(root_activity)
            if exit_time:
                #get the occurrence of the root activity
                occurrence = self.env['extraschool.activityoccurrence'].search([('activityid.root_id.id', '=',root_activity.id),
                                                                                ('occurrence_date', '=', self.date_of_the_day),
                                                                                ('place_id.id', '=', last_prestation_time.placeid.id)])
                occurrence = occurrence.sorted(key=lambda r: r.prest_to, reverse = True)[0]
                #add missing exit presta
                activity_occurrence_obj.add_presta(occurrence, self.child_id.id, None,True,False,False,True)
                #return presta added
                prestation_times_rs = self.prestationtime_ids.filtered(lambda r: r.activity_occurrence_id.id == occurrence.id)
                prestation_times_rs = prestation_times_rs.sorted(key=lambda r: r.prestation_time)
                return prestation_times_rs[len(prestation_times_rs)-1]
            else:
                self._add_comment("Unable to define an entry")
                return False


    def _occu_start_stop_completion(self,start_time,stop_time,occurrence,down,from_occurrence):
#         print "->_occu_start_stop_completion"
#         print "%s" % (occurrence.activityname)

        occurrence_obj = self.env['extraschool.activityoccurrence']
        cr,uid = self.env.cr, self.env.user.id

        #init used to avoid adding presta in parent if not needed
        prest_from = -1
        prest_to = -1

        looked_activity = None
        add_prest_to = False
        #if start occurrence than entry is OK so do something ONLY if it's not entry occurrence
        if not start_time.activity_occurrence_id.id == occurrence.id:
            # This is NOT the start occurrence.
            if not down: #"UP"
                #if we are going up, start is exit of the occurrence that we are coming from
                prest_from = from_occurrence.prest_to
            else:
                prest_from = occurrence.prest_from
            #add entry presta
            occurrence_obj.add_presta(occurrence,self.child_id.id,None, True, False, True, False,prest_from)

        #if stop occurrence than exit is OK so do something ONLY if it's not exit occurrence
        if not stop_time.activity_occurrence_id.id == occurrence.id:
            # This is NOT the exit occurrence.
            if not down: #"UP"
                #in we are not in the root
                if occurrence.activityid.id != occurrence.activityid.root_id.id:
                    prest_to = occurrence.prest_to
                else:
                    #we are in the root and the exit is in an other occurrence so the exit is the entry of first occurrence in the way to the exit occurrence
                    #go up from exit occurrence until the last occurrence just before the root"
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

            #add exit presta
            occurrence_obj.add_presta(occurrence,self.child_id.id,None, True, False, False, add_prest_to, None, prest_to)


        #add parent entry and exit if needed
        if down and occurrence.activityid.id != occurrence.activityid.root_id.id and from_occurrence: #Down and Not in root
            #if level >=2
            if occurrence.activityid.parent_id and occurrence.activityid.parent_id.id != occurrence.activityid.root_id.id:

                occurrence_obj.add_presta(from_occurrence,self.child_id.id,None, True, False, True if prest_to > 0 else False, True if prest_from > 0 else False,prest_to,prest_from) #from & to are inverted it's normal it's for parent
            else: #just under the root level 1
                if not looked_activity:
                    looked_activity = stop_time.activity_occurrence_id.activityid.parent_id
                    while looked_activity.parent_id.id != looked_activity.root_id.id:
                        # print looked_activity.parent_id.id , looked_activity.root_id.id
                        looked_activity = looked_activity.parent_id
                if occurrence.id !=looked_activity.id:
                    occurrence_obj.add_presta(from_occurrence,self.child_id.id,None, True, False, True if prest_to > 0 else False, True if prest_from > 0 else False,prest_to,prest_from) #from & to are inverted it's normal it's for parent

#        print "<-_occu_start_stop_completion"


    def _occu_completion(self,start_time,stop_time,occurrence,down,from_occurrence):
#        print "_occu_completion : %s" % ("start" if not occurrence else occurrence.name)
        if not occurrence:
            #first call of the fct .... Here we are .... let's go
            down = True
            occurrence = start_time.activity_occurrence_id

        last_occu = False
        self._occu_start_stop_completion(start_time,stop_time,occurrence,down,from_occurrence)

        #compute entry before going down
        if start_time.activity_occurrence_id.id == occurrence.id:
            #"this is the start"
            prest_from = start_time.prestation_time
        else:#
            if not down:
                #if we are going up, start is exit of the occurrence that we are comming from
                prest_from = from_occurrence.prest_to
            else:
                #to do check if entry presta exist in occurrence, check it with from_to
#                prest_from = from_occurrence.prest_from
                prest_from = occurrence.prest_from

        #compute exit before going down
        if stop_time.activity_occurrence_id.id == occurrence.id:
            #"this is almost the end, we have reached the last occurrence"
            last_occu = True
            prest_to = stop_time.prestation_time
        else:
            #to do check if EXIT exist in occurrence and check from_to
            # prest_to = stop_time.prestation_time if occurrence.prest_to <= stop_time.prestation_time else occurrence.prest_to
            prest_to = stop_time.prestation_time


        #get child occurrence starting after current occu
        from_occurrence_id = from_occurrence if from_occurrence else None
        if not last_occu:
            child_occurrences = self.env['extraschool.activityoccurrence'].search([('activityid.id', 'in',occurrence.activityid.activity_child_ids.ids),
                                                                                   ('activityid.id', '!=',from_occurrence_id.activityid.id if from_occurrence_id else -1),
                                                                                ('occurrence_date', '=', self.date_of_the_day),
                                                                                ('place_id.id', '=', occurrence.place_id.id),
                                                                                ('prest_from', '>=', prest_from),
                                                                                ('prest_from', '<=', prest_to),
                                                                                   ])
        else:
            child_occurrences = self.env['extraschool.activityoccurrence'].search([('activityid.id', 'in',occurrence.activityid.activity_child_ids.ids),
                                                                                   ('activityid.id', '!=',from_occurrence_id.activityid.id if from_occurrence_id else -1),
                                                                                ('occurrence_date', '=', self.date_of_the_day),
                                                                                ('place_id.id', '=', occurrence.place_id.id),
                                                                                ('prest_from', '>=', prest_from),
                                                                                ('prest_to', '<=', prest_to),
                                                                                ])
#         print "prest from : %s prest to : %s" % (prest_from,prest_to)
#         print "occu child_ids of occurrence %s : %s" % (occurrence.name,child_occurrences.ids)
        for child_occurrence in child_occurrences:
            if child_occurrence.check_if_child_take_part_to(self.child_id):
                self._occu_completion(start_time,stop_time,child_occurrence,True,occurrence)

        # try to go up
        #if occu is start occu stop
        if occurrence.id == start_time.activity_occurrence_id.id:
            return self
        # if entry and exit is in the current occurrence STOP
        if occurrence.id != start_time.activity_occurrence_id.id or occurrence.id != stop_time.activity_occurrence_id.id:
            if (from_occurrence == None and occurrence.activityid.parent_id) or (from_occurrence and occurrence.activityid.parent_id and occurrence.activityid.parent_id.id != from_occurrence.activityid.id):
                from_occurrence_id = from_occurrence.id if from_occurrence else -1
                parent_occurrences = self.env['extraschool.activityoccurrence'].search([('activityid.id', '=',occurrence.activityid.parent_id.id),
                                                                                   ('activityid.id', '!=',from_occurrence_id),
                                                                                ('occurrence_date', '=', self.date_of_the_day),
                                                                                ('place_id.id', '=', occurrence.place_id.id),
                                                                                ])

                self._occu_completion(start_time,stop_time,parent_occurrences,False,occurrence)
        else:
            return self

        return self

    @api.multi
    def check(self):
        print "Checking......."
        #Check if presta is not invoiced
        if len(self.prestationtime_ids.filtered(lambda r: r.invoiced_prestation_id.id is not False).ids) == 0:
            #if no presta than warning and exit
            if not self.prestationtime_ids:
                self._add_comment(_("Warning : No presta found"),True)
                self.verified = True
                return True

            #
            str_prestation_ids = str(self.prestationtime_ids.ids).replace('[','(').replace(']',')')
            for prestation in self.prestationtime_ids.filtered(lambda r: not r.activity_occurrence_id):
#                print "add activity occurrence id "
                self.env['extraschool.prestationscheck_wizard']._prestation_activity_occurrence_completion(prestation)
#            print "str_prestation_ids %s" % str_prestation_ids
            # Get list of distinct root_id of prestation time for those occurrence activities.
            self.env.cr.execute(
                "select distinct(root_id) from extraschool_prestationtimes ep left join extraschool_activityoccurrence o on ep.activity_occurrence_id = o.id left join extraschool_activity a on o.activityid = a.id where a.root_id > 0 and ep.id in " + str_prestation_ids)

            prestationtimes = self.env.cr.dictfetchall()
            root_ids = [r['root_id'] for r in prestationtimes]

#            print "root_ids : %s" % (root_ids)
            for root_activity in self.env['extraschool.activity'].browse(root_ids):
                #print "checking root : %s" % (root_activity.name)
                start_time = self._completion_entry(root_activity)
                stop_time = self._completion_exit(root_activity)

                if start_time and stop_time:
                    start_time.verified = True
                    stop_time.verified = True
                    self._occu_completion(start_time,stop_time,None,True,None)
                else:
                    #an error has been found and added to comment field
                    self.verified = False

        # print self.verified

        self.last_check_entry_exit()

        if len(self.prestationtime_ids.filtered(lambda r: r.verified is False).ids) or len(self.prestationtime_ids) % 2:
            self.verified = False
        else:
            self.verified = True
            self.env.cr.commit()

        return self.verified

    @api.model
    def check_all(self):
#         print "--------------"
#         print "check all"
#         print "--------------"

        #first set correction for old bug
        #some presta are not verified but invoiced
        #the concerning pod must not be reseted
        #too late
        #so set verified = True
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

class extraschool_prestation_times_history(models.Model):
    _name = 'extraschool.prestation_times_history'

    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place')
    childid = fields.Many2one('extraschool.child', 'Child')
    parent_id = fields.Many2one(related='childid.parentid')
    prestation_date = fields.Date('Date')
    prestation_time = fields.Float('Time')
    es = fields.Selection((('E','In'), ('S','Out')),'es')
    exit_all = fields.Boolean('Exit all',default=False)
    manualy_encoded = fields.Boolean('Manualy encoded')
    verified = fields.Boolean('Verified',default=False)
    error_msg = fields.Char('Error', size=255)
    activity_occurrence_id = fields.Many2one('extraschool.activityoccurrence', 'Activity occurrence')
    activity_name = fields.Char(related='activity_occurrence_id.activityname')
    activity_category_id = fields.Many2one('extraschool.activitycategory', 'Activity Category')
    prestation_times_of_the_day_id = fields.Many2one('extraschool.prestation_times_of_the_day', 'Prestation of the day')
    invoiced_prestation_id = fields.Many2one('extraschool.invoicedprestations', string='Invoiced prestation')








