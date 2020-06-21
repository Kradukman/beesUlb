from odoo import api, fields, models, _

class InsectFamily(models.Model):
    _name = "insect.family"
    _description = "Insect Family"

    name = fields.Char('Name', required=True)
    position = fields.Char('Position')
    super_family_id = fields.Many2one('insect.super.family', string='Super Family', required=True)