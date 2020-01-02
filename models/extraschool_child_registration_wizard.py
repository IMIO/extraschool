# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia- Imio (<http://www.imio.be>).
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
import logging
_logger = logging.getLogger(__name__)


class extraschool_child_registration_validation_wizard(models.TransientModel):
    _name = 'extraschool.child_registration_validation_wizard'

    @api.multi
    def validate(self):
        registration_obj = self.env['extraschool.child_registration'].browse(self._context.get('active_ids'))
        logging.info("#Start Validation Registration.")
        count = 1
        for reg in registration_obj:
            logging.info("## Thread number: [{}/{}]".format(count, len(registration_obj)))
            if reg.activity_id:
                reg.validate()
            else:
                reg.validate_multi()
            count += 1
        logging.info("### End Validation Registration.")
        return True

    @api.multi
    def force_set_to_draft(self):

        for reg in self.env['extraschool.child_registration'].browse(self._context.get('active_ids')):
            reg.force_set_to_draft()

        return True

    @api.multi
    def check_doublons(self):
        cr,uid = self.env.cr, self.env.user.id

        update_extraschool_child_registration = """
                    update extraschool_child_registration cr
                    set error_duplicate_reg_line = True
                    where (select count(*) from ( select count(*)
                                    from extraschool_child_registration_line crl
                                    where child_registration_id = cr.id
                                    group by child_id
                                    having count(*) > 1
                                    ) zz ) > 0;
                        """
        cr.execute(update_extraschool_child_registration)

        update_extraschool_child_registration_line = """
            update extraschool_child_registration_line crl
            set error_duplicate_reg_line = True        
            where (select count(*)
                from extraschool_child_registration_line ccrl
                where ccrl.id != crl.id and ccrl.child_registration_id = crl.child_registration_id and ccrl.child_id = crl.child_id
                ) > 0
                """
        cr.execute(update_extraschool_child_registration_line)
