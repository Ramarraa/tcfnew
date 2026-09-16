from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    special_code = fields.Char(string='Special Code')
    alternative_code = fields.Char(
        related='product_id.product_tmpl_id.alternative_code',
        string='Alternative Code',
        readonly=True,
    )
