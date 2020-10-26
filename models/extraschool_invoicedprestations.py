# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia & Jenny Pans & François Burniaux - Imio (<http://www.imio.be>).
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
import openerp.addons.decimal_precision as dp
import math


class extraschool_invoicedprestations(models.Model):
    _name = 'extraschool.invoicedprestations'
    _description = 'invoiced Prestations'

    invoiceid = fields.Many2one(comodel_name='extraschool.invoice', string='invoice', ondelete='cascade', index=True)
    childid = fields.Many2one(comodel_name='extraschool.child', string='Child', required=False, index=True)
    child_position_id = fields.Many2one(comodel_name='extraschool.childposition', string='Child position',
                                        required=False, index=True)
    placeid = fields.Many2one(related='activity_occurrence_id.place_id', store=True, index=True)
    prestation_date = fields.Date(related='activity_occurrence_id.occurrence_date', store=True, index=True)
    activity_occurrence_id = fields.Many2one(
        comodel_name='extraschool.activityoccurrence',
        string='Activity occurrence',
        required=False,
        index=True,
        ondelete='restrict')
    activity_activity_id = fields.Many2one(
        related="activity_occurrence_id.activityid",
        store=True,
        index=True)
    # use for hide button
    on_tax_certificate = fields.Boolean()
    description = fields.Char('Description')
    date_no_value = fields.Date(
        string='Date of no value',
        track_visibility='onchange',
    )
    duration = fields.Integer('Duration')
    quantity = fields.Integer('Quantity')
    period_duration = fields.Integer('Period Duration')
    period_tolerance = fields.Integer('Period Tolerance')
    unit_price = fields.Float(
        'Price',
        digits_compute=dp.get_precision('extraschool_invoice_line')
    )
    total_price = fields.Float(
        'Price',
        digits_compute=dp.get_precision('extraschool_invoice_line')
    )
    discount = fields.Boolean('Discount')
    discount_value = fields.Float(
        'Discount value',
        digits_compute=dp.get_precision('extraschool_invoice_line'),
        default=0
    )
    price_list_version_id = fields.Many2one(
        comodel_name='extraschool.price_list_version',
        ondelete='restrict'
    )
    prestation_ids = fields.One2many(
        comodel_name='extraschool.prestationtimes',
        inverse_name='invoiced_prestation_id',
        ondelete='restrict'
    )

    # bug with the big sql request (no no value)
    no_value_amount = fields.Float(default=0.0)
    no_value_date = fields.Date()
    no_value_description = fields.Text()

    def float_time_to_str(self, float_val):
        factor = float_val < 0 and -1 or 1
        val = abs(float_val)
        return "%02d:%02d" % (factor * int(math.floor(val)), int(round((val % 1) * 60)))

    def get_child_entry(self):
        presta_obj = self.env['extraschool.prestationtimes']
        # get child presta
        presta_ids = presta_obj.search([("childid", "=", self.childid.id),
                                        ("activity_occurrence_id.activityid.short_name", "=",
                                         self.activity_occurrence_id.activityid.short_name),
                                        ("prestation_date", "=", self.prestation_date),
                                        ("es", "=", "E")
                                        ])
        if presta_ids:
            # sort on time
            presta_ids = presta_ids.sorted(key=lambda r: r.prestation_time)
            return self.float_time_to_str(presta_ids[0].prestation_time)
        else:
            return False

    def get_child_exit(self):
        # get child presta
        # wdb voir présence
        presta_obj = self.env['extraschool.prestationtimes']
        presta_ids = presta_obj.search([("childid", "=", self.childid.id),
                                        ("activity_occurrence_id.activityid.short_name", "=",
                                         self.activity_occurrence_id.activityid.short_name),
                                        ("prestation_date", "=", self.prestation_date),
                                        ("es", "=", "S")
                                        ])
        if presta_ids:
            # sort on time
            presta_ids = presta_ids.sorted(key=lambda r: r.prestation_time, reverse=True)
            return self.float_time_to_str(presta_ids[0].prestation_time)
        else:
            return False

    def get_child_entry_performance(self):
        return self.float_time_to_str(self.prestation_ids.filtered(lambda r: r.es == 'E'))

    def get_child_exit_performance(self):
        return self.float_time_to_str(self.prestation_ids.filtered(lambda r: r.es == 'S').prestation_time)

    @api.multi
    def write(self, vals):

        if 'no_value_amount' in vals and vals.get('no_value_amount') > self.total_price:
            vals['no_value_amount'] = 0.00

        return super(extraschool_invoicedprestations, self).write(vals)
