from odoo import api, fields, models, _


class PlaceCultivar(models.Model):
    _name = "place.cultivar"
    _description = "Place Cultivar"

    name = fields.Char('Name', required=True)