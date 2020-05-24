from odoo import api, fields, models, _


class InsectSuperFamily(models.Model):
    _name = "insect.super.family"
    _description = "Insect Super Family"

    name = fields.Char('Name', required=True)