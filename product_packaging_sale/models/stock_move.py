from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends("sale_line_id.packaging_uom_id")
    def _compute_packaging_uom_id(self):
        super()._compute_packaging_uom_id()
        for move in self:
            # Sales keeps packaging separate from the quantity's unit of measure.
            # Retain the standard fallback for lines without selected packaging.
            if move.sale_line_id.packaging_uom_id:
                move.packaging_uom_id = move.sale_line_id.packaging_uom_id

    @api.depends(
        "sale_line_id.packaging_qty", "sale_line_id.product_uom_qty",
        "sale_line_id.product_uom_id", "sale_line_id.product_uom_id.factor",
        "product_uom", "product_uom.factor",
    )
    def _compute_packaging_uom_qty(self):
        super()._compute_packaging_uom_qty()
        for move in self:
            line = move.sale_line_id
            # Scale the line's packaging_qty by this move's own product_uom_qty
            # (rather than converting through the packaging UoM's factor) so a
            # split move or backorder gets a proportional packaging_uom_qty
            # instead of the full line value, and migrated packaging UoMs with
            # a stale `factor` field can't produce a wrong quantity here.
            if (
                line.packaging_uom_id
                and move.packaging_uom_id == line.packaging_uom_id
                and line.product_uom_qty
            ):
                quantity_in_sale_uom = move.product_uom._compute_quantity(
                    move.product_uom_qty, line.product_uom_id, round=False,
                )
                move.packaging_uom_qty = (
                    quantity_in_sale_uom * line.packaging_qty / line.product_uom_qty
                )
