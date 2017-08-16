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
from openerp.exceptions import Warning
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import *

class extraschool_mainsettings(models.Model):
    _name = 'extraschool.mainsettings'
    _description = 'Main Settings'

    lastqrcodenbr = fields.Integer('lastqrcodenbr')
    qrencode = fields.Char('qrencode', size=80)
    tempfolder = fields.Char('tempfolder', size=80)
    templatesfolder = fields.Char('templatesfolder', size=80)
    codasfolder = fields.Char('codasfolder', size=80)
    processedcodasfolder = fields.Char('processedcodasfolder', size=80)
    emailfornotifications = fields.Char('Email for notifications', size=80)
    logo = fields.Binary()
    levelbeforedisable = fields.Many2one('extraschool.level', 'Level')
    last_child_upgrade_levels = fields.Date('Last child upgrade level', readonly=True)
            
    @api.one
    def update(self):
        self.write({'lastqrcodenbr':self.lastqrcodenbr, 'qrencode':self.qrencode, 'tempfolder':self.tempfolder,'templatesfolder':self.templatesfolder, 'codasfolder':self.codasfolder,'processedcodasfolder':self.processedcodasfolder})

        raise Warning('record saved!')
        
    def initdef(self):
        pass
    
    @api.one
    def update_parent_send_method(self):
        parent = self.env['extraschool.parent'].search([('email', '!=', ''),]).write({'invoicesendmethod': 'onlyemail',
                                                                                      'remindersendmethod': 'onlyemail'})
        parent = self.env['extraschool.parent'].search(['|',('email', '=', False),
                                                            ('email', '=', '')]).write({'invoicesendmethod': 'onlybymail',
                                                                                        'remindersendmethod': 'onlybymail'})
    @api.one
    def childupgradelevels(self):
        cr, uid = self.env.cr, self.env.user.id 
        obj_child = self.pool.get('extraschool.child')
        obj_class = self.pool.get('extraschool.class')
                
        obj_level = self.pool.get('extraschool.level')
        obj_child = self.pool.get('extraschool.child')
        levelbeforedisable = obj_level.read(cr, uid, [self.levelbeforedisable.id], ['ordernumber'])[0]['ordernumber']
        cr.execute('select * from extraschool_child where create_date < %s', (str(datetime.now().year)+'-07-01',))
        print 'select * from extraschool_child where create_date < %s' % (str(datetime.now().year)+'-07-01')
        childs = cr.dictfetchall()
        cr.execute('select * from extraschool_level')
        levels = cr.dictfetchall()
        for child in childs:
            # if child['id'] == 403:
            #     import pdb;pdb.set_trace()
            cr.execute('select * from extraschool_class where id in (select class_id from extraschool_class_level_rel where level_id=%s) order by name',(str(child['levelid']),))
            childClasses = cr.dictfetchall()
            currentClassPosition = 0
            i=1
            for childClass in childClasses:
                if child['classid'] == childClass['id']:
                    currentClassPosition=i
                i=i+1
            childlevel = obj_level.read(cr, uid, [child['levelid']], ['ordernumber'])[0]
            newlevelid=0
            if childlevel['ordernumber'] < levelbeforedisable:
                for level in levels:
                    if newlevelid==0 and level['ordernumber'] > childlevel['ordernumber']:
                        newlevelid=level['id']
                cr.execute('select * from extraschool_class where id in (select class_id from extraschool_class_level_rel where level_id=%s) order by name',(str(newlevelid),))
                childClasses = cr.dictfetchall()
                newclassid=0
                if currentClassPosition > 0 and len(childClasses) != 0:
                    if len(childClasses) >= currentClassPosition:        
                        newclassid = childClasses[currentClassPosition-1]['id']           
                    else:
                        newclassid = childClasses[0]['id']
                    print "update child %s  oldclass: %s - old level : %s - class : %s - level : %s" % (child['id'],child['classid'],child['levelid'],newclassid,newlevelid)                        
                    obj_child.write(cr, uid, [child['id']], {'classid': newclassid,'levelid':newlevelid})
                else:
                    print "update child %s - old level : %s - level : %s" % (child['id'],child['levelid'],newlevelid)
                    obj_child.write(cr, uid, [child['id']], {'levelid':newlevelid})
            else:
                print "disable child %s" % (child['id'])
                obj_child.write(cr, uid, [child['id']], {'isdisabled': True})

        self.last_child_upgrade_levels = datetime.now()

    @api.one
    def update_presta_stat(self):
        self.env['extraschool.presta_stat'].compute()
