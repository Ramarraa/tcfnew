# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    special_code = fields.Char(compute="get_sale_order_line_multiline_description_sale1", string="Special Code",
                               store=True, readonly=True)

    @api.depends('product_id')
    def get_sale_order_line_multiline_description_sale1(self):
        for move in self:
            if not move.product_id:
                return
            special_code = ""
            if move.sale_line_id and move.sale_line_id.special_code:
                special_code = move.sale_line_id.special_code
            else:
                if move.picking_id and move.picking_id.sale_id:
                    customerinfo = self.env['product.customerinfo'].search(
                        [('name', '=', move.picking_id.sale_id.partner_id.id),
                         ('product_id', '=', move.product_id.id),
                         ('product_tmpl_id', '=', move.product_id.product_tmpl_id.id)])
                    if customerinfo:
                        special_code = customerinfo.product_code

            move.special_code = special_code
