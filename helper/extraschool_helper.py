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

from openerp import models, api
from datetime import date, datetime, timedelta as td
import time
import logging
_logger = logging.getLogger(__name__)


class extraschool_helper(models.Model):
    _name = "extraschool.helper"

    @api.multi
    def add_date_user(self, data):
        return "\n" + "[" + datetime.now().strftime('%d-%m-%Y') + "][" + self.env['res.users'].browse(
            self._context.get('uid')).name + "] " + data

    @staticmethod
    def str_to_date(date):
        return datetime.strptime(date, "%Y-%m-%d")

    @staticmethod
    def complete_year(start, end):
        """
        :param start: lowest year.
        :param end: highest year.
        :return: List with all years from start to end.
        """
        start= extraschool_helper.str_to_date(start).year
        end = extraschool_helper.str_to_date(end).year
        diff_year = end - start

        if diff_year == 1:
            return [start.year]
        else:
            year_list = []
            year_list.append(start)
            for i in range(diff_year):
                start += 1
                year_list.append(start)

        return year_list


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        logging.info('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te - ts))
        return result

    return timed
