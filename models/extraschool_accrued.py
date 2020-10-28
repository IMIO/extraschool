# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2020
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia & Jenny Pans - Imio (<http://www.imio.be>).
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


class extraschoolAccrued(models.Model):
    _name = 'extraschool.accrued'
    _description = 'Droit constatés'

    biller_id = fields.Many2one(comodel_name="extraschool.biller", string="Biller")
    activity_category_id = fields.Many2one(comodel_name="extraschool.activitycategory", string="Activity category")
    amount = fields.Float(string="Amount")
    ref = fields.Char(string="Ref categ")
    amount_received = fields.Float(compute="_compute_amount_received", string="Amount received", store=True)

    @api.multi
    @api.depends("biller_id.balance")
    def _compute_amount_received(self):
        cr = self.env.cr
        for rec in self:
            if rec.biller_id and rec.activity_category_id:
                cr.execute(
                            """
                            SELECT COALESCE(SUM(ip.total_price),0) + COALESCE(SUM(ip.discount_value),0) - COALESCE(SUM(ip.no_value_amount),0) AS "amount_received"
                            FROM extraschool_invoicedprestations ip
                            LEFT JOIN extraschool_invoice i
                                ON ip.invoiceid = i.id
                            LEFT JOIN extraschool_activity a
                                ON a.id = ip.activity_activity_id
                            LEFT JOIN extraschool_activitycategory ac
                                ON a.category_id = ac.id
                            WHERE ac.id = '%s'  AND i.balance = 0 AND i.amount_received > 0 AND i.biller_id = '%s'
                            """ % (rec.activity_category_id.id, rec.biller_id.id)
                         )
                rec.amount_received = cr.dictfetchall()[0].get("amount_received")
