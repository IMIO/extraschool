import odoorpc

db='aes_seraing'
username = 'admin'
password = 'admin'

odoo = odoorpc.ODOO('localhost', port=8069)
odoo.login(db,username,password)

pod = odoo.env['extraschool.prestation_times_of_the_day']
result = pod.search([
		   ('prestationtime_ids.prestation_date', '>=', '01/01/2017'),
    	 	   ('prestationtime_ids.prestation_date', '<=', '31/03/2017'),
		   ('prestationtime_ids.invoiced_prestation_id', '=', 'null')
		   ])

for i in result:
    print (i)
