from odoo import api, fields, models, _


class InsectSubSpecie(models.Model):
    _name = "insect.sub.specie"
    _description = "Insect Specie"

    name = fields.Char('Insect Sub Specie Name', required=True)
    specie_id = fields.Many2one('insect.specie', string='Specie', required=True)
    genus_id = fields.Many2one('insect.genus', string='Genus', required=True)
    tribe_id = fields.Many2one(string='Tribe', related='genus_id.tribe_id', readonly=True)
    sub_family_id = fields.Many2one(string='Sub Family', related='genus_id.sub_family_id', readonly=True)
    family_id = fields.Many2one(string='Family', related='sub_family_id.family_id', readonly=True)
    super_family_id = fields.Many2one(string='Super Family', related='family_id.super_family_id', readonly=True)