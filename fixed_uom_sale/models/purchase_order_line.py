# -*- coding: utf-8 -*-

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _compute_allowed_uom_ids(self):
        super()._compute_allowed_uom_ids()
        for line in self:
            line.allowed_uom_ids |= line.product_id.purchase_uom_id

    def _product_id_change(self):
        super()._product_id_change()
        if self.product_id.purchase_uom_id:
            self.product_uom_id = self.product_id.purchase_uom_id

    def _suggest_quantity(self):
        # runs after _product_id_change in onchange_product_id and may reset
        # the UoM from the vendor pricelist line - the product's fixed
        # Purchase UoM must win, like uom_po_id did in v16
        super()._suggest_quantity()
        if self.product_id.purchase_uom_id:
            self.product_uom_id = self.product_id.purchase_uom_id
