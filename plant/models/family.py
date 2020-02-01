from odoo import api, fields, models, _


class PlantFamily(models.Model):
    _name = "plant.family"
    _description = "Plant Family"

    name = fields.Char('Name', required=True)