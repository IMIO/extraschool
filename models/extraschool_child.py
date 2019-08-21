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

from openerp import models, api, fields, _
from openerp.api import Environment
from datetime import date, datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning
import time
import timeit
import logging
_logger = logging.getLogger(__name__)


class extraschool_child(models.Model):
    _name = 'extraschool.child'
    _description = 'Child'
    _inherit = 'mail.thread'

    organising_power_id = fields.Many2one(
        'extraschool.organising_power',
        'Organising Power',
        track_visibility='onchange',
                                          )
    name = fields.Char(compute='_name_compute',string='FullName', search='_search_fullname', size=100)
    childtypeid = fields.Many2one('extraschool.childtype', 'Type',required=True, ondelete='restrict', help='Ce champs permet de définir si l\'enfant a le droit à un tarif préférentiel (ex: enfants du CPAS, enfants de la croix rouge, enfants des accueillantes,...)')
    rn = fields.Char('RN')
    firstname = fields.Char('FirstName', size=50, required=True, track_visibility='onchange')
    lastname = fields.Char('LastName', size=50 , required=True, track_visibility='onchange')
    schoolimplantation = fields.Many2one('extraschool.schoolimplantation', 'School implantation',required=True, track_visibility='onchange')
    levelid = fields.Many2one('extraschool.level', 'Level', required=True, track_visibility='onchange')
    classid = fields.Many2one('extraschool.class', 'Class', required=False, domain="[('schoolimplantation','=',schoolimplantation)]", track_visibility='onchange')
    parentid = fields.Many2one('extraschool.parent', 'Parent', required=True, ondelete='RESTRICT', select=True, track_visibility='onchange', domain="[('isdisabled', '=', False)]")
    birthdate = fields.Date('Birthdate', required=True, track_visibility='onchange')
    last_import_date = fields.Datetime('Import date', readonly=True)
    modified_since_last_import = fields.Boolean('Modified since last import')
    tagid = fields.Char('Tag ID', help='Numéro contenu dans le QR Code', track_visibility='onchange')
    otherref = fields.Char('Other ref', size=50, track_visibility='onchange')
    isdisabled = fields.Boolean('Disabled', track_visibility='onchange')
    comment = fields.Text('Comment', track_visibility='onchange')
    check_name = fields.Boolean(default=True)
    check_rn = fields.Boolean(default=True)
    health_sheet_ids = fields.One2many('extraschool.health_sheet', 'child_id')
    old_level_id = fields.Many2one('extraschool.level', 'Old Level')
    old_class_id = fields.Many2one('extraschool.class', 'Old Class')

    def get_age(self):
        date_of_birth = datetime.strptime(self.birthdate,'%Y-%m-%d')
        return datetime.today().year - date_of_birth.year - (
        (datetime.today().month, datetime.today().day) < (date_of_birth.month, date_of_birth.day))

    @api.multi
    def wizard_action(self):
        return {
            'name': 'Fusion d\'enfants',
            'domain': [],
            'res_model': 'extraschool.child_fusion_wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {},
            'target': 'new',
        }

    def _search_fullname(self, operator, value):
        return ['|',('firstname', operator, value),('lastname', operator, value)]


    @api.depends('firstname','lastname')
    def _name_compute(self):
        for record in self:
            record.name = '%s %s'  % (record.lastname, record.firstname)

    @api.onchange('firstname', 'lastname')
    @api.multi
    def _check_name(self):
        if self.search([('lastname', 'ilike', self.lastname), ('firstname', 'ilike', self.firstname)]):
            self.check_name = False
        else:
            self.check_name = True

    @api.onchange('rn')
    @api.multi
    def _check_rn(self):
        if self.rn and self.search([('rn', '=', self.rn)]):
            self.check_rn = False
        else:
            self.check_rn = True

    @api.one
    def action_gentagid(self):
        if not self.tagid :
            config = self.env['extraschool.mainsettings'].browse([1])
            self.tagid = config.lastqrcodenbr = config.lastqrcodenbr + 1

        # return long(self.tagid)
        return self.tagid

    @api.multi
    def write(self, vals):
        fields_to_find = set(['firstname',
                              'lastname'])

        if fields_to_find.intersection(set([k for k,v in vals.iteritems()])):
            vals['modified_since_last_import'] = True

        return super(extraschool_child,self).write(vals)

    @api.multi
    def get_presta(self):

        return {'name': 'Présences',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.prestation_times_of_the_day',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('child_id', '=',self.id),]
            }

    @api.multi
    def get_sante(self):

        return {'name': 'Fiche santé',
                'type': 'ir.actions.act_window',
                'res_model': 'extraschool.health_sheet',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'nodestroy': False,
                'target': 'current',
                'limit': 50000,
                'domain': [('child_id', '=', self.id), ],
                'context' : {'child_id': self.id},
                }

    @api.one
    def unlink(self):
        self.isdisabled = True

    @api.model
    def create(self, vals):
        vals[u'organising_power_id'] = self.env['extraschool.organising_power'].search([]).mapped('id')[0]

        return super(extraschool_child, self).create(vals)


##############################################################################
#
#    AESMobile
#    Copyright (C) 2018
#    Colicchia Michaël & Delaere Olivier - Imio (<http://www.imio.be>).
#
##############################################################################
    @api.multi
    def get_child_for_smartphone(self, smartphone_id):
        # Todo: Get newtag list.
        """

        :param smartphone_id: ID of the smartphone used to get place_id
        :return: Dictionnary of children {id: , nom: , prenom:, tagid:}
        """
        start_time = time.time()
        cr = self.env.cr


        # Get all the child corresponding to the smartphone's place_id
        sql_query = """
                    SELECT c.id, c.lastname, c.firstname, c.tagid
                    FROM extraschool_smartphone AS s
                    INNER JOIN extraschool_place_schoolimplantation_rel AS ps_rel
                    ON s.placeid = ps_rel.place_id
                    INNER JOIN extraschool_child AS c
                    ON c.schoolimplantation = ps_rel.schoolimplantation_id
                    WHERE s.id = %s AND c.isdisabled = False;
                    """

        cr.execute(sql_query, [smartphone_id])
        children_info = cr.dictfetchall()

        # Check if a child has a tagid or not. Otherwiser XMLRPC will crash. It can't be None.
        for child in children_info:
            if child['tagid'] == None:
                child['tagid'] = ''

        try:
            self.env['extraschool.smartphone_log'].create({ 'title': 'Fetching children',
                                                            'time_of_transmission': time.time() - start_time,
                                                            'smartphone_id': smartphone_id,
                                                            })
        except:
            logging.info("Error Sync on Children")
            return "Error Sync on Children"

        return children_info

    @staticmethod
    def get_children(cr, uid, smartphone_id, context=None):
        """
        :param cr, uid, context needed for a static method
        :param smartphone_id: Id of the smartphone that contact us.
        :return: Dictionnary of children {id: , nom: , prenom:, tagid:}
        """
        # Declare new Environment.
        env = api.Environment(cr, uid, context={})

        return extraschool_child.get_child_for_smartphone(env['extraschool.child'], smartphone_id)
