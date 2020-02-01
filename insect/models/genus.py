from odoo import api, fields, models, _


class InsectGenus(models.Model):
    _name = "insect.genus"
    _description = "Insect Genus"

    name = fields.Char('Insect Genus Name', required=True)
    family_id = fields.Many2one('insect.family', string='Family', required=True)