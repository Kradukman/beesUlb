from odoo import api, fields, models, _


class ULBProject(models.Model):
    _name = 'project_ulb.project'

    name = fields.Char('Project', required=True)
    year = fields.Date('Year', required=True)
    site_ids = fields.Many2many('place.place', 'Sites')
    leader_ids = fields.Many2many('res.partner', 'Leader', required=True)