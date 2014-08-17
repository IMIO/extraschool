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
from openerp.osv import osv, fields

class extraschool_reminder(osv.osv):
    _name = 'extraschool.reminder'
    _description = 'Reminder'

    _columns = {
        'remindersjournalid' : fields.many2one('extraschool.remindersjournal', 'Reminders journal',ondelete='cascade', required=False),
        'parentid' : fields.many2one('extraschool.parent', 'Parent', required=False),
        'amount' : fields.float('Amount'),
        'structcom' : fields.char('Structured Communication', size=50),
        'schoolimplantationid' : fields.many2one('extraschool.schoolimplantation', 'School implantation', required=False),
        'concernedinvoices' : fields.many2many('extraschool.invoice','extraschool_reminder_invoice_rel', 'reminder_id', 'invoice_id','Concerned invoices'),
        'filename' : fields.char('filename', size=30,readonly=True),
        'reminder_file' : fields.binary('File', readonly=True),
        'activitycategoryid' : fields.related('remindersjournalid', 'activitycategoryid', type='many2one',relation="extraschool.activitycategory", string='Activity Category'),
        'term' : fields.related('remindersjournalid', 'term', type='date', string='Term'),
        'transmissiondate' : fields.related('remindersjournalid', 'transmissiondate', type='date', string='Transmission date'),  
    }
extraschool_reminder()
