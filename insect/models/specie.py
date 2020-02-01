from odoo import api, fields, models, _


class InsectSpecie(models.Model):
    _name = "insect.specie"
    _description = "Insect Specie"

    name = fields.Char('Insect Specie Name', required=True)
    genus_id = fields.Many2one('insect.genus', string='Genus', required=True)
    family_id = fields.Many2one(string='Family', related='genus_id.family_id', readonly=True)