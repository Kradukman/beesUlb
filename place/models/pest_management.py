from odoo import api, fields, models, _


class PlacePestManagement(models.Model):
    _name = "place.pest.management"
    _description = "Place Pest Management"

    name = fields.Char('Pest Management', required=True)