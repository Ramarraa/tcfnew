from odoo import models, fields


class BrandTag(models.Model):
    _name = 'brand.tag'
    _description = 'Brand Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')
