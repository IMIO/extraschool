# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (c) 2012-TODAY OpenERP S.A. <http://openerp.com>
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

from openerp import tools
from openerp.tests import common
from openerp import api

class T_005_Test_ExtraSchool_PrestationCheck(common.TransactionCase):

    def setUp(self):
        """*****setUp*****"""
        super(T_005_Test_ExtraSchool_PrestationCheck, self).setUp()

        self.prestationscheck_wizard = self.registry('extraschool.prestationscheck_wizard')
        self.prestationscheck_wizard_rs = self.env['extraschool.prestationscheck_wizard']
        self.place = self.registry('extraschool.place')
        self.activity = self.registry('extraschool.activity')
        self.activityoccurrence = self.env['extraschool.activityoccurrence']
        self.activitycategory = self.registry('extraschool.activitycategory')
        self.prestationtimes = self.registry('extraschool.prestationtimes')
        self.prestationtimes_rs = self.env['extraschool.prestationtimes']
        
        self.invoice_wizard = self.registry('extraschool.invoice_wizard')
        self.schoolimplantation = self.registry('extraschool.schoolimplantation')       
        
#
#    presta std matin 
#        - mercredi 1/1/2014 
#        - enfant std 1
#
#    Vérif :
#        - ajout de la presta manquante
#        
    def test_00_test_fct(self):
        print "test_00_test_fct"        
        cr, uid = self.cr, self.uid
        form = {'placeid': self.place.search(cr,uid,[('name','in',['Ecole du parc'])]),
                'period_from': '2014-01-01',
                'period_to': '2014-01-01',
                'activitycategory': self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])]),
                'state': 'init',
                'currentdate': False,
                }
        return_value = self.prestationscheck_wizard._check(cr, uid,form)
        
        #check return
        self.assertEqual(return_value['state'],'end_of_verification')
        #check ajout de la presta manquante
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-01'),
                                                     ('es','=','S'),
                                                     ('manualy_encoded','=',False),
                                                     ('verified','=',True),
                                                     ('prestation_time','=',8.5), 
                                                     ('activityid.name','=','Garderie Standard Matin'), 
                                                                                                                                                             
                                                     ])
        self.assertEqual(len(presta),1,'check ajout de la presta manquante')
        #check verified field is true
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-01'),
                                                     ('verified','=',True), 
#                                                     ('activityid.name','=','Garderie Standard Matin'),
                                                     ])
        self.assertEqual(len(presta),2,'check verified field is true')

        ids = self.prestationtimes.search(cr,uid,[])
        
#
#    presta std matin 
#        - mercredi 2/1/2014 
#        - enfant std 1
#
#    Vérif :
#        - ajout de la presta manquante
#        
    def test_01_test_fct(self):
        print "test_01_test_fct"
        cr, uid = self.cr, self.uid

        self.prestationscheck_wizard_rs = self.prestationscheck_wizard_rs.with_context(tz='Europe/Brussels').create({})
        self.prestationscheck_wizard_rs.placeid = self.place.search(cr,uid,[('name','in',['Ecole du parc'])])
        self.prestationscheck_wizard_rs.period_from = '2014-01-02'
        self.prestationscheck_wizard_rs.period_to = '2014-01-02'
        self.prestationscheck_wizard_rs.activitycategory = self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])])
        self.prestationscheck_wizard_rs.state = 'init'
        self.prestationscheck_wizard_rs.currentdate = False
        
        return_value = self.prestationscheck_wizard_rs.with_context(tz='Europe/Brussels')._check() 
        
        #check PAS ajout de la presta manquante
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-02'),
                                                                                                                    
                                                     ])
        self.assertEqual(len(presta),1,'check 1 présence')
        #check verified field is False
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-02'),
#                                                     ('verified','=',True), 
#                                                     ('activityid.name','=','Garderie Standard Matin'),
                                                     ])
#!!! to uncomment when verified is handled        self.assertEqual(len(presta),0,'check verified field is False')      
    test_01_test_fct.prestacheck = 1
    test_01_test_fct.check_wizard = 1         
