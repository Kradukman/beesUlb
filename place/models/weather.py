from odoo import api, fields, models, _


class PlaceWeather(models.Model):
    _name = "place.weather"
    _description = "Place weather"

    name = fields.Char('Weather', required=True)