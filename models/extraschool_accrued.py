# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
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

from odoo import models, api, fields, _
from odoo.api import Environment
from odoo.exceptions import except_orm, Warning
from odoo.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)

from odoo.tools.misc import profile
from datetime import date, datetime, timedelta as td
import time
import pdb
from odoo.exceptions import except_orm, Warning, RedirectWarning


class extraschoolAccrued(models.Model):
    _name = 'extraschool.accrued'
    _description = 'Droit constatés'

    biller_id = fields.Many2one('extraschool.biller')
    activity_category_id = fields.Many2one('extraschool.activitycategory')
    amount = fields.Float()
    ref = fields.Char()
