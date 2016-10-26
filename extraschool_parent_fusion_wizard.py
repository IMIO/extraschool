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
import lbutils
from openerp.exceptions import except_orm, Warning, RedirectWarning

class extraschool_parent_fusion_wizard(models.TransientModel):
    _name = 'extraschool.parent_fusion_wizard'
    _description = 'Parent fusion wizard'
    
    parent_id = fields.Many2one('extraschool.parent', 'Parent')
    parent_ids = fields.Many2many('extraschool.parent','extraschool_parent_fusion_rel', 'parent_fusion_id', 'parent_id','Parent_fusion')
    
    @api.multi
    def fusion(self):
        print "fusion"