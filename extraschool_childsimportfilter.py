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

class extraschool_childsimportfilter(osv.osv):
    _name = 'extraschool.childsimportfilter'
    _description = 'Childs import filter'

    _columns = {
        'name' : fields.char('Name', size=50),
        'startrow': fields.integer('Start row'),
        'childlastnamecolumn' : fields.integer('Child lastname column'),
        'childlastnamecolumnname' : fields.char('Child lastname column name',size=30),
        'childfirstnamecolumn' : fields.integer('Child firstname column'),
        'childfirstnamecolumnname' : fields.char('Child firstname column name', size=30),
        'childbirthdatecolumn' : fields.integer('Child birthdate column'),
        'childbirthdatecolumnname' : fields.char('Child birthdate column name', size=30),
        'majchildclassname' : fields.boolean('MAJ'),
        'childclassnamecolumns' : fields.char('Child class name columns', size=10),
        'childclassnamecolumnsname' : fields.char('Child class name columns name', size=60),
        'majchildlevel' : fields.boolean('MAJ'),
        'childlevelcolumns': fields.char('Child level column', size=10),
        'childlevelcolumnsname': fields.char('Child level columns name', size=60),
        'importlevelrule_ids':fields.many2many('extraschool.importlevelrule','extraschool_childsimportfilter_importlevelrule_rel', 'childsimportfilter_id', 'importlevelrule_id','Import level rules'),        
        'majchildotherref' : fields.boolean('MAJ'),
        'childotherrefcolumn' : fields.integer('Child other ref column'),
        'childotherrefcolumnname' : fields.char('Child other ref column name', size=30),
        'majparentlastname' : fields.boolean('MAJ'),
        'parentlastnamecolumn' : fields.integer('Parent lastname column'),
        'parentlastnamecolumnname' : fields.char('Parent lastname column name',size=30),
        'majparentfirstname' : fields.boolean('MAJ'),
        'parentfirstnamecolumn' : fields.integer('Parent firstname column'),
        'parentfirstnamecolumnname' : fields.char('Parent firstname column name', size=30),
        'majparentstreet' : fields.boolean('MAJ'),
        'parentstreetcolumns' : fields.char('Parent street columns', size=10),
        'parentstreetcolumnsname' : fields.char('Parent street columns name', size=60),
        'majparentzipcode' : fields.boolean('MAJ'),
        'parentzipcodecolumn' : fields.integer('Parent zipcode column'),
        'parentzipcodecolumnname' : fields.char('Parent zipcode column name', size=30),
        'majparentcity' : fields.boolean('MAJ'),
        'parentcitycolumn' : fields.integer('Parent city column'),
        'parentcitycolumnname' : fields.char('Parent city column name', size=30),
        'majparenthousephone' : fields.boolean('MAJ'),
        'parenthousephonecolumn' : fields.integer('Parent house phone column'),
        'parenthousephonecolumnname' : fields.char('Parent house phone column name', size=30),
        'majparentworkphone' : fields.boolean('MAJ'),
        'parentworkphonecolumn' : fields.integer('Parent work phone column'),
        'parentworkphonecolumnname' : fields.char('Parent work phone column name', size=30),
        'majparentgsm' : fields.boolean('MAJ'),
        'parentgsmcolumn' : fields.integer('Parent gsm column'),
        'parentgsmcolumnname' : fields.char('Parent gsm column name', size=30),
        'majparentemail' : fields.boolean('MAJ'),
        'parentemailcolumn' : fields.integer('Parent email column'),
        'parentemailcolumnname' : fields.char('Parent email column name', size=30),
        'majschoolimplantation' : fields.boolean('MAJ implantation'),
    }
    _defaults = {
        'childclassnamecolumns' : lambda *a: '0',
        'childlevelcolumns' : lambda *a: '0',
        'parentstreetcolumns' : lambda *a: '0',
    }
extraschool_childsimportfilter()
