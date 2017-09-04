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
from openerp import models, api, fields,_
from openerp.api import Environment
import cStringIO
import base64
import os
from pyPdf import PdfFileWriter, PdfFileReader
import datetime
from xlrd import open_workbook
from xlutils.copy import copy
from xlutils.styles import Styles
import xlwt
from xlwt import *
from datetime import date, datetime, timedelta as td
from openerp.exceptions import Warning
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)

class extraschool_one_report_day(models.Model):
    _name = 'extraschool.one_report_day'
    
    one_report_id = fields.Many2one('extraschool.one_report',ondelete='cascade')
    day_date = fields.Date()
    child_ids = fields.Many2many(comodel_name='extraschool.child',
                               relation='extraschool_one_report_day_child_rel',
                               column1='one_report_day_id',
                               column2='child_id')
    subvention_type = fields.Selection((('sf','operating grants'), ('sdp','positive differentiation grants')))
    nb_m_childs = fields.Integer()
    nb_p_childs = fields.Integer()
    nb_childs = fields.Integer(compute='_compute_nb_childs')
    
    @api.depends('nb_m_childs','nb_p_childs')
    def _compute_nb_childs(self):
        for rec in self:
            self.nb_childs = self.nb_m_childs + self.nb_p_childs

extraschool_one_report_day()

