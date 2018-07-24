# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2014
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

class extraschool_organising_power(models.Model):
    _name = 'extraschool.organising_power'
    _description = 'Organising Power that contains all activities'

    activity_category_ids = fields.One2many('extraschool.activitycategory', 'organising_power_id', 'Activity Category')
    town = fields.Char('Name of the town', required=True)
    childpositiondetermination = fields.Selection((('byparent','by parent'),
                                                   ('byparentwp','by parent (only childs with prestations)'),
                                                   ('byparent_nb_childs','by parent (position replaced by nbr childs'),
                                                   ('byparent_nb_childs_wp','by parent (position replaced by nbr childs with prestations'),
                                                   ('byaddress','by address'),
                                                   ('byaddresswp','by address (only childs with prestations)'),
                                                   ('byaddress_nb_childs','by address (position replaced by nbr childs'),
                                                   ('byaddress_nb_childs_wp','by address (position replaced by nbr childs with prestations'),
                                                   ),'Child position determination', required = True)
