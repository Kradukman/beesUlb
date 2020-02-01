from odoo import api, fields, models, _


class InsectFamily(models.Model):
    _name = "insect.family"
    _description = "Insect Family"

    name = fields.Char('Name', required=True)