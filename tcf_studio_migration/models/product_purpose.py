from odoo import models, fields, api


class ProductPurpose(models.Model):
    _name = 'product.purpose'
    _description = 'Product Purpose'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color')
    image_128 = fields.Image(string='Image', max_width=128, max_height=128)
    category_id = fields.Many2one(
        comodel_name='product.purpose.category',
        string='Category',
        ondelete='set null',
    )
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence', default=10)
    product_count = fields.Integer(
        string='Product Count',
        compute='_compute_product_count',
    )

    @api.depends()
    def _compute_product_count(self):
        for record in self:
            record.product_count = self.env['product.template'].search_count([
                ('purpose_ids', 'in', [record.id])
            ])
