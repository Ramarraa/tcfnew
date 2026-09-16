from odoo import models, fields


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sales Order',
        ondelete='set null',
        readonly=True,
    )
