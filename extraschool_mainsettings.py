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
    query_sql = fields.Text('Query Sql')
    sql_query_ids = fields.Many2one('extraschool.query_sql', 'Query SQL')

    @api.onchange('sql_query_ids')
    def _get_query_sql(self):
        self.query_sql = self.env['extraschool.query_sql'].browse(self.sql_query_ids.id).query

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

    @api.multi
    def reset(self):
        for reg in self.env['extraschool.prestation_times_of_the_day'].browse(self._context.get('active_ids')):
            reg.reset()

        return True

    @api.multi
    def check(self):
        self.merge_pod_dup()
        for reg in self.env['extraschool.prestation_times_of_the_day'].search(
                [('id', 'in', self._context.get('active_ids')), ]):
            reg.check()

        return True

    @api.multi
    def last_check_entry_exit(self):
        for reg in self.env['extraschool.prestation_times_of_the_day'].browse(self._context.get('active_ids')):
            reg.last_check_entry_exit()

        return True

    @api.multi
    def execute_sql(self):
        self.env.cr.execute(self.query_sql)

    @api.multi
    def del_pod_doublon(self):
        pda_doublon = """
                        select id, activity_category_id, date_of_the_day, child_id
                        from extraschool_prestation_times_of_the_day
                        where ('' || CASE WHEN activity_category_id is NULL 
                                THEN ''
                                ELSE activity_category_id::text END || to_char(date_of_the_day,'YYYY-MM-DD') || child_id) in ( 
                        select ('' || CASE WHEN activity_category_id is NULL 
                                THEN ''
                                ELSE activity_category_id::text END || to_char(date_of_the_day,'YYYY-MM-DD') || child_id) as zz
                        from extraschool_prestation_times_of_the_day
                        where date_of_the_day > '2016-02-01' 
                        group by zz
                        having count(*) > 1);
                    """
        self.env.cr.execute(pda_doublon)

        prestation_times_of_the_day_obj = self.env['extraschool.prestation_times_of_the_day']
        prestation_times_obj = self.env['extraschool.prestationtimes']
        pdaprestation_times_obj = self.env['extraschool.pdaprestationtimes']

        doublons = self.env.cr.dictfetchall()
        saved_activity_category_id = ''
        saved_date = ''
        saved_child = ''
        for doublon in doublons:
            if saved_activity_category_id != doublon['activity_category_id'] or saved_date != doublon[
                'date_of_the_day'] or saved_child != doublon['child_id']:
                saved_activity_category_id = doublon['activity_category_id']
                saved_date = doublon['date_of_the_day']
                saved_child = doublon['child_id']
            else:
                prestation_times_obj.search([('prestation_times_of_the_day_id', '=', doublon['id'])]).unlink()
                pdaprestation_times_obj.search([('prestation_times_of_the_day_id', '=', doublon['id'])]).unlink()
                prestation_times_of_the_day_obj.search([('id', '=', doublon['id'])]).unlink()

    @api.multi
    def merge_pod_dup(self):
        self.env['extraschool.prestation_times_of_the_day'].merge_duplicate_pod()

    @api.multi
    def reset_verified_pod_with_non_verified_presta(self):
        pod_error = """
                        select distinct(prestation_times_of_the_day_id) as id
                        from extraschool_prestationtimes p
                        left join extraschool_prestation_times_of_the_day pod on pod.id = p.prestation_times_of_the_day_id
                        where p.verified = False and pod.verified = False;
                    """
        self.env.cr.execute(pod_error)

        pod_errors = self.env.cr.dictfetchall()
        pod_error_ids = [doublon['id'] for doublon in pod_errors]

        self.env['extraschool.prestation_times_of_the_day'].browse(pod_error_ids).reset()