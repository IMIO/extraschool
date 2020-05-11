from openerp import models, api, fields, _


class extraschool_structured_communication(models.Model):
    _name = "extraschool.structured_communication"
    _description = 'Structured communication'

    digits = fields.Char(size=12)

    def get_formatted(self):
        return "+++{}/{}/{}+++".format(self[0:3], self[3:7], self[7:12])

    def get_prefix(self):
        return self.digits[0:3]
