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
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
from datetime import date
import datetime


class extraschool_prestation_times_encodage_manuel(models.Model):
    _name = 'extraschool.prestation_times_encodage_manuel'

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        
        res=[]
        for presta in self.browse(cr, uid, ids,context=context):
            res.append((presta.id, presta.place_id.name + ' - ' + datetime.datetime.strptime(presta.date_of_the_day, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y")  ))    
    
        print str(res)

        return res      
     
    date_of_the_day = fields.Date(required=True)    
    place_id = fields.Many2one('extraschool.place', required=True)                    
    prestationtime_ids = fields.One2many('extraschool.prestation_times_manuel','prestation_times_encodage_manuel_id')    
    comment = fields.Text()

extraschool_prestation_times_encodage_manuel()   
