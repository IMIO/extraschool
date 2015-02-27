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


class extraschool_prestation_times_manuel(models.Model):
    _name = 'extraschool.prestation_times_manuel'

    child_id = fields.Many2one('extraschool.child', required=True)
    prestation_times_encodage_manuel_id = fields.Many2one('extraschool.prestation_times_encodage_manuel', 'encodage manuel')
    prestation_time_entry = fields.Float('Entry Time')
    prestation_time_exit = fields.Float('Exit Time')                
    comment = fields.Text()

extraschool_prestation_times_manuel()   
