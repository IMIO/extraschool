import xmlrpclib

url = 'http://localhost:8069'
db = 'testlb'
username = 'admin'
password = 'admin'
  
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))


uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

todeleteids = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'search', [[]])
ids = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'unlink', [todeleteids])

todeleteids = models.execute_kw(db, uid, password, 'extraschool.price_list', 'search', [[]])
ids = models.execute_kw(db, uid, password, 'extraschool.price_list', 'unlink', [todeleteids])

todeleteids = models.execute_kw(db, uid, password, 'extraschool.activityoccurrence', 'search', [[]])
ids = models.execute_kw(db, uid, password, 'extraschool.activityoccurrence', 'unlink', [todeleteids])

todeleteids = models.execute_kw(db, uid, password, 'extraschool.activity', 'search', [[]])
ids = models.execute_kw(db, uid, password, 'extraschool.activity', 'unlink', [todeleteids])

todeleteids = models.execute_kw(db, uid, password, 'extraschool.childposition', 'search', [[['id','>',10]]])
ids = models.execute_kw(db, uid, password, 'extraschool.childposition', 'unlink', [todeleteids])

placeids = models.execute_kw(db, uid, password, 'extraschool.place', 'search', [[]])

childtypeidaucun = models.execute_kw(db, uid, password, 'extraschool.childtype', 'search', [[['name','=','aucun']]])
childtypeidpers = models.execute_kw(db, uid, password, 'extraschool.childtype', 'search', [[['name','like','Personnel%']]])
priceliststandardid = models.execute_kw(db, uid, password, 'extraschool.price_list', 'create', [{
   'name':'Prix standard',
}])

pricelist18051815id = models.execute_kw(db, uid, password, 'extraschool.price_list', 'create', [{
   'name':'Prix 18h05 - 18h15',
}])

pricelist181523id = models.execute_kw(db, uid, password, 'extraschool.price_list', 'create', [{
   'name':'Prix 18h15 - 23h',
}])

pricelistgratuitid = models.execute_kw(db, uid, password, 'extraschool.price_list', 'create', [{
   'name':'Gratuit + de 2 enfants',
}])

pricelistpersid = models.execute_kw(db, uid, password, 'extraschool.price_list', 'create', [{
   'name':'Gratuit Personnel',
}])

childpositionids= models.execute_kw(db, uid, password, 'extraschool.childposition', 'search', [[['position','<',3]]])

pricelistversionstandardid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'create', [{
   'name':'Prix standard',
   'price_list_id':priceliststandardid,
   'validity_from':'2013-09-01',
   'validity_to':'2016-12-31',
   'child_position_ids':[[6,0,childpositionids]],
   'child_type_ids':[[6,0,childtypeidaucun]],
   'period_duration':1,
   'period_tolerance':0,
   'price':0.03,
}])

childpositionids= models.execute_kw(db, uid, password, 'extraschool.childposition', 'search', [[['position','>=',3]]])

pricelistversiongratuitid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'create', [{
   'name':'Gratuit + de 2 enfants',
   'price_list_id':pricelistgratuitid,
   'validity_from':'2013-09-01',
   'validity_to':'2016-12-31',
   'child_position_ids':[[6,0,childpositionids]],
   'child_type_ids':[[6,0,childtypeidaucun]],
   'period_duration':1,
   'period_tolerance':0,
   'price':0.0,
}])

childpositionids= models.execute_kw(db, uid, password, 'extraschool.childposition', 'search', [[]])

pricelistversionpersid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'create', [{
   'name':'Gratuit Personnel',
   'price_list_id':pricelistpersid,
   'validity_from':'2013-09-01',
   'validity_to':'2016-12-31',
   'child_position_ids':[[6,0,childpositionids]],
   'child_type_ids':[[6,0,childtypeidpers]],
   'period_duration':1,
   'period_tolerance':0,
   'price':0.0,
}])

childpositionids= models.execute_kw(db, uid, password, 'extraschool.childposition', 'search', [[]])

pricelistversion18051815id = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'create', [{
   'name':'18h05 - 18h15',
   'price_list_id':pricelist18051815id,
   'validity_from':'2013-09-01',
   'validity_to':'2016-12-31',
   'child_position_ids':[[6,0,childpositionids]],
   'child_type_ids':[[6,0,(childtypeidpers+childtypeidaucun)]],
   'period_duration':5,
   'period_tolerance':0,
   'price':5,
}])

childpositionids= models.execute_kw(db, uid, password, 'extraschool.childposition', 'search', [[]])

pricelistversion181523id = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'create', [{
   'name':'18h15 - 23h',
   'price_list_id':pricelist181523id,
   'validity_from':'2013-09-01',
   'validity_to':'2016-12-31',
   'child_position_ids':[[6,0,childpositionids]],
   'child_type_ids':[[6,0,(childtypeidpers+childtypeidaucun)]],
   'period_duration':285,
   'period_tolerance':0,
   'price':10,
}])

schoolimplantationids = models.execute_kw(db, uid, password, 'extraschool.schoolimplantation', 'search', [[['name','not ilike','%meux%']]])
placeids = models.execute_kw(db, uid, password, 'extraschool.place', 'search', [[['name','not ilike','%meux%']]])

activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie soir mercredi 12h",
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'SOIR',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '2',
    'leveltype': 'M,P',
    'prest_from': 12.17,
    'prest_to': 18.08,
    'default_from_to':'from',
    'subsidizedbyone':1,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversionstandardid], {
    'activity_ids': [[4,activityid,0]],
}]) 
plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversiongratuitid], {
    'activity_ids': [[4,activityid,0]],
}]) 
plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversionpersid], {
    'activity_ids': [[4,activityid,0]],
}]) 

activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie soir mercredi 12h 18h05 18h15",
    'parent_id': activityid,
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'SOIR',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '2',
    'leveltype': 'M,P',
    'prest_from': 18.08,
    'prest_to': 18.25,
    'default_from_to':'from',
    'subsidizedbyone':1,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversion18051815id], {
    'activity_ids': [[4,activityid,0]],
}]) 

activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie soir mercredi 12h 18h15 23h",
    'parent_id': activityid,
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'SOIR',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '2',
    'leveltype': 'M,P',
    'prest_from': 18.25,
    'prest_to': 23,
    'default_from_to':'from',
    'subsidizedbyone':1,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversion181523id], {
    'activity_ids': [[4,activityid,0]],
}]) 

schoolimplantationids = models.execute_kw(db, uid, password, 'extraschool.schoolimplantation', 'search', [[['name','ilike','%meux%']]])
placeids = models.execute_kw(db, uid, password, 'extraschool.place', 'search', [[['name','ilike','%meux%']]])

activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie soir mercredi 13h",
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'SOIR',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '2',
    'leveltype': 'M,P',
    'prest_from': 13,
    'prest_to': 18.08,
    'default_from_to':'from',
    'subsidizedbyone':1,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversionstandardid], {
    'activity_ids': [[4,activityid,0]],
}]) 
plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversiongratuitid], {
    'activity_ids': [[4,activityid,0]],
}]) 
plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversionpersid], {
    'activity_ids': [[4,activityid,0]],
}]) 

activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie soir mercredi 13h 18h05 18h15",
    'parent_id': activityid,
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'SOIR',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '2',
    'leveltype': 'M,P',
    'prest_from': 18.08,
    'prest_to': 18.25,
    'default_from_to':'from',
    'subsidizedbyone':1,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversion18051815id], {
    'activity_ids': [[4,activityid,0]],
}]) 

activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie soir mercredi 13h 18h15 23h",
    'price_list_id':pricelist181523id,
    'parent_id': activityid,
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'SOIR',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '2',
    'leveltype': 'M,P',
    'prest_from': 18.25,
    'prest_to': 23,
    'default_from_to':'from',
    'subsidizedbyone':1,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversion181523id], {
    'activity_ids': [[4,activityid,0]],
}]) 

schoolimplantationids = models.execute_kw(db, uid, password, 'extraschool.schoolimplantation', 'search', [[]])
placeids = models.execute_kw(db, uid, password, 'extraschool.place', 'search', [[]])

activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie matin",
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'MATIN',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '0,1,2,3,4',
    'leveltype': 'M,P',
    'prest_from': 6,
    'prest_to': 8.25,
    'default_from_to':'to',
    'subsidizedbyone':0,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversionstandardid], {
    'activity_ids': [[4,activityid,0]],
}]) 
plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversiongratuitid], {
    'activity_ids': [[4,activityid,0]],
}]) 
plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversionpersid], {
    'activity_ids': [[4,activityid,0]],
}]) 




activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie soir",
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'SOIR',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '0,1,3,4',
    'leveltype': 'M,P',
    'prest_from': 15.67,
    'prest_to': 18.08,
    'default_from_to':'from',
    'subsidizedbyone':1,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversionstandardid], {
    'activity_ids': [[4,activityid,0]],
}]) 
plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversiongratuitid], {
    'activity_ids': [[4,activityid,0]],
}]) 
plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversionpersid], {
    'activity_ids': [[4,activityid,0]],
}]) 

activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie soir 18h05 18h15",
    'parent_id': activityid,
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'SOIR',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '0,1,3,4',
    'leveltype': 'M,P',
    'prest_from': 18.08,
    'prest_to': 18.25,
    'default_from_to':'from',
    'subsidizedbyone':1,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversion18051815id], {
    'activity_ids': [[4,activityid,0]],
}]) 

activityid = models.execute_kw(db, uid, password, 'extraschool.activity', 'create', [{
    'name': "Garderie soir 18h15 23h",
    'parent_id': activityid,
    'validity_from':'2013-09-01',
    'validity_to':'2016-12-31',
    'category':1,
    'placeids':[[6,0,placeids]],
    'schoolimplantationids':[[6,0,schoolimplantationids]],
    'short_name':'SOIR',
    'childtype_ids': [[6,0,(childtypeidaucun+childtypeidpers)]],
    'days': '0,1,3,4',
    'leveltype': 'M,P',
    'prest_from': 18.25,
    'prest_to': 23,
    'default_from_to':'from',
    'subsidizedbyone':1,
}])

plvid = models.execute_kw(db, uid, password, 'extraschool.price_list_version', 'write',[[pricelistversion181523id], {
    'activity_ids': [[4,activityid,0]],
}]) 









