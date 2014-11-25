from openerp.report import report_sxw
import time

# Declaration d'un parser pour mon rapport
# On utilise le parser par defaut que l'on override
class parser_extraschool_coda_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(parser_extraschool_coda_report, self).__init__(cr, uid, name, context)

        # Definition du context local afin de rajouter la possibilite d'utiliser le module
        # time de python
        self.localcontext.update({
            'time': time,
            'get_about' : self.get_about,
        })

    def get_about(self):
        import xmlrpclib

        server = xmlrpclib.ServerProxy('http://tiny.my.odoo.com:8069/xmlrpc/common')
        return server.about()


# Creation d'une instance du parser personnalise pour l'objet training.session et le rapport
# training.session.report
report_sxw.report_sxw('report.extraschool.coda.report',
                      'extraschool.coda',
                      'addons/extraschool/report/coda_report.rml',
                      parser=parser_extraschool_coda_report)

