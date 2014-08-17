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

import xmlrpclib
import psycopg2
import psycopg2.extras
import os

conn = psycopg2.connect("dbname='recreagiquelb' user=postgres host='localhost' password=GtMsgSQL");
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

dict_cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' and table_name ILIKE 'extraschool_%' and not (table_name ILIKE '%rel') order by table_name;")
results = dict_cur.fetchall()
#results.append({'table_name':'ir_attachment'})
groups = ['extraschool_schoolcareadmin','extraschool_schoolcareuser']
try:
    os.remove('security/ir.model.access.csv')
except:
    pass
f = open('security/ir.model.access.csv','w')
f.write('id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n')
for group in groups:
    for rec in results:
        f.write('access_'+rec['table_name']+'_'+group+','+rec['table_name']+'_'+group+',model_'+rec['table_name']+','+'extraschool.'+group+',1,1,1,1\n')
        print rec['table_name']
f.close()
conn.close()

