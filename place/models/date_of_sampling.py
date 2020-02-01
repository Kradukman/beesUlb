from odoo import api, fields, models, _


class PlaceDateOfSampling(models.Model):
    _name = "place.date.of.sampling"
    _description = "Place Date Of Sampling"

    date = fields.Date('Date of sampling', required=True)
    weather_id = fields.Many2one('place.weather')
    min_temperature = fields.Integer('Minimum temperature')
    max_temperature = fields.Integer('Maximum temperature')