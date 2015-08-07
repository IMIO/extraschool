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
import pdb
from openerp.osv import osv

class extraschool_report_hack(osv.Model):
    _inherit = 'report'
    
    def _build_wkhtmltopdf_args(self, paperformat, specific_paperformat_args=None):
        print "!!!!!!!!!!!!!!!Report Hack!!!!!!!!!!!!!!!!!!!"
        """Hack the parent fct to remove dpi arg from the return value."""
        res = super(extraschool_report_hack,self)._build_wkhtmltopdf_args(paperformat, specific_paperformat_args)
        if '--dpi' in res:
            i = res.index('--dpi')
            del res[i] #delete --dpi key
            del res[i] #delete --dpi value
            
#        pdb.set_trace()
        return res