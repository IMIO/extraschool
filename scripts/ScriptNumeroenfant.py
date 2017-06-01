import odoorpc

db='aes_seraing'
username = 'admin'
password = 'admin'

odoo = odoorpc.ODOO('localhost', port=8069)
odoo.login(db,username,password)

pod = odoo.env['extraschool.childposition']


for i in range(50):

    if not pod.search([('position', '=', i+1)]):
        pod.create({'position': i+1,'name': '%s e enfant' % (i+1),})