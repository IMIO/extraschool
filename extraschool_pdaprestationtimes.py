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
import time

class extraschool_pdaprestationtimes(models.Model):
    _name = 'extraschool.pdaprestationtimes'
    _description = 'PDA Prestation Times'

    def _get_activity_category_id(self):
        return self.env['extraschool.activitycategory'].search([]).filtered('id').id

    placeid = fields.Many2one('extraschool.place', 'Schoolcare Place', required=True)
    activitycategoryid = fields.Many2one('extraschool.activitycategory', 'Activity Category', required=False, default=_get_activity_category_id)
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
    def create(self,vals):
        if len(self.env['extraschool.child'].search([('id', '=',vals['childid']),])) == 0:
            #child deleted ...
            print "warning pda_presta of child deleted !!"
            return self

        if 'type' not in vals:
            vals['type'] = 'pda'

        vals['prestation_time'] = '%.6f' % round(vals['prestation_time'], 6)

        search_domain = [   ('activitycategoryid', '=', vals['activitycategoryid']),
                            ('childid.id', '=', vals['childid']),
                            ('placeid.id', '=', vals['placeid']),
                            ('prestation_date', '=', vals['prestation_date']),
                            ('prestation_time', '=', vals['prestation_time']),
                            ('type', '=', vals['type']),
                            ('es', '=', vals['es']),
                            ]

        print "search_domain : %s" % (search_domain)
        presta = self.search(search_domain)
        # if the same presta already exist than exit
        print "len(presta) %s" % (len(presta))
        if len(presta):
            print "presta already exist"
            return presta[0]

        prestation_times_of_the_day_obj = self.env['extraschool.prestation_times_of_the_day']
        prestation_times_obj = self.env['extraschool.prestationtimes']

        prestation_times_of_the_day_ids = prestation_times_of_the_day_obj.search([('activity_category_id.id', '=', vals['activitycategoryid']),
                                                                                  ('child_id.id', '=', vals['childid']),
                                                                                  ('date_of_the_day', '=', vals['prestation_date']),
                                                                                  ])
        if not prestation_times_of_the_day_ids:
            print "pod doesn't exist"
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_obj.create({'activity_category_id' : vals['activitycategoryid'],
                                                                                             'child_id' : vals['childid'],
                                                                                             'date_of_the_day' : vals['prestation_date'],
                                                                                             }).id
        else :
            print "presta of day already exist"
            vals['prestation_times_of_the_day_id'] = prestation_times_of_the_day_ids[0].id

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
    def import_prestations(self, dict_prestations, smartphone_id=16):
        activity_category = self.env['extraschool.activitycategory'].search([]).filtered('id').id
        actual_prestations = 0
        start_time = time.time()

        for prestation in dict_prestations:
            if prestation['type'] == 1:
                self.env['extraschool.guardianprestationtimes'].create({'guardianid': prestation['childid'],
                                                                        'prestation_date': prestation['prestation_date'],
                                                                        'prestation_time': prestation['prestation_time'],
                                                                        'es': prestation['es'],
                                                                        'manualy_encoded': False,
                                                                        })
                actual_prestations += 1
            else:
                self.create({   'childid': prestation['childid'],
                                'placeid': prestation['placeid'],
                                'prestation_date': prestation['prestation_date'],
                                'prestation_time': prestation['prestation_time'],
                                'es': prestation['es'],
                                'activitycategoryid': activity_category,
                                })
                actual_prestations += 1

        if len(dict_prestations) == actual_prestations:
            self.env['extraschool.smartphone_log'].create({'title': 'Successfully imported data',
                                                           'time_of_transmission': time.time() - start_time,
                                                           'smartphone_id': smartphone_id,
                                                           })
            return "Data successfully send."
        else:
            self.env['extraschool.smartphone_log'].create({'title': 'WARNING ! Error while sending data',
                                                           'time_of_transmission': time.time() - start_time,
                                                           'smartphone_id': smartphone_id,
                                                           })
            return "There has been an error, please contact your supervisor."

    @staticmethod
    def get_guardian(cr, uid, dict_prestations, context=None):
        # Declare new Environment.
        env = api.Environment(cr, uid, context={})

        # Log des transmissions des smartphones
        # Dictionnaire des enfants {id: , nom: , prenom:, tagid:}

        return extraschool_pdaprestationtimes.import_prestations(env['extraschool.pdaprestationtimes'], dict_prestations)