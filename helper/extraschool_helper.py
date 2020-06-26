# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
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
import re

from dateutil.relativedelta import relativedelta
from openerp import models, api

from datetime import datetime, date

import time
import logging

_logger = logging.getLogger(__name__)


class extraschool_helper(models.Model):
    _name = "extraschool.helper"

    @api.multi
    def add_date_user(self, data):
        return "\n" + "[" + datetime.now().strftime('%d-%m-%Y') + "][" + self.env['res.users'].browse(
            self._context.get('uid')).name + "] " + data


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        logging.info('%r (%r, %r) %2.2f sec' % \
                     (method.__name__, args, kw, te - ts))
        return result

    return timed


def email_validation(email):
    """
    Verify if email is valid
    :param email: email
    :return: True if valid, False otherwise
    """
    return re.match('^[a-zA-Z0-9.+_%-]+@[a-zA-Z0-9._%-]+\\.[a-zA-Z]{2,6}$', email) is not None


def rn_validation(rn):
    """
    Verify if RN is valid
    :param rn: National registration number
    :return: True if valid, False otherwise
    """
    return re.match('^[0-9]{11}$', rn) is not None


def calculate_age(date_of_birth):
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


def calculate_birthdate_from_age(age_group):
    """
    Take an age_group (for exemple, 10 à 12 ans), split it and calculate birthdate for 10,12
    and return a list [date_from, date_to]
    """
    splitted_age_group = age_group.split(' ')
    today_date = datetime.now()
    date_from = today_date - relativedelta(years=int(splitted_age_group[2]))
    date_to = today_date - relativedelta(years=int(splitted_age_group[0]))
    return [date_from, date_to]


def split_list(alist, wanted_parts=1):

    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts] for i in range(wanted_parts)]
