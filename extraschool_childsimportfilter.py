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

class extraschool_childsimportfilter(models.Model):
    _name = 'extraschool.childsimportfilter'
    _description = 'Childs import filter'

    name = fields.Char('Name', size=50)
    startrow = fields.Integer('Start row')
    childlastnamecolumn = fields.Integer('Child lastname column')
    childlastnamecolumnname = fields.Char('Child lastname column name',size=30)
    childfirstnamecolumn = fields.Integer('Child firstname column')
    childfirstnamecolumnname = fields.Char('Child firstname column name', size=30)
    childbirthdatecolumn = fields.Integer('Child birthdate column')
    childbirthdatecolumnname = fields.Char('Child birthdate column name', size=30)
    majchildclassname = fields.Boolean('MAJ')
    childclassnamecolumns = fields.Char('Child class name columns', size=10, default=0)
    childclassnamecolumnsname = fields.Char('Child class name columns name', size=60)
    majchildlevel = fields.Boolean('MAJ')
    childlevelcolumns = fields.Char('Child level column', size=10, default=0)
    childlevelcolumnsname = fields.Char('Child level columns name', size=60)
    importlevelrule_ids = fields.Many2many('extraschool.importlevelrule','extraschool_childsimportfilter_importlevelrule_rel', 'childsimportfilter_id', 'importlevelrule_id','Import level rules')        
    majchildotherref = fields.Boolean('MAJ')
    childotherrefcolumn = fields.Integer('Child other ref column')
    childotherrefcolumnname = fields.Char('Child other ref column name', size=30)
    majparentlastname = fields.Boolean('MAJ')
    parentlastnamecolumn = fields.Integer('Parent lastname column')
    parentlastnamecolumnname = fields.Char('Parent lastname column name',size=30)
    majparentfirstname = fields.Boolean('MAJ')
    parentfirstnamecolumn = fields.Integer('Parent firstname column')
    parentfirstnamecolumnname = fields.Char('Parent firstname column name', size=30)
    majparentstreet = fields.Boolean('MAJ')
    parentstreetcolumns = fields.Char('Parent street columns', size=10, default=0)
    parentstreetcolumnsname = fields.Char('Parent street columns name', size=60)
    majparentzipcode = fields.Boolean('MAJ')
    parentzipcodecolumn = fields.Integer('Parent zipcode column')
    parentzipcodecolumnname = fields.Char('Parent zipcode column name', size=30)
    majparentcity = fields.Boolean('MAJ')
    parentcitycolumn = fields.Integer('Parent city column')
    parentcitycolumnname = fields.Char('Parent city column name', size=30)
    majparenthousephone = fields.Boolean('MAJ')
    parenthousephonecolumn = fields.Integer('Parent house phone column')
    parenthousephonecolumnname = fields.Char('Parent house phone column name', size=30)
    majparentworkphone = fields.Boolean('MAJ')
    parentworkphonecolumn = fields.Integer('Parent work phone column')
    parentworkphonecolumnname = fields.Char('Parent work phone column name', size=30)
    majparentgsm = fields.Boolean('MAJ')
    parentgsmcolumn = fields.Integer('Parent gsm column')
    parentgsmcolumnname = fields.Char('Parent gsm column name', size=30)
    majparentemail = fields.Boolean('MAJ')
    parentemailcolumn = fields.Integer('Parent email column')
    parentemailcolumnname = fields.Char('Parent email column name', size=30)
    majschoolimplantation = fields.Boolean('MAJ implantation')

extraschool_childsimportfilter()
