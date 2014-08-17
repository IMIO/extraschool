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
    '''
    def importpaiements(self, cr, uid, ids, context=None):
        import xlrd
        workbook = xlrd.open_workbook('/opt/garderies/paiements.xlsx')
        worksheets = workbook.sheet_names()
        book_datemode = workbook.datemode
        worksheet = workbook.sheet_by_name(worksheets[0])
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        rejectstr='-------------------------------------------\n'
        curr_row=0
        invoice_obj = self.pool.get('extraschool.invoice')
        payment_obj = self.pool.get('extraschool.payment')
        while curr_row < num_rows:
            curr_row += 1
            amount=worksheet.cell_value(curr_row, 8)
            year, month, day, hour, minute, second = xlrd.xldate_as_tuple(worksheet.cell_value(curr_row, 7), book_datemode)
            transfertdate = str(year)+'-'+str(month)+'-'+str(day)
            parentaccount=worksheet.cell_value(curr_row, 2)
            name=worksheet.cell_value(curr_row, 3)
            try:
                communication=str(int(worksheet.cell_value(curr_row, 6)))
            except:
                communication=''
            cr.execute('select invoicecomstructprefix from extraschool_activitycategory')
            prefixes=cr.dictfetchall()
            prefixfound=False                    
            for prefix in prefixes:
                    if (len(prefix['invoicecomstructprefix']) > 0) and (len(communication) > len(prefix['invoicecomstructprefix'])):
                        if communication[0:len(prefix['invoicecomstructprefix'])] == prefix['invoicecomstructprefix']:
                            prefixfound=True
            if prefixfound:                            
                invoice_ids=invoice_obj.search(cr, uid, [('structcom', '=', communication)])                           
                if len(invoice_ids)==1:
                    invoice=invoice_obj.read(cr, uid, invoice_ids,['amount_received','balance'])[0]
                    if invoice['balance'] < amount:
                        rejectstr=rejectstr+str(curr_row+1)+' - '+str(amount)+' - Amount greather than invoice balance\n'
                    else:
                        invoice_obj.write(cr, uid, invoice_ids,{'amount_received':invoice['amount_received']+amount,'balance':invoice['balance']-amount})
                        payment_id = payment_obj.create(cr, uid, {'concernedinvoice': invoice_ids[0],'account':parentaccount,'paymenttype':'1','paymentdate':transfertdate,'structcom':communication,'name':name,'amount':amount})
                else:
                    rejectstr=rejectstr+str(curr_row+1)+' - '+str(amount)+' - No valid structured Communication\n'
            else:
                rejectstr=rejectstr+str(curr_row+1)+' - '+str(amount)+' - No valid structured Communication\n'
        print rejectstr
        print '-------------------------------------------'
        return True
    '''
    def initdefaultvalues(self, cr, uid, ids, context=None):
        obj_config = self.pool.get('extraschool.mainsettings')
        obj_level = self.pool.get('extraschool.level')
        obj_childtype = self.pool.get('extraschool.childtype')
        obj_class = self.pool.get('extraschool.class')
        obj_childposition = self.pool.get('extraschool.childposition')
        obj_importlevelrule = self.pool.get('extraschool.importlevelrule')
        config=obj_config.search(cr, uid, [('id','=','1')])
        if not config:
            if os.name == 'nt':
                obj_config.create(cr, uid, {'id':1,'lastqrcodenbr':0,'qrencode':'c:\\opt\\garderies\\qrcodes\\qrcode.exe','tempfolder':'c:\\opt\\garderies\\appytemp\\','templatesfolder':'c:\\opt\\garderies\\templates\\'}, context=context)
            else:
                obj_config.create(cr, uid, {'id':1,'lastqrcodenbr':0,'qrencode':'/opt/qrencode/qrencode','tempfolder':'/opt/garderies/appytemp/','templatesfolder':'/opt/garderies/templates/'}, context=context)
            l1=obj_level.create(cr, uid, {'name':'1ere Maternelle','ordernumber':1,'leveltype':'M'}, context=context)
            l2=obj_level.create(cr, uid, {'name':'2eme Maternelle','ordernumber':2,'leveltype':'M'}, context=context)
            l3=obj_level.create(cr, uid, {'name':'3eme Maternelle','ordernumber':3,'leveltype':'M'}, context=context)
            l4=obj_level.create(cr, uid, {'name':'1ere Primaire','ordernumber':4,'leveltype':'P'}, context=context)
            l5=obj_level.create(cr, uid, {'name':'2eme Primaire','ordernumber':5,'leveltype':'P'}, context=context)
            l6=obj_level.create(cr, uid, {'name':'3eme Primaire','ordernumber':6,'leveltype':'P'}, context=context)
            l7=obj_level.create(cr, uid, {'name':'4eme Primaire','ordernumber':7,'leveltype':'P'}, context=context)
            l8=obj_level.create(cr, uid, {'name':'5eme Primaire','ordernumber':8,'leveltype':'P'}, context=context)
            l9=obj_level.create(cr, uid, {'name':'6eme Primaire','ordernumber':9,'leveltype':'P'}, context=context)
            obj_childtype.create(cr, uid, {'name':'aucun'}, context=context)
            obj_childposition.create(cr, uid, {'name':'1er enfant','position':1}, context=context)
            obj_childposition.create(cr, uid, {'name':'2eme enfant','position':2}, context=context)
            obj_childposition.create(cr, uid, {'name':'3eme enfant','position':3}, context=context)
            obj_childposition.create(cr, uid, {'name':'4eme enfant','position':4}, context=context)
            obj_childposition.create(cr, uid, {'name':'5eme enfant','position':5}, context=context)
            obj_childposition.create(cr, uid, {'name':'6eme enfant','position':6}, context=context)
            obj_childposition.create(cr, uid, {'name':'7eme enfant','position':7}, context=context)
            obj_childposition.create(cr, uid, {'name':'8eme enfant','position':8}, context=context)
            obj_childposition.create(cr, uid, {'name':'9eme enfant','position':9}, context=context)
            obj_childposition.create(cr, uid, {'name':'10eme enfant','position':10}, context=context)
            obj_importlevelrule.create(cr, uid, {'levelid':l1,'startpos1':1,'endpos1':2,'equalto1':'M1'}, context=context)
            obj_importlevelrule.create(cr, uid, {'levelid':l2,'startpos1':1,'endpos1':2,'equalto1':'M2'}, context=context)
            obj_importlevelrule.create(cr, uid, {'levelid':l3,'startpos1':1,'endpos1':2,'equalto1':'M3'}, context=context)
            obj_importlevelrule.create(cr, uid, {'levelid':l4,'startpos1':1,'endpos1':2,'equalto1':'P1'}, context=context)
            obj_importlevelrule.create(cr, uid, {'levelid':l5,'startpos1':1,'endpos1':2,'equalto1':'P2'}, context=context)
            obj_importlevelrule.create(cr, uid, {'levelid':l6,'startpos1':1,'endpos1':2,'equalto1':'P3'}, context=context)
            obj_importlevelrule.create(cr, uid, {'levelid':l7,'startpos1':1,'endpos1':2,'equalto1':'P4'}, context=context)
            obj_importlevelrule.create(cr, uid, {'levelid':l8,'startpos1':1,'endpos1':2,'equalto1':'P5'}, context=context)
            obj_importlevelrule.create(cr, uid, {'levelid':l9,'startpos1':1,'endpos1':2,'equalto1':'P6'}, context=context)
    
    def updateapplication(self, cr, uid, ids, context=None):
        '''
        module_osv=self.pool.get('ir.module.module')
        module_ids=module_osv.search(cr,uid,[('name', '=', 'extraschool')])
        
        module=module_osv.read(cr,uid,module_ids[0])
        print 'upgrading "{0}"'.format('extraschool')
        module_osv.button_immediate_upgrade(cr,uid,[module_ids[0]])
        '''
        #upgrade_id=self.pool.get('base.module.upgrade').create(cr,uid,{'module_info': module_ids[0]})
        #self.pool.get('base.module.upgrade').upgrade_module(cr,uid,upgrade_id)
        os.system('/opt/garderies/extraschool/update.sh')
        pass
extraschool_initupdate_wizard()
