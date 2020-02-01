from odoo import api, fields, models, _


class PlantGenus(models.Model):
    _name = "plant.genus"
    _description = "Plant Genus"

    name = fields.Char('Plant Genus Name', required=True)
    family_id = fields.Many2one('plant.family', string='Family', required=True)