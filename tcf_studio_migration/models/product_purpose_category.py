from odoo import models, fields, api


class ProductPurposeCategory(models.Model):
    _name = 'product.purpose.category'
    _description = 'Product Purpose Category'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    image_128 = fields.Image(string='Image', max_width=128, max_height=128)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence', default=10)
    purpose_ids = fields.One2many('product.purpose', 'category_id', string='Purposes')
    purpose_count = fields.Integer(string='Purpose Count', compute='_compute_purpose_count')

    @api.depends('purpose_ids')
    def _compute_purpose_count(self):
        for record in self:
            record.purpose_count = len(record.purpose_ids)

    def action_view_purposes(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purposes',
            'res_model': 'product.purpose',
            'view_mode': 'list,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }
