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

class T_005_Test_ExtraSchool_PrestationCheck(common.TransactionCase):

    def setUp(self):
        """*****setUp*****"""
        super(T_005_Test_ExtraSchool_PrestationCheck, self).setUp()
        cr, uid = self.cr, self.uid

        self.prestationscheck_wizard = self.registry('extraschool.prestationscheck_wizard')
        self.place = self.registry('extraschool.place')
        self.activity = self.registry('extraschool.activity')
        self.activitycategory = self.registry('extraschool.activitycategory')
        self.prestationtimes = self.registry('extraschool.prestationtimes')
        
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
                                                     ('ES','=','S'),
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
        form = {'placeid': self.place.search(cr,uid,[('name','in',['Ecole du parc'])]),
                'period_from': '2014-01-02',
                'period_to': '2014-01-02',
                'activitycategory': self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])]),
                'state': 'init',
                'currentdate': False,
                }
        return_value = self.prestationscheck_wizard._check(cr, uid,form)
        
        #check return
        self.assertNotEqual(return_value['state'],'end_of_verification','Pas d''erreur trouvée')
        #check PAS ajout de la presta manquante
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-02'),
                                                                                                                    
                                                     ])
        self.assertEqual(len(presta),1,'check 1 présence')
        #check verified field is False
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-02'),
                                                     ('verified','=',True), 
#                                                     ('activityid.name','=','Garderie Standard Matin'),
                                                     ])
        self.assertEqual(len(presta),0,'check verified field is False')      
        
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
        form = {'placeid': self.place.search(cr,uid,[('name','in',['Ecole du parc'])]),
                'period_from': '2014-01-03',
                'period_to': '2014-01-03',
                'activitycategory': self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])]),
                'state': 'init',
                'currentdate': False,
                }
        return_value = self.prestationscheck_wizard._check(cr, uid,form)
        
        #check return
        self.assertEqual(return_value['state'],'end_of_verification','Pas d''erreur trouvée')
        #check ajout de la presta manquante
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-03'),   
                                                     ('ES','=','E'),
                                                     ('manualy_encoded','=',False),
                                                     ('verified','=',True),
                                                     ('prestation_time','=',16), 
#                                                     ('activityid.name','=','Garderie Standard Soir'),                                                                                                                                                
                                                     ])
        self.assertEqual(len(presta),1,'check 1 présences ajoutée')
        #check verified field is False
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-03'),
                                                     ('verified','=',True), 
#                                                     ('activityid.name','=','Garderie Standard Matin'),
                                                     ])
        self.assertEqual(len(presta),2,'check verified field is True')        
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
        form = {'placeid': self.place.search(cr,uid,[('name','in',['Ecole du parc'])]),
                'period_from': '2014-01-06',
                'period_to': '2014-01-06',
                'activitycategory': self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])]),
                'state': 'init',
                'currentdate': False,
                }
        return_value = self.prestationscheck_wizard._check(cr, uid,form)
        
        #check return
        self.assertEqual(return_value['state'],'end_of_verification','Pas d''erreur trouvée')
        #check ajout de la presta d entrée
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-06'),   
                                                     ('ES','=','E'),
                                                     ('manualy_encoded','=',False),
                                                     ('verified','=',True),
                                                     ('prestation_time','=',7.5), 
#                                                     ('activityid.name','=','Garderie Standard Soir'),                                                                                                                                                
                                                     ])
        self.assertEqual(len(presta),1,u'check 1 présences corrigée')
        #check ajout de la presta de sortie
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 1'),
                                                     ('prestation_date','=','2014-01-06'),   
                                                     ('ES','=','S'),
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
        form = {'placeid': self.place.search(cr,uid,[('name','in',['Ecole du parc'])]),
                'period_from': '2014-01-08',
                'period_to': '2014-01-08',
                'activitycategory': self.activitycategory.search(cr,uid,[('name','in',['Garderies byparent'])]),
                'state': 'init',
                'currentdate': False,
                }
        return_value = self.prestationscheck_wizard._check(cr, uid,form)
        
        #check return
        self.assertEqual(return_value['state'],'end_of_verification','Pas d''erreur trouvée')
        #check ajout de la presta d entrée
        presta = self.prestationtimes.search(cr,uid,[('childid.name','=','enfant std 3'),
                                                     ('prestation_date','=','2014-01-08'),   
                                                     ('ES','=','E'),
                                                     ('manualy_encoded','=',False),
                                                     ('verified','=',True),
                                                     ('prestation_time','=',12), 
#                                                     ('activityid.name','=','Garderie Standard Soir'),                                                                                                                                                
                                                     ])
        self.assertEqual(len(presta),1,u'check 1 présences ajoutée')

    def test_05_test_fct(self):
        print "test_00_get_prestation_activityid"        
        cr, uid = self.cr, self.uid
        
        
        act_id = self.prestationscheck_wizard.get_prestation_activityid(cr,uid,self.prestationtimes.browse(cr,uid,3))
        print str(act_id)
        
        #check return
        self.assertEqual(act_id,[2],'Activity not selected')

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
    
        
