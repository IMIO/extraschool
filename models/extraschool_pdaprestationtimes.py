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
from openerp import models, api, fields, _
from openerp.exceptions import Warning
from openerp.api import Environment
from openerp.exceptions import Warning
import datetime
import time
import logging

_logger = logging.getLogger(__name__)

class extraschool_pdaprestationtimes(models.Model):
    _name = 'extraschool.pdaprestationtimes'
    _description = 'PDA Prestation Times'

    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place', required=True)
    activitycategoryid = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=False)
    childid = fields.Many2one('extraschool.child', 'Child', required=False)
    prestation_date = fields.Date('Date')
    prestation_time = fields.Float('Time')
    type = fields.Selection((('pda','Smartphone'),
                             ('manuel','Encodage manuel')),'Type', default='pda' )
    prestation_times_encodage_manuel_id = fields.Many2one('extraschool.prestation_times_encodage_manuel', 'Encodage Manuel',ondelete='cascade')
    es = fields.Selection((('E','In'),
                           ('S','Out')),'ES' )
    prestation_times_of_the_day_id = fields.Many2one('extraschool.prestation_times_of_the_day', 'Prestation of the day',ondelete='cascade')
    pda_transmission_id = fields.Many2one('extraschool.pda_transmission', 'Transmission')
    active = fields.Boolean('active', default=True)

    @api.multi
    def desactive(self):
        if not self.active:
            self.active = True
        else:
            self.active = False

        self.prestation_times_of_the_day_id.reset()
        self.prestation_times_of_the_day_id.check()

    @api.model
    def unlink(self):
        prestation_times_ids = self.prestation_times_of_the_day_id.prestationtime_ids
        for prestation_times_id in prestation_times_ids:
            if prestation_times_id.invoiced_prestation_id:
                raise Warning(_("At least one registration line is already invoiced !"))

        return super(extraschool_pdaprestationtimes, self).unlink()

    @api.model
    def create(self,vals):
        if len(self.env['extraschool.child'].search([('id', '=',vals['childid']),])) == 0:
            return self

        if 'type' not in vals:
            vals['type'] = 'pda'

        vals['prestation_time'] = '%.6f' % round(vals['prestation_time'], 6)

        search_domain = [   ('childid.id', '=', vals['childid']),
                            ('placeid.id', '=', vals['placeid']),
                            ('prestation_date', '=', vals['prestation_date']),
                            ('prestation_time', '=', vals['prestation_time']),
                            ('type', '=', vals['type']),
                            ('es', '=', vals['es']),
                            ]

        presta = self.search(search_domain)

        # if the same presta already exist than exit
        if len(presta):
            return presta[0]

        prestation_times_of_the_day_obj = self.env['extraschool.prestation_times_of_the_day']
        prestation_times_obj = self.env['extraschool.prestationtimes']

        prestation_times_of_the_day_ids = prestation_times_of_the_day_obj.search([
                                                                                  ('child_id.id', '=', vals['childid']),
                                                                                  ('date_of_the_day', '=', vals['prestation_date']),
                                                                                  ])

        if not prestation_times_of_the_day_ids:
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_obj.create({
                # 'activity_category_id' : vals['activitycategoryid'],
                                                                                             'child_id' : vals['childid'],
                                                                                             'date_of_the_day' : vals['prestation_date'],
                                                                                             }).id
        else:
            # Prestation of the day already exist.
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_ids[0].id
            prestation_times_of_the_day_ids[0].checked = False
            prestation_times_of_the_day_ids[0].verified = False

        prestation_times_obj.create({'prestation_times_of_the_day_id': vals['prestation_times_of_the_day_id'],
                                     'activity_category_id': vals['activitycategoryid'],
                                     'childid': vals['childid'],
                                     'placeid': vals['placeid'],
                                     'prestation_date': vals['prestation_date'],
                                     'prestation_time': vals['prestation_time'],
                                     'type': vals['type'],
                                     'es': vals['es'],
                                     })

        return super(extraschool_pdaprestationtimes, self).create(vals)

