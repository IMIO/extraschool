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
import lbutils

class extraschool_parent(osv.osv):
    _name = 'extraschool.parent'
    _description = 'Parent'
    def _name_compute(self, cr, uid, ids, fieldname, other, context=None):

        res = dict.fromkeys(ids, '')

        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = str(obj.lastname).encode('utf-8')+' '+str(obj.firstname).encode('utf-8')

        return res
    def onchange_name(self, cr, uid, ids, lastname,firstname):        
        v={}        
        if lastname:
            if firstname:
                v['name']='%s %s' % (lastname, firstname)
            else:
                v['name']=lastname
        return {'value':v}
        
    def onchange_address(self, cr, uid, ids, street,city):        
        v={}        
        if street:
            if city:
                v['streetcode']=lbutils.genstreetcode(street+city)
            else:
                v['streetcode']=lbutils.genstreetcode(street)
        return {'value':v}
    
    def return_action_to_open(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current parent """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'extraschool', context['xml_id'], context=context)
            res['context'] = context
            res['domain'] = [('parentid','=', ids[0])]
            return res
        return False
    
    def _compute_totalinvoiced (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            cr.execute('select sum(amount_total) from extraschool_invoice where parentid=%s',(record.id,))
            to_return[record.id] = cr.fetchall()[0][0]
        return to_return
        
    def _compute_totalreceived (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            cr.execute('select sum(amount_received) from extraschool_invoice where parentid=%s',(record.id,))
            to_return[record.id] = cr.fetchall()[0][0]
        return to_return

    def _compute_totalbalance (self, cr, uid, ids, field_name, arg, context):
        to_return={}
        for record in self.browse(cr, uid, ids):
            cr.execute('select sum(balance) from extraschool_invoice where parentid=%s',(record.id,))
            to_return[record.id] = cr.fetchall()[0][0]
        return to_return
    
    _columns = {        
        'name' : fields.char('FullName', size=100),        
        'firstname' : fields.char('FirstName', size=50,required=True),
        'lastname' : fields.char('LastName', size=50,required=True),        
        'street' : fields.char('Street', size=50,required=True),
        'zipcode' : fields.char('ZipCode', size=6,required=True),
        'city' : fields.char('City', size=50,required=True),
        'housephone' : fields.char('House Phone', size=20),
        'workphone' : fields.char('Work Phone', size=20),
        'gsm' : fields.char('GSM', size=20),
        'email' : fields.char('Email', size=100),
        'invoicesendmethod' : fields.selection((('emailandmail','By mail and email'),('onlyemail','Only by email'),('onlybymail','Only by mail')),'Invoice send method',required=True),
        'streetcode': fields.char('Street code', size=50),
        'child_ids' : fields.one2many('extraschool.child', 'parentid','childs'),
        'invoice_ids' : fields.one2many('extraschool.invoice', 'parentid','invoices'),
        'remindersendmethod' : fields.selection((('emailandmail','By mail and email'),('onlyemail','Only by email'),('onlybymail','Only by mail')),'Reminder send method',required=True),
        'reminder_ids' : fields.one2many('extraschool.reminder', 'parentid','reminders'),
        'totalinvoiced' : fields.function(_compute_totalinvoiced, method=True, type="float", string="Total invoiced"),
        'totalreceived' : fields.function(_compute_totalreceived, method=True, type="float", string="Total received"),
        'totalbalance' : fields.function(_compute_totalbalance, method=True, type="float", string="Total balance"),
        'oldid' : fields.integer('oldid'),                
    }
    
    _defaults = {
        'invoicesendmethod' : lambda *a: 'emailandmail',
        'remindersendmethod' : lambda *a: 'emailandmail',
    }
    
    def create(self, cr, uid, vals, *args, **kw):
        
        parent_obj = self.pool.get('extraschool.parent')
        parent_ids=parent_obj.search(cr, uid, [('firstname', 'ilike', vals['firstname'].strip()),('lastname', 'ilike', vals['lastname'].strip()),('streetcode', 'ilike', vals['streetcode'])])
        if len(parent_ids) >0:
            raise osv.except_osv('Erreur','Ce parent a deja ete encode !!!')
        return super(extraschool_parent, self).create(cr, uid, vals)
    
    def unlink(self, cr, uid, ids, context=None):
        child_obj = self.pool.get('extraschool.child')
        childs_ids=child_obj.search(cr, uid, [('parentid', '=', ids[0])])
        if len(childs_ids) >0:
            raise osv.except_osv('Error', 'You can not delete a parent with childs.')
            return False
        return super(extraschool_parent, self).unlink(cr, uid, ids)
extraschool_parent()
