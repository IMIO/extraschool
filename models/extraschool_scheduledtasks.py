# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia - Imio (<http://www.imio.be>).
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

from openerp import models, api, fields
from openerp.api import Environment
from datetime import datetime
from datetime import date
import re

class extraschool_scheduledtasks(models.Model):
    _name = 'extraschool.scheduledtasks'
    _description = 'Scheduled tasks'
    

    def transmissionreport(self, cr, uid, context=None):
        mail_mail = self.pool.get('mail.mail')
        obj_config = self.pool.get('extraschool.mainsettings')
        config=obj_config.read(cr, uid, [1],['emailfornotifications'])[0]   
        cr.execute("select * from extraschool_smartphone where to_char(current_date,'YYYY-MM-DD') <> to_char(lasttransmissiondate,'YYYY-MM-DD')")
        notransmissions=cr.dictfetchall()
        transmissionerror = False
        emailtxt = ''
        if len(notransmissions) > 0:
            transmissionerror = True
            for notransmission in notransmissions:
                emailtxt = emailtxt+ 'Pas de transmissions pour le smartphone '+str(notransmission['id'])+'\n'
            emailtxt = emailtxt+'\n'
        cr.execute("select id,maxtimedelta,oldversion,write_date,lasttransmissiondate,EXTRACT(HOUR FROM write_date) as hwrite,EXTRACT(MINUTE FROM write_date) as mwrite,EXTRACT(HOUR FROM lasttransmissiondate) as htransmission,EXTRACT(MINUTE FROM lasttransmissiondate) as mtransmission from extraschool_smartphone")
        smartphones = cr.dictfetchall()
        for smartphone in smartphones:
            if smartphone['htransmission']:
                hwrite = (smartphone['hwrite'] * 60)+smartphone['mwrite']
                htransmission = (smartphone['htransmission'] * 60)+smartphone['mtransmission']
                deltaminutes = int(abs(htransmission - hwrite))
                if smartphone['oldversion']:
                    deltaminutes = deltaminutes - 60
                if deltaminutes > smartphone['maxtimedelta']:
                    transmissionerror = True
                    emailtxt = emailtxt + 'smartphone '+str(smartphone['id'])+': ecart de '+str(deltaminutes)+' minutes avec le serveur \nHeure serveur: '+smartphone['write_date']+' - Heure smartphone: '+smartphone['lasttransmissiondate']+'\n'
                    emailtxt = emailtxt + '---------------------------------------------------------------------------------\n'
        if transmissionerror:
            emailsubject = 'GARDERIES: ATTENTION!!! ERREURS!!! Rapport de transmission du '+date.today().strftime('%d/%m/%Y')
            emailtxt = '\nATTENTION!!! ERREURS!!!:\n\n' + emailtxt
        else:
            emailsubject = 'Rapport de transmission du '+date.today().strftime('%d/%m/%Y')
        emailtxt = emailtxt + '\n\nTransmissions de ce jour ('+date.today().strftime('%d/%m/%Y')+'):\n--------------------------------------\n\n'
        cr.execute('select count(*) as number,extraschool_place.name as placename from extraschool_pdaprestationtimes left join extraschool_place on placeid = extraschool_place.id where prestation_date = %s group by extraschool_place.name',(date.today().strftime('%Y-%m-%d'),)) 
        prestations = cr.dictfetchall()
        for prestation in prestations:
            emailtxt = emailtxt + prestation['placename']+': '+str(prestation['number'])+' pointage(s)\n'
        emails = str(config['emailfornotifications']).split(';')
        for email in emails:
            email = email.strip()
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:                    
                mail_id = mail_mail.create(cr, uid, {
                    'email_from': email,
                    'email_to': email,
                    'subject': emailsubject,
                    'body_html': '<pre>%s</pre>' % emailtxt}, context=context)
                mail_mail.send(cr, uid, [mail_id], context=context)
                mail_mail.unlink(cr, uid, [mail_id])

extraschool_scheduledtasks()