##############################################################################
#
#    AESMobile
#    Copyright (C) 2018
#    Colicchia Michaël & Delaere Olivier - Imio (<http://www.imio.be>).
#
##############################################################################

    @api.multi
    def import_prestations(self, dict_prestations, smartphone_id):
        place_id = self.env['extraschool.smartphone'].search([('id', '=', smartphone_id)]).placeid.id
        start_time = time.time()

        # Updating Tag ID of children
        try:
            for new_tag in dict_prestations['newTag']:
                self.env['extraschool.child'].search([('id', '=', new_tag['pk'])]).write({'tagid': new_tag['tagId']})

            self.env['extraschool.smartphone_log'].create({'title': 'Successfully updated children new tag Id',
                                                           'time_of_transmission': time.time() - start_time,
                                                           'smartphone_id': smartphone_id,
                                                           })

        except:

            self.env['extraschool.smartphone_log'].create({'title': 'WARNING ! Error while updating children new tag Id',
                                                           'time_of_transmission': time.time() - start_time,
                                                           'smartphone_id': smartphone_id,
                                                           })

            return False

        # Importing prestation for children
        try:
            pda_transmission_id = self.env['extraschool.pda_transmission'].create({
                'transmission_date_from': datetime.datetime.now(),
                'smartphone_id': smartphone_id,
            })

            for children in dict_prestations['children']:
                child_level = self.env['extraschool.child'].search([('id', '=', children['pk'])]).levelid.leveltype

                # Xml RPC datetime to python datetime
                datechild = datetime.datetime.strptime(str(children['date']), '%Y%m%dT%H%M%S')

                # Convert time to float
                prestation_time = datechild.hour + datechild.minute / 60.0

                # Get the category activity id if possible.
                activity_occurrence_ids = self.env['extraschool.activityoccurrence'].search(
                    [('occurrence_date', '=', datechild.date()), ('prest_from', '<=', prestation_time),
                     ('prest_to', '>=', prestation_time), ('place_id', '=', place_id)])

                if len(activity_occurrence_ids) != 1:
                    for activity_occurrence in activity_occurrence_ids:
                        if activity_occurrence.activityid.leveltype == child_level or activity_occurrence.activityid.leveltype == u'M,P':
                            activity_category_id = activity_occurrence.activity_category_id

                if len(activity_occurrence_ids) == 1:
                    activity_category_id = activity_occurrence_ids.activity_category_id

                if len(activity_occurrence_ids) == 0:
                    activity_category_id = self.env['extraschool.activitycategory'].search([])[0]

                self.create({   'childid': children['pk'],
                                'placeid': place_id,
                                'prestation_date': datechild.date(),
                                'prestation_time': prestation_time,
                                'es': children['eventType'],
                                'activitycategoryid': activity_category_id.id,
                                'pda_transmission_id': pda_transmission_id.id,
                            })

            self.env['extraschool.smartphone_log'].create({'title': 'Successfully imported children prestation',
                                                           'time_of_transmission': time.time() - start_time,
                                                           'smartphone_id': smartphone_id,
                                                           })

        except:
            self.env['extraschool.smartphone_log'].create({'title': 'WARNING ! Error while receiving children prestation data',
                                                           'time_of_transmission': time.time() - start_time,
                                                           'smartphone_id': smartphone_id,
                                                           })

            return False

        #Importing prestation for guardians
        try:
            for sitters in dict_prestations['sitters']:
                # Xml RPC datetime to python datetime
                datesitter = datetime.datetime.strptime(str(sitters['date']), '%Y%m%dT%H%M%S')

                #  Convert time to float
                prestation_time = datesitter.hour + datesitter.minute / 60.0

                self.env['extraschool.guardianprestationtimes'].create({   'guardianid': sitters['pk'],
                                                                            'prestation_date': datesitter.date(),
                                                                            'prestation_time': prestation_time,
                                                                            'es': sitters['eventType'],
                                                                            # 'activitycategoryid': activity_category_id,
                                                                            'manualy_encoded': False,
                                                                            })

        except:
            self.env['extraschool.smartphone_log'].create({'title': 'WARNING ! Error while receiving guardians prestation data',
                                                           'time_of_transmission': time.time() - start_time,
                                                           'smartphone_id': smartphone_id,
                                                           })

            return False

        return True

    @staticmethod
    def send_data(cr, uid, dict_prestations, smartphone_id, context=None):
        # Declare new Environment.
        env = api.Environment(cr, uid, context={})

        return extraschool_pdaprestationtimes.import_prestations(env['extraschool.pdaprestationtimes'], dict_prestations, smartphone_id)