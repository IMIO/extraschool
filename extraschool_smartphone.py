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
import cStringIO
import base64
import os


class extraschool_smartphone(osv.osv):
    _name = 'extraschool.smartphone'
    _description = 'Smartphone'

    _columns = {
        'name' : fields.char('Name', size=50),         
        'placeid' : fields.many2one('extraschool.place', 'Schoolcare Place', required=True),
        'activitycategories_ids' : fields.many2many('extraschool.activitycategory','extraschool_smartphone_activitycategory_rel', 'smartphone_id', 'activitycategory_id','Activity categories'),
        'lasttransmissiondate' : fields.datetime('Last Transmission Date'),
        'softwareurl' : fields.char('Software url', size=100, readonly=True),
        'transmissiontime' : fields.char('Transmission time', size=5),    
        'serveraddress' : fields.char('Server address', size=50),
        'databasename' : fields.char('Database name', size=30),
        'username' : fields.char('User name', size=30),
        'userpassword' : fields.char('User password', size=20),
        'scanmethod' : fields.selection((('Tag','Tag'),('QR','QR')),'Scan method'),
        'transfertmethod' : fields.selection((('WIFI','WIFI'),('3G','3G')),'Transfert method'),
        'qrdownload' : fields.binary('QR Download'),
        'qrconfig' : fields.binary('QR Config'),
        'oldversion': fields.boolean('Old version'),
        'maxtimedelta': fields.integer('Max time delta'),
    }
    
    _defaults = {
        'softwareurl' : lambda *a: 'http://intranet.la-bruyere.be/garderies/V2-4/Garderies.apk'
    }
    
    
    def write(self, cr, uid, ids, vals, context=None):
        form = self.read(cr,uid,ids,)[-1]
        obj_config = self.pool.get('extraschool.mainsettings')
        config=obj_config.read(cr, uid, [1],['lastqrcodenbr','qrencode','tempfolder','templatesfolder'])[0]            
        os.system(config['qrencode']+' -o '+config['tempfolder']+'qrdownload.png -s 4 -l Q '+form['softwareurl'])        
        qrfile = open(config['tempfolder']+'qrdownload.png','r').read()
        vals['qrdownload'] = base64.b64encode(qrfile)
        if form['transmissiontime']:
            transmissiontime = form['transmissiontime']
        else:
            transmissiontime = vals['transmissiontime']
        if form['serveraddress']:
            serveraddress = form['serveraddress']
        else:
            serveraddress = vals['serveraddress']
        if form['databasename']:
            databasename = form['databasename']
        else:
            databasename = vals['databasename']
        if form['username']:
            username = form['username']
        else:
            username = vals['username']
        if form['userpassword']:
            userpassword = form['userpassword']
        else:
            userpassword = vals['userpassword']
        if form['scanmethod']:
            scanmethod = form['scanmethod']
        else:
            scanmethod = vals['scanmethod']
        if form['transfertmethod']:
            transfertmethod = form['transfertmethod']
        else:
            transfertmethod = vals['transfertmethod']
        os.system(config['qrencode']+' -o '+config['tempfolder']+'qrconfig.png -s 4 -l Q "cfg;'+str(ids[0])+';'+transmissiontime+';'+serveraddress+';'+databasename+';'+username+';'+userpassword+';'+scanmethod+';'+transfertmethod+'"')        
        qrfile = open(config['tempfolder']+'qrconfig.png','r').read()
        vals['qrconfig'] = base64.b64encode(qrfile)
        return super(extraschool_smartphone, self).write(cr, uid, ids, vals, context=context)  
extraschool_smartphone()
