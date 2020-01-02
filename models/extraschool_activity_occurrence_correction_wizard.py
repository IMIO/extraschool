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

from odoo import models, api, fields, _
from datetime import date, datetime, timedelta as td
from odoo.exceptions import except_orm, Warning


class extraschool_activity_occurrence_correction_wizard(models.TransientModel):
    _name = 'extraschool.activity_occurrence_correction_wizard'

    date_to = fields.Date('Date to')
    place_ids = fields.Many2many('extraschool.place','extraschool_place_activity_wizard_rel', 'place_id', 'wizard_id','School implantations')

    @api.multi
    def change_place(self):
        place_list = []

        for place in self.place_ids:
            place_list.append(place.id)

        vals = { 'placeids': [[6, _, place_list]],
                 'multi_write': True,
                 }

        for activity in self.env['extraschool.activity'].browse(self._context.get('active_ids')):
            activity.check_validity_from_invoice(activity.id)
            activity.write(vals)

    @api.multi
    def reset_populate(self):
        return_val = {
                        'validity_to': -1,
                        'validity_from': -1,
                    }
        if self.date_to > datetime.now().strftime("%Y-%m-%d"):
            for activity in self.env['extraschool.activity'].browse(self._context.get('active_ids')):
                return_val['validity_to'] = self.date_to
                return_val['validity_from'] = self.check_last_invoice(activity)
                activity.write(return_val)
        else:
            raise Warning(_("The date must be higher than today"))

    def check_last_invoice(self,activity):
        cr = self.env.cr
        invoiced_obj = self.env['extraschool.invoicedprestations']
        # If there is an invoiced prestation for the activity.
        return_val = activity.validity_from
        if (invoiced_obj.search(
                [('activity_occurrence_id.activityid', '=', activity.id)])):
            # Get the date of the last invoice for this activity.
            cr.execute("SELECT prestation_date FROM extraschool_invoicedprestations WHERE activity_activity_id = %s ORDER BY prestation_date DESC LIMIT 1" % (activity.id))
            date_last_invoice = cr.fetchone()
            date_last_invoice = fields.Date.from_string(date_last_invoice[0]) + td(days=1)
            date_last_invoice = date_last_invoice.strftime('%Y-%m-%d')

            if activity.validity_from < date_last_invoice:
                return_val = date_last_invoice

        return return_val