#
#    Triple activité  
#        - mercredi 3/1/2014 
#        - enfant std 1
#
#    Vérif :
#        - ajout des presta manquante
#        
    def test_02_test_fct(self):
        print "test_02_test_fct"
        cr, uid = self.cr, self.uid

        self.prestationscheck_wizard_rs = self.prestationscheck_wizard_rs.with_context(tz='Europe/Brussels').create({})
        self.prestationscheck_wizard_rs.placeid = self.place.search(cr,uid,[('name','in',['Ecole du parc'])])
        self.prestationscheck_wizard_rs.period_from = '2014-01-03'
        self.prestationscheck_wizard_rs.period_to = '2014-01-03'
        self.prestationscheck_wizard_rs.activitycategory = self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])])
        self.prestationscheck_wizard_rs.state = 'init'
        self.prestationscheck_wizard_rs.currentdate = False
        
        return_value = self.prestationscheck_wizard_rs.with_context(tz='Europe/Brussels')._check()  
        
        #check ajout de la presta manquante
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-03'),   
                                                     ('es','=','E'),
                                                     ('manualy_encoded','=',False),
#                                                     ('verified','=',True),
                                                     ('prestation_time','=',16), 
#                                                     ('activityid.name','=','Garderie Standard Soir'),                                                                                                                                                
                                                     ])
        self.assertEqual(len(presta),1,'check 1 présences ajoutée')
        #check verified field is False
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-03'),
#                                                     ('verified','=',True), 
#                                                     ('activityid.name','=','Garderie Standard Matin'),
                                                     ])
#!!! to uncomment when verified is handled        self.assertEqual(len(presta),2,'check verified field is True')  
    test_02_test_fct.prestacheck = 1
    test_02_test_fct.check_wizard = 1  
              
#
#    activité pédagogique  
#        - lundi 6/1/2014 
#        - enfant std 1
#
#    Vérif :
#        - ajout des presta manquante + remplacement des activité std
#        
    def test_03_test_fct(self):
        print "test_03_test_fct"
        cr, uid = self.cr, self.uid
     
        self.prestationscheck_wizard_rs = self.prestationscheck_wizard_rs.with_context(tz='Europe/Brussels').create({})
        self.prestationscheck_wizard_rs.placeid = self.place.search(cr,uid,[('name','in',['Ecole du parc'])])
        self.prestationscheck_wizard_rs.period_from = '2014-01-06'
        self.prestationscheck_wizard_rs.period_to = '2014-01-06'
        self.prestationscheck_wizard_rs.activitycategory = self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])])
        self.prestationscheck_wizard_rs.state = 'init'
        self.prestationscheck_wizard_rs.currentdate = False
        
        return_value = self.prestationscheck_wizard_rs.with_context(tz='Europe/Brussels')._check()        
        
        #check return
        self.assertEqual(return_value['state'],'end_of_verification','Pas d''erreur trouvée')
        #check ajout de la presta d entrée
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-06'),   
                                                     ('es','=','E'),
                                                     ('manualy_encoded','=',False),
                                                     ('verified','=',True),
                                                     ('prestation_time','=',7.5), 
#                                                     ('activityid.name','=','Garderie Standard Soir'),                                                                                                                                                
                                                     ])
        self.assertEqual(len(presta),1,u'check 1 présences corrigée')
        #check ajout de la presta de sortie
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-06'),   
                                                     ('es','=','S'),
                                                     ('manualy_encoded','=',False),
                                                     ('verified','=',True),
                                                     ('prestation_time','=',18), 
#                                                     ('activityid.name','=','Garderie Standard Soir'),                                                                                                                                                
                                                     ])
        self.assertEqual(len(presta),1,u'check 1 présences ajoutée')
        #check verified field is False
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-06'),
                                                     ('verified','=',True), 
#                                                     ('activityid.name','=','Garderie Standard Matin'),
                                                     ])
        self.assertEqual(len(presta),2,'check verified field is True')   
             
    test_03_test_fct.prestacheck = 1
    test_03_test_fct.check_wizard = 1   
#
#    activité bricolage  
#        - lundi 8/1/2014 
#        - enfant std 1 inscri auto
#        - enfant std 2 inscri garderie mais pas brico
#
#    Vérif :
#        - ajout des presta manquante + remplacement des activité std
#        
    def test_04_test_fct(self):
        print "test_04_test_fct"
        cr, uid = self.cr, self.uid
        
        self.prestationscheck_wizard_rs = self.prestationscheck_wizard_rs.with_context(tz='Europe/Brussels').create({})
        self.prestationscheck_wizard_rs.placeid = self.place.search(cr,uid,[('name','in',['Ecole du parc'])])
        self.prestationscheck_wizard_rs.period_from = '2014-01-08'
        self.prestationscheck_wizard_rs.period_to = '2014-01-08'
        self.prestationscheck_wizard_rs.activitycategory = self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])])
        self.prestationscheck_wizard_rs.state = 'init'
        self.prestationscheck_wizard_rs.currentdate = False
        
        return_value = self.prestationscheck_wizard_rs.with_context(tz='Europe/Brussels')._check()
        
        #check return
        self.assertEqual(return_value['state'],'end_of_verification','Pas d''erreur trouvée')
        #check ajout de la presta d entrée
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 3'),
                                                     ('prestation_date','=','2014-01-08'),   
                                                     ('es','=','E'),
                                                     ('manualy_encoded','=',False),
                                                     ('verified','=',True),
                                                     ('prestation_time','=',12), 
