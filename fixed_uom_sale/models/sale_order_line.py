# -*- coding: utf-8 -*-

from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _compute_allowed_uom_ids(self):
        super()._compute_allowed_uom_ids()
        for line in self:
            line.allowed_uom_ids |= line.product_id.sale_uom_id | line.product_id.sale_samples_uom_id

    @api.depends("product_id", "order_id.order_type")
    def _compute_product_uom_id(self):
        super(SaleOrderLine, self)._compute_product_uom_id()

        for line in self:
            if not line.product_uom_id or (line.product_id.sale_uom_id.id != line.product_uom_id.id):
                line.product_uom_id = line.product_id.sale_uom_id

            if not line.product_uom_id or (
                    line.order_id.order_type == "samples" and line.product_id.sale_samples_uom_id.id != line.product_uom_id.id):
                line.product_uom_id = line.product_id.sale_samples_uom_id
