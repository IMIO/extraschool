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

from openerp import models, api, fields, _
from openerp.api import Environment
from openerp.exceptions import except_orm, Warning, RedirectWarning

class extraschool_school(models.Model):
    _name = 'extraschool.school'
    _description = 'School'
    _inherti = 'mail.thread'

    name = fields.Char('Name', size=50, required=True, track_visibility=True)
    logo = fields.Binary()
    street = fields.Char('Street', size=50)
    zipcode = fields.Char('ZipCode', size=6)
    city = fields.Char('City', size=50)
    schoolimplantations = fields.One2many('extraschool.schoolimplantation', 'schoolid','schoolimplantations', required=True, track_visibility=True)
    oldid = fields.Integer('oldid')                

    @api.model
    def create(self,vals):
        # Override to check if they can create a new school.
        # AES should not be counted as school.
        schools_count = len(self.env['extraschool.school'].search([]).filtered(lambda r: r.name != 'AES'))
        max_school = self.env['extraschool.activitycategory'].search([])[0].max_school_implantation


        if schools_count >= max_school:
            self.send_mail()
            self.env['email.template'].browse()
            raise Warning(_("You have reached the maximum school"))

        return super(extraschool_school, self).create(vals)

    @api.multi
    def send_mail(self):
        import smtplib

        server = smtplib.SMTP('mailrelay.imio.be', 25)
        server.starttls()

        message = "%s a essayé de créer une école supplémentaire alors qu'ils sont à la limite autorisée" % (self.env[
            'extraschool.activitycategory'].search([])[0].po_name.encode("utf-8"))

        server.sendmail("aes@imio.be", "support-aes@imio.be", message)

        server.quit()

extraschool_school()
