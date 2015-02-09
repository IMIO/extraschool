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

from openerp.osv import osv, fields

class extraschool_activityplanneddate(osv.osv):
    _name = 'extraschool.activityplanneddate'
    _description = 'Activities planned dates'

    _rec_name = 'activitydate'
        

    _columns = {
#        'name' : fields.function(_compute_name, method=True, type="char", string="Name"),        
        'activities' : fields.many2many('extraschool.activity','extraschool_activity_activityplanneddate_rel', 'activityplanneddate_id', 'activity_id','Activities'),        
        'activitydate' : fields.date('Date'),        
    }
extraschool_activityplanneddate()
