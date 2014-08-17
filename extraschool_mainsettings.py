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

class extraschool_mainsettings(osv.osv):
    _name = 'extraschool.mainsettings'
    _description = 'Main Settings'

    _columns = {
        'lastqrcodenbr' : fields.integer('lastqrcodenbr'),
        'qrencode' : fields.char('qrencode', size=80),
        'tempfolder' : fields.char('tempfolder', size=80),
        'templatesfolder' : fields.char('templatesfolder', size=80),
        'codasfolder' : fields.char('codasfolder', size=80),
        'processedcodasfolder' : fields.char('processedcodasfolder', size=80),
        'emailfornotifications': fields.char('Email for notifications', size=80),
    }
    
    def update(self, cr, uid, ids, context=None):
        obj_config = self.pool.get('extraschool.mainsettings')
        form = self.read(cr,uid,ids,)[-1]
        mainsettings_id = obj_config.write(cr, uid, ids[0], {'lastqrcodenbr':form['lastqrcodenbr'],'qrencode':form['qrencode'],'tempfolder':form['tempfolder'],'templatesfolder':form['templatesfolder'],'codasfolder':form['codasfolder'],'processedcodasfolder':form['processedcodasfolder']}, context=context)
        return {'warning': {'title': 'Record saved','message': 'record saved!',}}
        
    def initdef(self, cr, uid, ids, context=None):
        pass
extraschool_mainsettings()
