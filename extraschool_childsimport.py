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
import xlrd
import lbutils
import base64
from openerp.exceptions import except_orm, Warning, RedirectWarning


class extraschool_childsimport(models.Model):
    _name = 'extraschool.childsimport'

    schoolimplantation = fields.Many2one('extraschool.schoolimplantation', 'School implantation',required=True)
    childsimportfilter = fields.Many2one('extraschool.childsimportfilter', 'Childs import filter',required=True)
    childsfile = fields.Binary('Childs File',required=True)
    
    @api.model
    def create(self, vals): 
        cr, uid = self.env.cr, self.env.user.id
        
        workbook = xlrd.open_workbook(file_contents=base64.b64decode(vals['childsfile']))
        worksheets = workbook.sheet_names()
        book_datemode = workbook.datemode
        worksheet = workbook.sheet_by_name(worksheets[0])
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        schoolimplantationid = vals['schoolimplantation']
        obj_filter = self.pool.get('extraschool.childsimportfilter')
        obj_child = self.pool.get('extraschool.child')
        obj_parent = self.pool.get('extraschool.parent')
        obj_class = self.pool.get('extraschool.class')
        obj_levelrule = self.pool.get('extraschool.importlevelrule')
        obj_childtype = self.pool.get('extraschool.childtype')
        childtypeid = obj_childtype.search(cr, uid, [('name', '=', 'aucun')])[0]
        importfilter=obj_filter.read(cr, uid, [vals['childsimportfilter']],
                                                    ['startrow',
                                                     'childrncolumn',
                                                     'childrncolumnname',
                                                     'childlastnamecolumn',
                                                     'childlastnamecolumnname',
                                                     'childfirstnamecolumn',
                                                     'childfirstnamecolumnname',
                                                     'childbirthdatecolumn',
                                                     'childbirthdatecolumnname',
                                                     'childclassnamecolumns',
                                                     'childclassnamecolumnsname',
                                                     'childlevelcolumns',
                                                     'childlevelcolumnsname',
                                                     'importlevelrule_ids',
                                                     'childotherrefcolumn',
                                                     'childotherrefcolumnname',
                                                     'parentrncolumn',
                                                     'parentrncolumnname',
                                                     'parentlastnamecolumn',
                                                     'parentlastnamecolumnname',
                                                     'parentfirstnamecolumn',
                                                     'parentfirstnamecolumnname',
                                                     'parentstreetcolumns',
                                                     'parentstreetcolumnsname',
                                                     'parentzipcodecolumn',
                                                     'parentzipcodecolumnname',
                                                     'parentcitycolumn',
                                                     'parentcitycolumnname',
                                                     'parenthousephonecolumn',
                                                     'parenthousephonecolumnname',
                                                     'parentworkphonecolumn',
                                                     'parentworkphonecolumnname',
                                                     'parentgsmcolumn',
                                                     'parentgsmcolumnname',
                                                     'parentemailcolumn',
                                                     'parentemailcolumnname',
                                                     'majchildclassname',
                                                     'majchildlevel',
                                                     'majchildotherref',
                                                     'majparentlastname',
                                                     'majparentfirstname',
                                                     'majparentstreet',
                                                     'majparentzipcode',
                                                     'majparentcity',
                                                     'majparenthousephone',
                                                     'majparentworkphone',
                                                     'majparentgsm',
                                                     'majparentemail',
                                                     'majschoolimplantation'])[0]
        startrow = importfilter['startrow']-1
        curr_row = startrow
        
        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            childrn=''
            childlastname=''
            childfirstname=''
            childbirthdate=''
            childclassname=''
            childlevel=''
            childlevelid=0
            childotherref=''
            parentrn=''
            parentlastname=''
            parentfirstname=''
            parentstreet=''
            parentzipcode=''
            parentcity=''
            parenthousephone=''
            parentworkphone=''
            parentgsm=''
            parentemail=''            
            error=False
            if importfilter['childrncolumn'] <> 0:
                if lbutils.genstreetcode(worksheet.cell_value(startrow, importfilter['childrncolumn']-1)) == lbutils.genstreetcode(importfilter['childrncolumnname']):
                    childrn=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['childrncolumn']-1),worksheet.cell_value(curr_row, importfilter['childrncolumn']-1))
                else:
                    raise Warning('Error columns does not match childRN')
            if importfilter['childlastnamecolumn'] <> 0:
                if lbutils.genstreetcode(worksheet.cell_value(startrow, importfilter['childlastnamecolumn']-1)) == lbutils.genstreetcode(importfilter['childlastnamecolumnname']):
                    childlastname=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['childlastnamecolumn']-1),worksheet.cell_value(curr_row, importfilter['childlastnamecolumn']-1))
                else:
                    raise Warning('Error columns does not match childlastname')
            if importfilter['childfirstnamecolumn'] <> 0:
                if lbutils.genstreetcode(worksheet.cell_value(startrow, importfilter['childfirstnamecolumn']-1)) == lbutils.genstreetcode(importfilter['childfirstnamecolumnname']):
                    childfirstname=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['childfirstnamecolumn']-1),worksheet.cell_value(curr_row, importfilter['childfirstnamecolumn']-1))
                else:
                    raise Warning('Error columns does not match childfirstname')
            if importfilter['childbirthdatecolumn'] <> 0:
                if lbutils.genstreetcode(worksheet.cell_value(startrow, importfilter['childbirthdatecolumn']-1)) == lbutils.genstreetcode(importfilter['childbirthdatecolumnname']):
                    cell_type = worksheet.cell_type(curr_row, importfilter['childbirthdatecolumn']-1)
                    if cell_type==3:
                        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(worksheet.cell_value(curr_row, importfilter['childbirthdatecolumn']-1), book_datemode)
                        childbirthdate = str(year)+'-'+str(month)+'-'+str(day)
                    else:
                        if cell_type==1:
                            day,month,year = worksheet.cell_value(curr_row, importfilter['childbirthdatecolumn']-1).strip().split('/')
                            childbirthdate = str(year)+'-'+str(month)+'-'+str(day)
                else:
                    raise Warning('Error columns does not match childbirthdate')
            if importfilter['childclassnamecolumns'] <> '0':
                columns = importfilter['childclassnamecolumns'].split(',')
                columnsnames = importfilter['childclassnamecolumnsname'].split(',')
                i=0
                for column in columns:
                    if lbutils.genstreetcode(worksheet.cell_value(startrow, int(column)-1)) == lbutils.genstreetcode(columnsnames[i]):
                        childclassname=childclassname+lbutils.strcell(worksheet.cell_type(curr_row, int(column)-1),worksheet.cell_value(curr_row, int(column)-1))
                    else:
                        raise Warning('Error columns does not match childclassname')
                    i=i+1
            if importfilter['childlevelcolumns'] <> '0':
                columns = importfilter['childlevelcolumns'].split(',')
                columnsnames = importfilter['childlevelcolumnsname'].split(',')
                i=0
                for column in columns:
                    if lbutils.genstreetcode(worksheet.cell_value(startrow, int(column)-1)) == lbutils.genstreetcode(columnsnames[i]):
                        childlevel=childlevel+lbutils.strcell(worksheet.cell_type(curr_row, int(column)-1),worksheet.cell_value(curr_row, int(column)-1))
                    else:
                        raise Warning('Error columns does not match childlevel')
                    i=i+1
            for levelruleid in importfilter['importlevelrule_ids']:
                levelrule=obj_levelrule.read(cr, uid, [levelruleid],['levelid','startpos1','endpos1','equalto1'])[0]
                if len(childlevel) >= levelrule['endpos1']:
                    if childlevel[levelrule['startpos1']-1:levelrule['endpos1']]==levelrule['equalto1']:
                        childlevelid=levelrule['levelid'][0]
            if importfilter['childotherrefcolumn'] <> 0:
                if lbutils.genstreetcode(worksheet.cell_value(startrow, importfilter['childotherrefcolumn']-1)) == lbutils.genstreetcode(importfilter['childotherrefcolumnname']):
                    childotherref=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['childotherrefcolumn']-1),worksheet.cell_value(curr_row, importfilter['childotherrefcolumn']-1))
                else:
                    raise Warning('Error columns does not match childotherref')
            if importfilter['parentrncolumn'] <> 0:
                if lbutils.genstreetcode(worksheet.cell_value(startrow, importfilter['parentrncolumn']-1)) == lbutils.genstreetcode(importfilter['parentrncolumnname']):
                    parentrn=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['parentrncolumn']-1),worksheet.cell_value(curr_row, importfilter['parentrncolumn']-1))
                else:
                    raise Warning('Error columns does not match parentrn')
            if importfilter['parentlastnamecolumn'] <> 0:
                if lbutils.genstreetcode(worksheet.cell_value(startrow, importfilter['parentlastnamecolumn']-1)) == lbutils.genstreetcode(importfilter['parentlastnamecolumnname']):
                    parentlastname=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['parentlastnamecolumn']-1),worksheet.cell_value(curr_row, importfilter['parentlastnamecolumn']-1))
                else:
                    raise Warning('Error columns does not match parentlastname')
            if importfilter['parentfirstnamecolumn'] <> 0:
                if lbutils.genstreetcode(worksheet.cell_value(startrow, importfilter['parentfirstnamecolumn']-1)) == lbutils.genstreetcode(importfilter['parentfirstnamecolumnname']):
                    parentfirstname=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['parentfirstnamecolumn']-1),worksheet.cell_value(curr_row, importfilter['parentfirstnamecolumn']-1))
                else:
                    raise Warning('Error columns does not match parentfirstname')
            if importfilter['parentstreetcolumns'] <> '0':
                columns = importfilter['parentstreetcolumns'].split(',')
                columnsnames = importfilter['parentstreetcolumnsname'].split(',')
                i=0
                for column in columns:
                    if lbutils.genstreetcode(lbutils.strcell(worksheet.cell_type(startrow, int(column)-1),worksheet.cell_value(startrow, int(column)-1))) == lbutils.genstreetcode(columnsnames[i]):
                        if i>0:
                            parentstreet=parentstreet+' '
                        parentstreet=parentstreet+lbutils.strcell(worksheet.cell_type(curr_row, int(column)-1),worksheet.cell_value(curr_row, int(column)-1))
                    else:
                        raise Warning('Error columns does not match parentstreet')
                    i=i+1
            if importfilter['parentzipcodecolumn'] <> 0:
                if lbutils.genstreetcode(lbutils.strcell(worksheet.cell_type(startrow, importfilter['parentzipcodecolumn']-1),worksheet.cell_value(startrow, importfilter['parentzipcodecolumn']-1))) == lbutils.genstreetcode(importfilter['parentzipcodecolumnname']):
                    parentzipcode = lbutils.strcell(worksheet.cell_type(curr_row, importfilter['parentzipcodecolumn']-1),worksheet.cell_value(curr_row, importfilter['parentzipcodecolumn']-1))
                else:
                    raise Warning('Error columns does not match parentzipcode')
            if importfilter['parentcitycolumn'] <> 0:
                if lbutils.genstreetcode(lbutils.strcell(worksheet.cell_type(startrow, importfilter['parentcitycolumn']-1),worksheet.cell_value(startrow, importfilter['parentcitycolumn']-1))) == lbutils.genstreetcode(importfilter['parentcitycolumnname']):
                    parentcity=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['parentcitycolumn']-1),worksheet.cell_value(curr_row, importfilter['parentcitycolumn']-1))
                else:
                    raise Warning('Error columns does not match parentcity')
            if importfilter['parenthousephonecolumn'] <> 0:
                if lbutils.genstreetcode(lbutils.strcell(worksheet.cell_type(startrow, importfilter['parenthousephonecolumn']-1),worksheet.cell_value(startrow, importfilter['parenthousephonecolumn']-1))) == lbutils.genstreetcode(importfilter['parenthousephonecolumnname']):
                    parenthousephone=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['parenthousephonecolumn']-1),worksheet.cell_value(curr_row, importfilter['parenthousephonecolumn']-1))
                else:
                    raise Warning('Error columns does not match parenthousephone')
            if importfilter['parentworkphonecolumn'] <> 0:
                if lbutils.genstreetcode(lbutils.strcell(worksheet.cell_type(startrow, importfilter['parentworkphonecolumn']-1),worksheet.cell_value(startrow, importfilter['parentworkphonecolumn']-1))) == lbutils.genstreetcode(importfilter['parentworkphonecolumnname']):
                    parentworkphone=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['parentworkphonecolumn']-1),worksheet.cell_value(curr_row, importfilter['parentworkphonecolumn']-1))
                else:
                    raise Warning('Error columns does not match parentworkphone')
            if importfilter['parentgsmcolumn'] <> 0:
                if lbutils.genstreetcode(lbutils.strcell(worksheet.cell_type(startrow, importfilter['parentgsmcolumn']-1),worksheet.cell_value(startrow, importfilter['parentgsmcolumn']-1))) == lbutils.genstreetcode(importfilter['parentgsmcolumnname']):
                    parentgsm=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['parentgsmcolumn']-1),worksheet.cell_value(curr_row, importfilter['parentgsmcolumn']-1))
                else:
                    raise Warning('Error columns does not match parentgsm')
            if importfilter['parentemailcolumn'] <> 0:
                if lbutils.genstreetcode(lbutils.strcell(worksheet.cell_type(startrow, importfilter['parentemailcolumn']-1),worksheet.cell_value(startrow, importfilter['parentemailcolumn']-1))) == lbutils.genstreetcode(importfilter['parentemailcolumnname']):
                    parentemail=lbutils.strcell(worksheet.cell_type(curr_row, importfilter['parentemailcolumn']-1),worksheet.cell_value(curr_row, importfilter['parentemailcolumn']-1))
                else:
                    raise Warning('Error columns does not match parentemail')
     
            
            if not ((childlastname == '') and (childfirstname == '') and (childbirthdate == '') and (childlevelid == 0) and (parentlastname == '')):
                if (childlastname == '') or (childfirstname == '') or (childbirthdate == '') or (childlevelid == 0) or (parentlastname == ''):
                    raise Warning("""Error at line: %s
                                     childlastname:%s
                                     childfirstname:%s
                                     childbirthdate:%s
                                     childlevelid:%s
                                     parentlastname:%s                                     
                                    """ % (curr_row+1,childlastname,childfirstname,childbirthdate,childlevelid,parentlastname))
                else:
                    if importfilter['childrncolumn'] <> 0:
                        childid = obj_child.search(cr, uid, [('rn', '=', childrn.strip())
                                                             ])
                    # if no rn or child not found on RN try to find on firstname,lastname,birthday
                    if not childid or importfilter['childrncolumn'] == 0:
                        childid = obj_child.search(cr, uid, [('lastname', 'ilike', childlastname.strip()),('firstname', 'ilike', childfirstname.strip()),('birthdate', '=', childbirthdate)])
                    
                    if not childid:
                        if importfilter['parentrncolumn'] <> 0:
                            parentids = obj_parent.search(cr, uid, [('rn', '=', parentrn),]) 
                        # if no rn or child not found on RN try to find on firstname,lastname,birthday  
                        print "parent : %s-%s rn : %s" % (parentlastname,parentfirstname,parentrn)
                        if not parentids or importfilter['parentrncolumn'] == 0 or parentrn == '':
                            parentids = obj_parent.search(cr, uid, [('lastname', 'ilike', parentlastname),('firstname', 'ilike', parentfirstname),('streetcode', 'ilike', lbutils.genstreetcode(parentstreet+parentcity))])
                        if not parentids:
                            parentid = obj_parent.create(cr, uid, {'name':parentlastname+' '+parentfirstname,
                                                                   'rn':parentrn,
                                                                   'lastname':parentlastname,
                                                                   'firstname':parentfirstname,
                                                                   'streetcode':lbutils.genstreetcode(parentstreet+parentcity),
                                                                   'street':parentstreet,
                                                                   'zipcode':parentzipcode,
                                                                   'city':parentcity,
                                                                   'housephone':parenthousephone,
                                                                   'workphone':parentworkphone,
                                                                   'gsm':parentgsm,
                                                                   'email':parentemail,
                                                                   'modified_since_last_import': False,
                                                                   'last_import_date':fields.datetime.now(),
                                                                    })
                        else:
                            parentid=parentids[0]
                        classids = obj_class.search(cr, uid, [('name', 'ilike', childclassname),('schoolimplantation', '=', schoolimplantationid)])
                        if not classids:
                            levelids=[]
                            levelids.append((6,0,[childlevelid]))
                            classid = obj_class.create(cr, uid, {'name':childclassname,'schoolimplantation':schoolimplantationid,'levelids':levelids})
                        else:
                            classid = classids[0]
                        obj_child.create(cr, uid, {'name':childlastname+' '+childfirstname,
                                                   'lastname':childlastname,
                                                   'firstname':childfirstname,
                                                   'rn':childrn,
                                                   'schoolimplantation':schoolimplantationid,
                                                   'levelid':childlevelid,
                                                   'classid':classid,
                                                   'parentid':parentid,
                                                   'birthdate':childbirthdate,
                                                   'otherref':childotherref,
                                                   'childtypeid':childtypeid,
                                                   'modified_since_last_import': False,
                                                   'last_import_date':fields.datetime.now(),
                                                   })
                    else:
                        #MAJ Child
                        for child_id in childid:
                            child = obj_child.read(cr, uid, [child_id],['parentid','modified_since_last_import','rn'])[0]
                            if child['modified_since_last_import'] == False:
                                parentid = child['parentid'][0]
                                if importfilter['majschoolimplantation']:
                                    obj_child.write(cr,uid,[child_id],{'schoolimplantation':schoolimplantationid})
                                if importfilter['majchildclassname']:
                                    classids = obj_class.search(cr, uid, [('name', 'ilike', childclassname),('schoolimplantation', '=', schoolimplantationid)])
                                    if not classids:
                                        levelids=[]
                                        levelids.append((6,0,[childlevelid]))
                                        classid = obj_class.create(cr, uid, {'name':childclassname,'schoolimplantation':schoolimplantationid,'levelids':levelids})
                                    else:
                                        classid = classids[0]
                                    obj_child.write(cr,uid,[child_id],{'classid':classid})
                                if importfilter['majchildlevel']:
                                    obj_child.write(cr,uid,[child_id],{'levelid':childlevelid})
                                if importfilter['majchildotherref']:
                                    obj_child.write(cr,uid,[child_id],{'otherref':childotherref})
                                    
                                    
                                obj_parent.write(cr,uid,[parentid],{'modified_since_last_import':False,
                                                                    'last_import_date':fields.datetime.now()})
                        
                            #MAJ PARENT   
                            parent = obj_parent.read(cr, uid, [parentid],['firstname','lastname','rn','modified_since_last_import'])[0]
                            if  parent['firstname'].lower() == parentfirstname.lower() and parent['lastname'].lower() == parentlastname.lower():
                                #print "check rn %s vs %s" % (parent['rn'],parentrn) 
                                if (parent['rn'] == False or parent['rn'] == '') and (parentrn != False and parentrn != ''):
                                    #print "upate rn"
                                    obj_parent.write(cr,uid,[parentid],{'rn':parentrn})
                                if parent['modified_since_last_import'] == False:
                                    if importfilter['majparentlastname']:                            
                                        obj_parent.write(cr,uid,[parentid],{'lastname':parentlastname})
                                    if importfilter['majparentfirstname']:
                                        obj_parent.write(cr,uid,[parentid],{'firstname':parentfirstname})
                                    if importfilter['majparentstreet']:
                                        obj_parent.write(cr,uid,[parentid],{'street':parentstreet,'streetcode':lbutils.genstreetcode(parentstreet+parentcity)})
                                    if importfilter['majparentzipcode']:
                                        obj_parent.write(cr,uid,[parentid],{'zipcode':parentzipcode})
                                    if importfilter['majparentcity']:
                                        obj_parent.write(cr,uid,[parentid],{'city':parentcity,'streetcode':lbutils.genstreetcode(parentstreet+parentcity)})                            
                                    if importfilter['majparenthousephone']:
                                        obj_parent.write(cr,uid,[parentid],{'housephone':parenthousephone})
                                    if importfilter['majparentworkphone']:
                                        obj_parent.write(cr,uid,[parentid],{'workphone':parentworkphone})
                                    if importfilter['majparentgsm']:
                                        obj_parent.write(cr,uid,[parentid],{'gsm':parentgsm})
                                    if importfilter['majparentemail']:
                                        obj_parent.write(cr,uid,[parentid],{'email':parentemail})

                                    obj_parent.write(cr,uid,[parentid],{'modified_since_last_import':False,
                                                                        'last_import_date':fields.datetime.now()})
                            else:
                                if importfilter['parentrncolumn'] <> 0:
                                    parentids = obj_parent.search(cr, uid, [('rn', '=', parentrn),]) 
                                # if no rn or child not found on RN try to find on firstname,lastname,birthday  
                                #print "parent : %s-%s rn : %s" % (parentlastname,parentfirstname,parentrn)
                                if not parentids or importfilter['parentrncolumn'] == 0 or parentrn == '':
                                    parentids = obj_parent.search(cr, uid, [('lastname', 'ilike', parentlastname),('firstname', 'ilike', parentfirstname),('streetcode', 'ilike', lbutils.genstreetcode(parentstreet+parentcity))])
                                if not parentids:
                                    #print "create parent %s %s" % (parentlastname,parentfirstname) 
                                    parentid = obj_parent.create(cr, uid, {'name':parentlastname+' '+parentfirstname,
                                                                           'rn':parentrn,
                                                                           'lastname':parentlastname,
                                                                           'firstname':parentfirstname,
                                                                           'streetcode':lbutils.genstreetcode(parentstreet+parentcity),
                                                                           'street':parentstreet,
                                                                           'zipcode':parentzipcode,
                                                                           'city':parentcity,
                                                                           'housephone':parenthousephone,
                                                                           'workphone':parentworkphone,
                                                                           'gsm':parentgsm,
                                                                           'email':parentemail,
                                                                           'modified_since_last_import': False,
                                                                           'last_import_date':fields.datetime.now(),
                                                                            })     
                                else:
                                    parentid=parentids[0]   
                                print "parent_id : %s" % (parentid)
                                obj_child.write(cr,uid,[child_id],{'parentid':parentid})                   
                                
        return super(extraschool_childsimport, self).create(vals)

