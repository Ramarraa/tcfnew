# -*- coding: utf-8 -*-

from odoo import models, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _compute_allowed_uom_ids(self):
        super()._compute_allowed_uom_ids()
        for line in self:
            line.allowed_uom_ids |= line.product_id.sale_uom_id | line.product_id.purchase_uom_id

    @api.depends("move_id.move_type")
    def _compute_product_uom_id(self):
        super()._compute_product_uom_id()
        for line in self:
            if line.move_id.is_sale_document(include_receipts=True) and line.product_id.sale_uom_id:
                line.product_uom_id = line.product_id.sale_uom_id
            elif line.move_id.is_purchase_document(include_receipts=True) and line.product_id.purchase_uom_id:
                line.product_uom_id = line.product_id.purchase_uom_id
