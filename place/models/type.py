from odoo import api, fields, models, _


class PlaceType(models.Model):
    _name = "place.type"
    _description = "Place Type"

    name = fields.Char('Name', required=True)