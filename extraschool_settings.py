from openerp import models, api, fields

class extraschool_settings(models.Model):
    _inherit = 'res.config.settings'
    _name = 'extraschool.onereport_settings'
    
    validity_from = fields.Date("Validity from")
    validity_to = fields.Date("Validity to")
    report_template = fields.Binary("Report template")
    one_logo = fields.Binary("ONE logo")
    
extraschool_settings()