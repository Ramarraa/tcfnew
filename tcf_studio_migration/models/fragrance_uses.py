from odoo import models, fields, api


class FragranceUses(models.Model):
    _name = 'fragrance.uses'
    _description = 'Fragrance Uses'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, translate=True, tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)
    product_count = fields.Integer(
        string='Product Count',
        compute='_compute_product_count',
    )

    @api.depends()
    def _compute_product_count(self):
        for record in self:
            record.product_count = self.env['product.template'].search_count([
                ('fragrance_use_id', '=', record.id)
            ])

    def action_view_products(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': [('fragrance_use_id', '=', self.id)],
            'context': {'default_fragrance_use_id': self.id},
        }
