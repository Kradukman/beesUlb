from odoo import api, fields, models, _


class TrapTrap(models.Model):
    _name = "trap.trap"
    _description = "Trap Trap"

    name = fields.Char('Name', required=True)