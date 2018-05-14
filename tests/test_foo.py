##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2018
#    Jean-Michel Abe - Town of La Bruyere (<http://www.labruyere.be>)
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

import unittest
from odoorpc.odoo import tools
from openerp import common, tests

class TestModelA(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_lower(self):
        self.assertEqual('FOO'.lower(), 'foo')

# class TestModel(common.TransactionCase):
#
#     def

