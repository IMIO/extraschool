#! /usr/bin/python
import odoorpc
import xlrd

db='database'
username = 'username'
password = 'password'

odoo = odoorpc.ODOO('ip', port=1234)
odoo.login(db,username,password)

pod = odoo.env['extraschool.child']

loc = "extraschool.child.xlsx"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

for i in range(1,284):
    child = pod.search([
        ('lastname', '=ilike', sheet.cell_value(i,0)),
        ('firstname', '=ilike', sheet.cell_value(i,1)),
    ])
    if not child:
        print (sheet.cell_value(i,0), sheet.cell_value(i,1))
    pod.browse(child).tagid = str(sheet.cell_value(i,2))
