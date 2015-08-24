import xmlrpclib

url = 'http://localhost:8069'
db = 'testlb'
username = 'admin'
password = 'admin'
  
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))


uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

prestationsids = models.execute_kw(db, uid, password, 'extraschool.prestationtimes', 'search', [[]])
ids = models.execute_kw(db, uid, password, 'extraschool.prestationtimes', 'unlink', [prestationsids])

prestationsids = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'search', [[]])
ids = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'unlink', [prestationsids])

prestationsids = models.execute_kw(db, uid, password, 'extraschool.prestation_times_of_the_day', 'search', [[]])
ids = models.execute_kw(db, uid, password, 'extraschool.prestation_times_of_the_day', 'unlink', [prestationsids])

prestationsids = models.execute_kw(db, uid, password, 'extraschool.invoicedprestations', 'search', [[]])
ids = models.execute_kw(db, uid, password, 'extraschool.invoicedprestations', 'unlink', [prestationsids])

prestationsids = models.execute_kw(db, uid, password, 'extraschool.invoice', 'search', [[]])
ids = models.execute_kw(db, uid, password, 'extraschool.invoice', 'unlink', [prestationsids])

rhisnesplaceid = models.execute_kw(db, uid, password, 'extraschool.place', 'search', [[['name','ilike','ECOLE COMMUNALE DE RHISNES']]])[0]
meuxplaceid = models.execute_kw(db, uid, password, 'extraschool.place', 'search', [[['name','ilike','ECOLE COMMUNALE DE MEUX']]])[0]

hugoid = models.execute_kw(db, uid, password, 'extraschool.child', 'search', [[['firstname','ilike','HUGO'],['lastname','ilike','IMBRECHTS']]])[0]
moaid = models.execute_kw(db, uid, password, 'extraschool.child', 'search', [[['firstname','ilike','MOA'],['lastname','ilike','IMBRECHTS']]])[0]
joachimid = models.execute_kw(db, uid, password, 'extraschool.child', 'search', [[['firstname','ilike','JOACHIM'],['lastname','ilike','IMBRECHTS']]])[0]
hannaid = models.execute_kw(db, uid, password, 'extraschool.child', 'search', [[['firstname','ilike','HANNA'],['lastname','ilike','IMBRECHTS']]])[0]
emmaid = models.execute_kw(db, uid, password, 'extraschool.child', 'search', [[['firstname','ilike','EMMA'],['lastname','ilike','ABE']]])[0]

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':7.25,
   'childid':hugoid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':7.25,
   'childid':emmaid,
   'placeid':rhisnesplaceid,
   'es':'E',
}])


pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':7.25,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':7.25,
   'childid':joachimid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':7.25,
   'childid':hannaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':17.50,
   'childid':hugoid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':17.50,
   'childid':emmaid,
   'placeid':rhisnesplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':17.50,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':17.50,
   'childid':joachimid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-01',
   'prestation_time':17.50,
   'childid':hannaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-02',
   'prestation_time':18.13,
   'childid':hugoid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-02',
   'prestation_time':18.13,
   'childid':emmaid,
   'placeid':rhisnesplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-02',
   'prestation_time':18.13,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-02',
   'prestation_time':18.13,
   'childid':joachimid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-02',
   'prestation_time':18.13,
   'childid':hannaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-03',
   'prestation_time':19,
   'childid':hugoid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-03',
   'prestation_time':19,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-03',
   'prestation_time':19,
   'childid':joachimid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-03',
   'prestation_time':19,
   'childid':hannaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-03',
   'prestation_time':19,
   'childid':emmaid,
   'placeid':rhisnesplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-04',
   'prestation_time':17.13,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-05',
   'prestation_time':17.13,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-05',
   'prestation_time':17.25,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-05',
   'prestation_time':17.5,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-08',
   'prestation_time':17.5,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-08',
   'prestation_time':18.25,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-09',
   'prestation_time':17.5,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-10',
   'prestation_time':7.5,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-11',
   'prestation_time':7.5,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-11',
   'prestation_time':8,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-12',
   'prestation_time':17,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-12',
   'prestation_time':18,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-16',
   'prestation_time':17,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-16',
   'prestation_time':18.25,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-17',
   'prestation_time':7,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-17',
   'prestation_time':9,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-15',
   'prestation_time':15,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-15',
   'prestation_time':18.25,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-18',
   'prestation_time':17.5,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'E',
}])

pricelistversionid = models.execute_kw(db, uid, password, 'extraschool.pdaprestationtimes', 'create', [{
   'activitycategoryid':1,
   'prestation_date':'2015-06-18',
   'prestation_time':18.25,
   'childid':moaid,
   'placeid':meuxplaceid,
   'es':'S',
}])
