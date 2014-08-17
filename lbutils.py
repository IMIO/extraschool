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

def strcell(t,s):
    if t==1:
        return s.encode('utf-8')
    else:
        if t==2:
            return str(int(s)).strip()
        else:
            return ''

def strdate(s):
    res=''
    terms=s.split('-')
    if len(terms)==3:
        res=terms[2]+'/'+terms[1]+'/'+terms[0]
    return res

def genstreetcode(street):
    terms1 = (" DE LA "," DU "," DES "," D'"," DE L'"," DE "," ")    
    terms2 = ('RUE','BOULEVARD','BD','AVENUE','AV','CHAUSSEE','PLACE','CHEMIN','RUELLE','IMPASSE','ROUTE')
    try:
        streetcode = street.replace(u'é',u'e')
        streetcode = streetcode.replace(u'è',u'e')
        streetcode = streetcode.replace(u'à',u'a')
        streetcode = streetcode.replace(u'â',u'a')
        streetcode = streetcode.replace(u'ê',u'e')
        streetcode = streetcode.replace(u'î',u'i')
        streetcode = streetcode.replace(u'ï',u'i')
        streetcode = streetcode.replace(u'ô',u'o')
        streetcode = streetcode.replace(u'ç',u'c')
        streetcode = streetcode.upper()    
    except:
        streetcode = street.replace('é','e')
        streetcode = streetcode.replace('è','e')
        streetcode = streetcode.replace('à','a')
        streetcode = streetcode.replace('â','a')
        streetcode = streetcode.replace('ê','e')
        streetcode = streetcode.replace('î','i')
        streetcode = streetcode.replace('ï','i')
        streetcode = streetcode.replace('ô','o')
        streetcode = streetcode.replace('ç','c')
        streetcode = streetcode.upper()    
    for term2 in terms2:
        for term1 in terms1:
            streetcode = streetcode.replace(term2+term1,'')
    streetcode = streetcode.replace('ST ','')
    streetcode = streetcode.replace('SAINT ','')
    streetcode = streetcode.replace('ST-','')
    streetcode = streetcode.replace('SAINT-','')
    streetcode = streetcode.replace(',','')
    streetcode = streetcode.replace(' ','')
    streetcode = streetcode.replace('.','')
    streetcode = streetcode.replace("'","")
    streetcode = streetcode.replace('"','')
    streetcode = streetcode.replace('-','')
    streetcode = streetcode.replace('/','')
    return streetcode
