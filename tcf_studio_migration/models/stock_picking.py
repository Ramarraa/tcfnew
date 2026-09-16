from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Odoo 19 replaced package levels with package history records.  Preserve
    # the former name for migrated Studio/QWeb reports; both record types
    # expose package_id, location_id, and location_dest_id.
    package_level_ids = fields.Many2many(
        comodel_name='stock.package.history',
        string='Package Levels',
        related='package_history_ids',
        readonly=True,
    )
    move_ids_without_package = fields.One2many(
        comodel_name='stock.move',
        inverse_name='picking_id',
        string='Stock Moves',
        related='move_ids',
        readonly=True,
    )
    move_line_ids_without_package = fields.One2many(
        comodel_name='stock.move.line',
        inverse_name='picking_id',
        string='Detailed Operations',
        related='move_line_ids',
        readonly=True,
    )
    has_packages = fields.Boolean(
        string='Has Packages',
        compute='_compute_has_packages_compatibility',
    )

    final_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Final Product',
        related='mrp_production_id.product_id',
        store=True,
        readonly=True,
    )
    final_product_qty = fields.Float(
        string='Final Product Quantity to Produce',
        related='mrp_production_id.product_qty',
        store=True,
        readonly=True,
    )
    lot_for_final_product_id = fields.Many2one(
        comodel_name='stock.lot',
        string='Lot for Final Product',
        compute='_compute_lot_for_final_product_id',
        store=True,
        readonly=True,
    )
    special_code_for_final_product = fields.Char(
        string='Special Code for Final Product',
        compute='_compute_special_code_for_final_product',
        store=True,
        readonly=True,
    )

    @api.depends('packages_count')
    def _compute_has_packages_compatibility(self):
        for picking in self:
            picking.has_packages = bool(picking.packages_count)

    @api.depends('mrp_production_id.lot_producing_ids')
    def _compute_lot_for_final_product_id(self):
        for picking in self:
            picking.lot_for_final_product_id = (
                picking.mrp_production_id.lot_producing_ids[:1]
            )

    @api.depends(
        'mrp_production_id.product_id',
        'mrp_production_id.sale_order_id.order_line.product_id',
        'mrp_production_id.sale_order_id.order_line.special_code',
    )
    def _compute_special_code_for_final_product(self):
        for picking in self:
            production = picking.mrp_production_id
            matching_lines = production.sale_order_id.order_line.filtered(
                lambda line: line.product_id == production.product_id
                and line.special_code
            )
            picking.special_code_for_final_product = (
                matching_lines[:1].special_code or False
            )
