from odoo import models, api, fields

class extraschool_main_settings(models.Model):
    _inherit = 'res.config.settings'
    _name = 'extraschool.main_settings'
    
    lastqrcodenbr = fields.Integer('lastqrcodenbr')


class extraschool_one_settings(models.Model):
    _inherit = 'res.config.settings'
    _name = 'extraschool.onereport_settings'
    
    validity_from = fields.Date("Validity from")
    validity_to = fields.Date("Validity to")
    report_template = fields.Binary("Report template")
    one_logo = fields.Binary("ONE logo")
    
