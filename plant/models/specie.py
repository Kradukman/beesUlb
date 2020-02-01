from odoo import api, fields, models, _


class PlantSpecie(models.Model):
    _name = "plant.specie"
    _description = "Plant Specie"

    name = fields.Char('Plant Specie Name', required=True)
    genus_id = fields.Many2one('plant.genus', string='Genus', required=True)
    family_id = fields.Many2one(string='Family', related='genus_id.family_id', readonly=True)