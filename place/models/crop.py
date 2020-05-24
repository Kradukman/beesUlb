from odoo import api, fields, models, _


class PlaceCrop(models.Model):
    _name = "place.crop"
    _description = "Place Crop"

    name = fields.Char('Name', required=True)