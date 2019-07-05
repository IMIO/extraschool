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

from odoo import models, api, fields
from odoo.api import Environment
from datetime import date, datetime
import time
import timeit
from odoo.exceptions import except_orm, Warning, RedirectWarning


class extraschool_health_sheet(models.Model):
    _name = 'extraschool.health_sheet'
    _description = 'Health sheet'

    def _get_child(self):
        return self._context.get('child_id')

    child_id = fields.Many2one('extraschool.child', string='Name', default=_get_child, required=True)
    comment = fields.Text(string='Comment')
    doctor_id = fields.Many2one('extraschool.doctor', string='Doctor', select=True)
    blood_type = fields.Selection(
        (('AB+','AB+'),
         ('AB-','AB-'),
         ('A+', 'A+'),
         ('A-', 'A-'),
         ('B+', 'B+'),
         ('B-', 'B-'),
         ('O+', 'O+'),
         ('O-', 'O-'),
         ('inconnu', 'Inconnu')), string='Blood type')
    tetanus = fields.Boolean(string='Tetanus', default=False)
    first_date_tetanus = fields.Date(string='First date tetanus')
    last_date_tetanus = fields.Date(string='Last date tetanus')
    contact_ids = fields.One2many('extraschool.other_contact', 'health_id', string='contact', )
    allergy = fields.Boolean(string='Allergy', default=False)
    allergy_ids = fields.Many2many('extraschool.allergy', 'extraschool_child_allergy_rel', 'child_id', 'allergy_id', 'Allergy list')
    handicap = fields.Boolean(string='Handicap', default=False)
    type_handicap = fields.Char(string='Type of handicap')
    specific_regime = fields.Boolean(string='Specific Regime', default=False)
    specific_regime_text = fields.Char(string='Type specific regime')
    activity_no_available = fields.Boolean(string='Activity no available', default=False)
    activity_no_available_text = fields.Char(string='Type of activity no available')
    disease_ids = fields.One2many('extraschool.disease','health_id', 'disease_id')
    facebook = fields.Selection(
        (('non_renseigne', 'Non renseigné'),
         ('non', 'Non'),
         ('oui', 'Oui')), default='non_renseigne', string='Facebook')
    photo = fields.Selection(
        (('non_renseigne', 'Non renseigné'),
         ('non', 'Non'),
         ('oui', 'Oui')), default='non_renseigne', string='Photo')
    swim = fields.Selection(
        (('non_renseigne', 'Non renseigné'),
         ('non', 'Non'),
         ('oui', 'Oui')), default='non_renseigne', string='Swim')
    swim_level = fields.Selection(
        (('tres_bien', 'Très bien'),
         ('bien', 'Bien'),
         ('moyen', 'Moyen'),
         ('difficilement', 'Difficilement'),
         ('pas_du_tout', 'Pas du tout'),
         ('non_renseigne', 'Non renseigné')), default='non_renseigne', string='Swim level')
    intervention = fields.Boolean(string='Intervention', default=False)
    intervention_text = fields.Char(string='Type of intervention')
    arnica = fields.Selection(
        (('non_renseigne', 'Non renseigné'),
         ('non', 'Non'),
         ('oui', 'Oui')), default='non_renseigne', string='Arnica')
    diabetique = fields.Boolean(string='Diabétique', default=False)
    interdiction_contact_ids = fields.One2many('extraschool.interdiction_other_contact', 'health_id', string='Interdiction contact', )

    @api.model
    def create(self, vals):
        if self.search([('child_id', '=', self._context.get('child_id'))]):
            raise Warning("Une fiche santé existe déjà pour cet enfant !")
        else:
            return super(extraschool_health_sheet,self).create(vals)

class extraschool_doctor(models.Model):
    _name = 'extraschool.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Doctor')
    doctor_contact = fields.Char(string='Tél. Doctor', size=20)
    doctor_gsm = fields.Char(string='Gsm Doctor', size=20)
    street = fields.Char('Street', size=50)
    zipcode = fields.Char('ZipCode', size=6)
    city = fields.Char('City', size=50)
    country_id = fields.Many2one('res.country', string='Country', default=21)
    comment = fields.Text(string='Comment')


class extraschool_other_contact(models.Model):
    _name = 'extraschool.other_contact'
    _description = 'Other contact'

    health_id = fields.Many2one('extraschool.health_sheet', string='Health sheet')
    contact_name = fields.Char(string='Contact name')
    contact_relation = fields.Char(string='Contact relation')
    contact_tel = fields.Char(string='Tél. contact', size=20)

class extraschool_interdiction_other_contact(models.Model):
    _name = 'extraschool.interdiction_other_contact'
    _description = 'Interdiction contact'

    health_id = fields.Many2one('extraschool.health_sheet', string='Health sheet')
    contact_name = fields.Char(string='Contact name')
    contact_relation = fields.Char(string='Contact relation')
    contact_tel = fields.Char(string='Tél. contact', size=20)

class extraschool_allergy(models.Model):
    _name = 'extraschool.allergy'
    _description = 'Allergy'

    name = fields.Char(string='Allergie')

class extraschool_disease(models.Model):
    _name = 'extraschool.disease'
    _description = 'Disease'

    health_id = fields.Many2one('extraschool.health_sheet', string='Health sheet')
    disease = fields.Many2one('extraschool.disease_type', string='Disease')
    disease_text = fields.Char(string='Treatment')

class extraschool_disease_type(models.Model):
    _name = 'extraschool.disease_type'
    _description = 'Type of disease'

    name = fields.Char(string='Disease')
