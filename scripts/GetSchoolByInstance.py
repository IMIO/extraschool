#!/usr/bin/env python

import xmlrpclib

with open("keepass.csv") as file:
    content = file.readlines()

    output_file = open("output.csv", "w")
    for line in content:
        line = line.split(',')
        instance = line[0].replace('"', '').lower()

        url = "https://{}-aes.imio-app.be".format(instance)
        db = "{}_extraschool".format(instance)
        username = 'dashboard'
        password= ""
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))

        uid = common.authenticate(db, username, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        number_schools = models.execute_kw(db, uid, password,
                          'extraschool.school', 'search_count',
                          [[['name', '!=', 'AES']]])

        print("Commune de {} a {} ecoles".format(instance, number_schools))
        output_file.write("{},{}\n".format(instance, number_schools))
    output_file.close()