#                                                     ('activityid.name','=','Garderie Standard Soir'),                                                                                                                                                
                                                     ])
        self.assertEqual(len(presta),1,u'check 1 présences ajoutée')

    test_04_test_fct.prestacheck = 1
    test_04_test_fct.check_wizard = 1
    

    def test_05_test_fct(self):
        print "test_00_get_prestation_activityid"        
        
        presta = self.prestationtimes_rs.search([('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-03'),   
                                                     ('es','=','E'),
                                                     ('prestation_time','=',7.45), 
                                                     ])        
        return_val = self.prestationscheck_wizard_rs.get_prestation_activityid(presta[0])
        print str(return_val)
        occurrence_rs = self.activityoccurrence.browse([return_val['occurrence_id']])
        #check return
        self.assertEqual(occurrence_rs[0].activityid.id,2,'Activity not selected')
        
    test_05_test_fct.prestacheck = 1
    test_05_test_fct.get_prestation_activityid = 1
        

    def test_10_test_fct(self):
        print "test_10_get_prestation_activityid_multi_result"        
        
        presta = self.prestationtimes_rs.search([('childid.name','=','enfant std 3'),
                                                     ('prestation_date','=','2014-02-05'),   
                                                     ('es','=','E'),
                                                     ('prestation_time','=',14), 
                                                     ])        
        return_val = self.prestationscheck_wizard_rs.get_prestation_activityid(presta[0])
        print str(return_val)
        occurrence_rs = self.activityoccurrence.browse([return_val['occurrence_id']])
        #check return
        self.assertEqual(occurrence_rs[0].activityid.id,8,'Activity not selected')
        
    test_10_test_fct.prestacheck = 1
    test_10_test_fct.get_prestation_activityid = 1

    def test_15_test_fct(self):
        print "test_15_get_prestation_activityid_NO_result"        
        
        presta = self.prestationtimes_rs.search([('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-02'),   
                                                     ('es','=','S'),
                                                     ('prestation_time','=',9), 
                                                     ])        
        print "-----"
        print presta
        print "-----"
        return_val = self.prestationscheck_wizard_rs.get_prestation_activityid(presta[0])
        print str(return_val)
        #check return
        self.assertEqual(return_val['return_code'],0,'Activity found !!!')
        self.assertEqual(return_val['error_msg'],"No matching occurrence found",'Activity found !!!')
        
    test_15_test_fct.prestacheck = 1
    test_15_test_fct.get_prestation_activityid = 1

    def test_20_test_fct(self):
        print "test_20_get_prestation_activityid_pas_inscrit_bricolage"        
        
        presta = self.prestationtimes_rs.search([('childid.name','=','enfant PC 1'),
                                                     ('prestation_date','=','2014-02-05'),   
                                                     ('es','=','S'),
                                                     ('prestation_time','=',14), 
                                                     ])        
        print "-----"
        print presta
        print "-----"
        return_val = self.prestationscheck_wizard_rs.get_prestation_activityid(presta[0])
        print str(return_val)
        occurrence_rs = self.activityoccurrence.browse([return_val['occurrence_id']])
        #check return
        self.assertEqual(return_val['return_code'],1,'Activity not found !!!')
        self.assertEqual(occurrence_rs[0].activityid.id,7,'Activity not selected')
        
    test_20_test_fct.prestacheck = 1
    test_20_test_fct.get_prestation_activityid = 1

#     #
#     #
#     #   !!!!!!!!!!!!!!!!!!!!!!!!!   Must be The LAST One !!!!!!!!!!!!!!!!!!!!!!!
#     #
#     #    
#     def test_9999_test_fct(self):
#         print "test_9999_test_fct"
#         cr, uid = self.cr, self.uid
#         form = {'placeid': self.place.search(cr,uid,[('name','in',['Ecole du parc'])]),
#                 'period_from': '2014-01-01',
#                 'period_to': '2099-12-31',
#                 'activitycategory': self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])]),
#                 'state': 'init',
#                 'currentdate': False,
#                 }
#         return_value = self.prestationscheck_wizard._check(cr, uid,form)
#         
#         #check return
#         self.assertEqual(return_value['state'],'end_of_verification','Ca devrait etre OK')
    
        
