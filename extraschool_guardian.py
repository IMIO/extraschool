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
from datetime import date, datetime
import time

class extraschool_guardian(models.Model):
    _name = 'extraschool.guardian'
    _description = 'Guardian'
    
    name = fields.Char(compute='_name_compute',string='FullName', size=100, store=True)
    firstname = fields.Char('FirstName', size=50)
    lastname = fields.Char('LastName', size=50 , required=True)
    tagid = fields.Char('Tag ID', size=50)
    otherref = fields.Char('Other ref')
    weekly_schedule = fields.Float('Horaire hebdomadaire')
    oldid = fields.Integer('oldid')
    isdisabled = fields.Boolean('Disabled',default=False, track_visibility='onchange')

    @api.depends('firstname','lastname')
    def _name_compute(self):
        for record in self:
            record.name = '%s %s'  % (record.lastname, record.firstname)

    @api.one
    def unlink(self):
        self.isdisabled = True

    @api.one    
    def action_gentagid(self):   
        if not self.tagid :
            config = self.env['extraschool.mainsettings'].browse([1])
            self.tagid = config.lastqrcodenbr = config.lastqrcodenbr + 1
        
        return self.tagid
        # return long(self.tagid)

    @api.one    
    def get_qr_logo(self):   
        config = self.env['extraschool.mainsettings'].browse([1])
        logo = config.logo
        
        return logo

##############################################################################
#
#    AESMobile
#    Copyright (C) 2018
#    Colicchia Michaël & Delaere Olivier - Imio (<http://www.imio.be>).
#
##############################################################################

    @api.multi
    def get_guardian_for_smartphone(self, smartphone_id):

        start_time = time.time()

        cr = self.env.cr

        sql_query = """
                    SELECT id, lastname, firstname, tagid
                    FROM extraschool_guardian
                    WHERE isdisabled IS NOT True OR isdisabled IS NULL;
                    """

        cr.execute(sql_query)
        guardian_info = cr.dictfetchall()

        for guardian in guardian_info:
            if guardian['tagid'] == None:
                guardian['tagid'] = ''

        try:
            self.env['extraschool.smartphone_log'].create({ 'title': 'Fetching guardians',
                                                            'time_of_transmission': time.time() - start_time,
                                                            'smartphone_id': smartphone_id,
                                                            })
        except:
            print "Error Guardian"
            return "Error Sync on Guardians"

        return guardian_info



    @staticmethod
    def get_guardian(cr, uid, smartphone_id, context=None):
        # Declare new Environment.
        env = api.Environment(cr, uid, context={})

        # Log des transmissions des smartphones
        # Dictionnaire des enfants {id: , nom: , prenom:, tagid:}

        return extraschool_guardian.get_guardian_for_smartphone(env['extraschool.guardian'], smartphone_id)
