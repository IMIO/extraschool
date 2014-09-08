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
import os

class extraschool_initupdate_wizard(osv.osv_memory):
    _name = 'extraschool.initupdate_wizard'

    _columns = {
    }

    _defaults = {
    }

    def initdefaultvalues(self, cr, uid, context=None):
        obj_config = self.pool.get('extraschool.mainsettings')
        obj_level = self.pool.get('extraschool.level')
        obj_childtype = self.pool.get('extraschool.childtype')
        obj_class = self.pool.get('extraschool.class')
        obj_childposition = self.pool.get('extraschool.childposition')
        obj_importlevelrule = self.pool.get('extraschool.importlevelrule')
        config=obj_config.search(cr, uid, [('id','=','1')])
        print 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
        if not config:
            obj_config.create(cr, uid, {'id':1,'lastqrcodenbr':0,'qrencode':'/opt/qrencode/qrencode','tempfolder':'/opt/garderies/appytemp/','templatesfolder':'/opt/garderies/templates/'}, context=context)
                
    def updateapplication(self, cr, uid, ids, context=None):
        os.system('/opt/garderies/extraschool/update.sh')
        pass
extraschool_initupdate_wizard()
