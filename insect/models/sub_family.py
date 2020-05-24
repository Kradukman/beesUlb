from odoo import api, fields, models, _


class InsectSubFamily(models.Model):
    _name = "insect.sub.family"
    _description = "Insect Sub Family"

    name = fields.Char('Name', required=True)
    family_id = fields.Many2one('insect.family', string='Family', required=True)
    super_family_id = fields.Many2one(string='Super Family', related='family_id.super_family_id', readonly=True)