class extraschool_one_report(models.Model):
    _name = 'extraschool.one_report'

    @api.multi
    def name_get(self):
        res = []
        for report_one in self:
            res.append((report_one.id, _("One Report from %s") %
                datetime.strptime(report_one.transmissiondate, DEFAULT_SERVER_DATE_FORMAT).strftime("%d-%m-%Y")))
        return res

    def _default_activitycategory(self):
        activitycategory_rs = self.env['extraschool.activitycategory']
    
    placeid = fields.Many2one('extraschool.place', default=1)
    activitycategory = fields.Many2one('extraschool.activitycategory', default=1)
    year = fields.Integer(required=True, default=2014)
    quarter = fields.Selection(((1,'1er'), (2,'2eme'), (3,'3eme'), (4,'4eme')), required=True, default=1 )
    transmissiondate = fields.Date(required=True, default='2015-07-01')
    nb_m_childs = fields.Integer()
    nb_p_childs = fields.Integer()
    nb_childs = fields.Integer(compute='_compute_nb_childs')
    report = fields.Binary()
    
    def compute_tablesf(self):
        return [{'href':'http://www.labruyere.be','value':'1'},{'href':'http://www.labruyere.be','value':'2'},{'href':'http://www.labruyere.be','value':'3'}]
    
    @api.depends('nb_m_childs','nb_p_childs')
    def _compute_nb_childs(self):
        for rec in self:
            self.nb_childs = self.nb_m_childs + self.nb_p_childs
    
    def _monthdays(self,y, m):
        m += 1
        if m == 13:
            m = 1
            y += 1
        next_month = datetime(y, m, 1)

        return (next_month + td(-1)).day

    def _getXLCell(self,XLSheet, irow, icol):
        row = XLSheet._Worksheet__rows.get(irow)
        cell = row._Row__cells.get(icol)
        return cell

    def setXLCell(self,XLSheet, row, col, value):
        previousCell = self._getXLCell(XLSheet,row,col)
        XLSheet.write(row, col, value)
        self._getXLCell(XLSheet,row,col).xf_idx = previousCell.xf_idx

    def search_childs(self,placeid,activitycategory,currentdate,level,subvention_type):
        self.env.cr.execute('''
                                select distinct(childid) from extraschool_invoicedprestations left join extraschool_child on childid=extraschool_child.id where 
                                placeid=%s 
                                and prestation_date=%s 
                                and activity_occurrence_id in (select id from extraschool_activityoccurrence where activityid in (select id from extraschool_activity where category=%s and subsidizedbyone=true)) 
                                and levelid in (select id from extraschool_level where leveltype=%s) 
                                and extraschool_child.parentid in (select id from extraschool_parent where one_subvention_type=%s)
                                ''', (placeid,currentdate,activitycategory,level,subvention_type))
        extraschool_one_report_childs = self.env.cr.dictfetchall()

        return [extraschool_one_report_child['childid'] for extraschool_one_report_child in extraschool_one_report_childs]

    def count_childs_quarter(self,placeid,activitycategory,date_from,date_to,level):
        self.env.cr.execute('''
                                select count(distinct(childid)) as count_child from extraschool_invoicedprestations left join extraschool_child on childid=extraschool_child.id where 
                                placeid=%s 
                                and prestation_date>=%s and prestation_date<=%s  
                                and activity_occurrence_id in (select id from extraschool_activityoccurrence where activityid in (select id from extraschool_activity where category=%s and subsidizedbyone=true)) 
                                and levelid in (select id from extraschool_level where leveltype=%s)                                 
                                ''', (placeid,date_from,date_to,activitycategory,level))
        
        extraschool_one_report_childs = self.env.cr.dictfetchall()
        print '''
                                select count(distinct(childid)) as count_child from extraschool_invoicedprestations left join extraschool_child on childid=extraschool_child.id where 
                                placeid=%s 
                                and prestation_date>=%s and prestation_date<=%s  
                                and activity_occurrence_id in (select id from extraschool_activityoccurrence where activityid in (select id from extraschool_activity where category=%s and subsidizedbyone=true)) 
                                and levelid in (select id from extraschool_level where leveltype=%s)                                 
                                ''' % (placeid,date_from,date_to,activitycategory,level)
        print "count_child : %s" % (extraschool_one_report_childs[0]['count_child'])
        return extraschool_one_report_childs[0]['count_child']
    
    @api.model
    def create(self,vals):
        month_names=('','Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre')
        obj_one_report_day = self.env['extraschool.one_report_day']
        new_obj = super(extraschool_one_report, self).create(vals)
        place_obj = self.env['extraschool.place']
        one_report_settings_obj = self.env['extraschool.onereport_settings']

        one_report_settings = one_report_settings_obj.search([('validity_from', '<=',vals['transmissiondate']),('validity_to', '>=',vals['transmissiondate']),])

        if not one_report_settings:
            raise Warning(_("There is no ONE report configuration"))

        print "----------"
        print one_report_settings
        print "----------"
        report_template_filename = '/tmp/one_report_template'+str(datetime.now())+'.xls'
        report_logoone_filename = '/tmp/one'+str(datetime.now())+'.bmp'
        report_filename = '/tmp/one_report'+str(datetime.now())+'.xls'
        report_template_file = file(report_template_filename,'w')
        report_logoone_file = file(report_logoone_filename,'w')        
        report_template_file.write(one_report_settings.report_template.decode('base64'))
        report_logoone_file.write(one_report_settings.one_logo.decode('base64'))
        report_template_file.close()
        report_logoone_file.close()
        place=place_obj.browse([vals['placeid']])
        strperiod_from = str(vals['year']) + '-'+str(vals['quarter']*3-2).zfill(2) +'-01'
        strperiod_to = str(vals['year']) + '-'+str(vals['quarter']*3).zfill(2) +'-'+str(self._monthdays(vals['year'],vals['quarter']*3)).zfill(2)
        
        period_from=datetime.strptime(strperiod_from, '%Y-%m-%d').date()
        period_to=datetime.strptime(strperiod_to, '%Y-%m-%d').date()
        tot_nb_m = 0
        tot_nb_p = 0
        currentdate = period_from
        rb = open_workbook(report_template_filename, formatting_info=True, on_demand=True)
        wb = copy(rb)
        XLSheet = wb.get_sheet(0)
        XLSheet.insert_bitmap(report_logoone_filename,0,0)
        self.setXLCell(XLSheet,2,3,u"Détail, pour un lieu d'accueil, des présences du "+("1er" if vals['quarter']==1 else str(vals['quarter'])+"e")+" trimestre "+str(vals['year']))
        self.setXLCell(XLSheet,5,1,"%s" % (place.name))
        self.setXLCell(XLSheet,6,1,'%s\n%s\n%s %s' % (place.name,place.street, place.zipcode,place.city))  
        self.setXLCell(XLSheet,7,5,place.schedule)
        for imonth in range(0,3):
            currentmonth=period_from.month+imonth            
            self.setXLCell(XLSheet,14+imonth*2,0,month_names[currentmonth])
            iweek=0            
            currentdate = datetime(vals['year'],currentmonth,01)
            while (iweek < 5): 
                 
                if datetime(currentdate.year,currentdate.month,01).weekday() > 4 and iweek==0:
                    while currentdate.weekday() != 0:
                        currentdate = currentdate + td(1)
                
                for iday in range(0,5):
                    
                    if iday==currentdate.weekday():
                        self.setXLCell(wb.get_sheet(0),13+imonth*2,(iday+1)+(iweek*5),currentdate.day)
                        
                        for subvention_type in ['sf','sdp']:
                            day_nb_m = 0
                            day_nb_p = 0
                            childidsm = self.search_childs(vals['placeid'],vals['activitycategory'],currentdate,'M',subvention_type)
                            day_nb_m = day_nb_m + len(childidsm)
                            childidsp = self.search_childs(vals['placeid'],vals['activitycategory'],currentdate,'P',subvention_type)                
                            day_nb_p = day_nb_p + len(childidsp)
                            obj_one_report_day.create({'one_report_id':new_obj.id,'day_date':str(currentdate),'child_ids':[(6, 0,(childidsm + childidsp))],'subvention_type':subvention_type,'nb_m_childs':day_nb_m,'nb_p_childs':day_nb_p})
                            tot_nb_m = tot_nb_m + day_nb_m
                            tot_nb_p = tot_nb_p + day_nb_p   
                            if subvention_type == 'sf':
                                ligne = 14
                            else:         
                                ligne = 30      
                            if (day_nb_m + day_nb_p) != 0:
                                self.setXLCell(XLSheet,ligne+imonth*2,(iday+1)+(iweek*5),day_nb_m + day_nb_p)
                            else:
                                self.setXLCell(XLSheet,ligne+imonth*2,(iday+1)+(iweek*5),str(''))
                        nextdate = currentdate + td(1)
                        if nextdate.month == currentmonth:
                            currentdate=nextdate
                        else:
                            iweek=iweek+1
                nextdate = currentdate + td(2)
                if nextdate.month == currentmonth:
                    currentdate=nextdate
                iweek=iweek+1
            currentdate = currentdate + td(1)
        
        tot_nb_m = self.count_childs_quarter(place.id, vals['activitycategory'],period_from, period_to,'M')
        tot_nb_p = self.count_childs_quarter(place.id, vals['activitycategory'],period_from, period_to,'P')
        print "nbr_mat : %s" % (tot_nb_m)
        print "nbr_prim : %s" % (tot_nb_p)

        #Formules
        self.setXLCell(XLSheet,8,19,tot_nb_m)
        self.setXLCell(XLSheet,8,22,tot_nb_p)
        self.setXLCell(XLSheet,8,25,Formula('T9+W9'))
        for gapTab in [0,16]: #gapTab = ecart entre les 2 tableaux
            for row in [15,17,19,20]:
                self.setXLCell(XLSheet,row-1+gapTab,26,Formula('SUM(B'+str(row+gapTab)+':Z'+str(row+gapTab)+')'))
            for i in range(66,91): #B->Z
                self.setXLCell(XLSheet,19+gapTab,i-65,Formula(chr(i)+str(15+gapTab)+'+'+chr(i)+str(17+gapTab)+'+'+chr(i)+str(19+gapTab)+')'))                
            self.setXLCell(XLSheet,20+gapTab,26,Formula('D'+str(20+gapTab)+'+I'+str(20+gapTab)+'+N'+str(20+gapTab)+'+S'+str(20+gapTab)+'+X'+str(20+gapTab)))
        
        wb.save(report_filename)
        outfile = open(report_filename,"r").read()
        attachment_obj = self.env['ir.attachment']
        attachment_obj.create({'res_model':'extraschool.one_report','res_id':new_obj.id,'datas_fname':'rapport_one_'+vals['transmissiondate']+'.xls','name':'rapport_one_'+vals['transmissiondate']+'.xls','datas':base64.b64encode(outfile),})
        new_obj.write({'nb_m_childs':tot_nb_m,'nb_p_childs':tot_nb_p})
        os.remove(report_template_filename)
        os.remove(report_logoone_filename)
        os.remove(report_filename)
        
        return new_obj

