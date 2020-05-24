from odoo import api, fields, models, _


class InsectGenus(models.Model):
    _name = "insect.genus"
    _description = "Insect Genus"

    name = fields.Char('Insect Genus Name', required=True)
    sub_family_id = fields.Many2one('insect.sub.family', string='Sub Family', required=True)
    family_id = fields.Many2one(string='Family', related='sub_family_id.family_id', readonly=True)
    super_family_id = fields.Many2one(string='Super Family', related='family_id.super_family_id', readonly=True)
    tribe_id = fields.Many2one('insect.tribe', string='Tribe')