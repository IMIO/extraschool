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

from openerp import models, api, fields
from openerp.api import Environment
import lbutils

class extraschool_parent(models.Model):
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
    
    def _compute_totalinvoiced (self):
        cr = self.env.cr
        for record in self:
            cr.execute('select sum(amount_total) from extraschool_invoice where parentid=%s',(record.id,))
            record.totalinvoiced = cr.fetchall()[0][0]
        
        
    def _compute_totalreceived (self):
        cr = self.env.cr
        for record in self:
            cr.execute('select sum(amount_received) from extraschool_invoice where parentid=%s',(record.id,))
            record.totalreceived = cr.fetchall()[0][0]

    def _compute_totalbalance (self):
        cr = self.env.cr
        for record in self:
            cr.execute('select sum(balance) from extraschool_invoice where parentid=%s',(record.id,))
            record.totalbalance = cr.fetchall()[0][0]
        
    name = fields.Char('FullName', size=100)        
    firstname = fields.Char('FirstName', size=50,required=True)
    lastname = fields.Char('LastName', size=50,required=True)        
    street = fields.Char('Street', size=50,required=True)
    zipcode = fields.Char('ZipCode', size=6,required=True)
    city = fields.Char('City', size=50,required=True)
    housephone = fields.Char('House Phone', size=20)
    workphone = fields.Char('Work Phone', size=20)
    gsm = fields.Char('GSM', size=20)
    email = fields.Char('Email', size=100)
    invoicesendmethod = fields.Selection((('emailandmail','By mail and email'),
                                          ('onlyemail','Only by email'),
                                          ('onlybymail','Only by mail')),
                                         'Invoice send method',required=True, default='emailandmail')
    streetcode = fields.Char('Street code', size=50)
    child_ids = fields.One2many('extraschool.child', 'parentid','childs')
    invoice_ids = fields.One2many('extraschool.invoice', 'parentid','invoices')
    remindersendmethod = fields.Selection((('emailandmail','By mail and email'),
                                           ('onlyemail','Only by email'),
                                           ('onlybymail','Only by mail')),
                                          'Reminder send method',required=True, default='emailandmail')
    one_subvention_type = fields.Selection((('sf','operating grants'),
                                            ('sdp','positive differentiation grants')),
                                            required=True, default='sf')
    reminder_ids = fields.One2many('extraschool.reminder', 'parentid','reminders')
    totalinvoiced = fields.Float(compute='_compute_totalinvoiced', string="Total invoiced")
    totalreceived = fields.Float(compute='_compute_totalreceived', string="Total received")
    totalbalance = fields.Float(compute='_compute_totalbalance', string="Total balance")
    oldid = fields.Integer('oldid')                
    
    @api.model        
    def create(self, vals):
        #to do replace check par une contraite
        parent_obj = self.env['extraschool.parent']
        parents=parent_obj.search([('firstname', 'ilike', vals['firstname'].strip()),
                                      ('lastname', 'ilike', vals['lastname'].strip()),
                                      ('streetcode', 'ilike', vals['streetcode'])])
        
        if len(parents) >0:
            raise Warning('Ce parent a deja ete encode !!!')
        
        return super(extraschool_parent, self).create(vals)
    

extraschool_parent()
