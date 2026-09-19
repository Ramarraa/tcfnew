# -*- coding: utf-8 -*-


from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    special_name = fields.Char(string="Special Name", compute="get_sale_order_line_multiline_description_sale1", store=True)
    special_code = fields.Char(string="Special Code", compute="get_sale_order_line_multiline_description_sale1", store=True)

    @api.depends('product_id')
    def get_sale_order_line_multiline_description_sale1(self):
        for line in self:
            if not line.product_id:
                return
            special_code = ""
            special_name = ""
            customerinfo = self.env['product.customerinfo'].search(
                [('name', '=', line.order_id.partner_id.id),
                 ('product_id', '=', line.product_id.id),('product_tmpl_id', '=', line.product_id.product_tmpl_id.id)])
            if customerinfo :
                special_code = customerinfo.product_code
                special_name = customerinfo.product_name
            elif not customerinfo :
                code = str(line.order_id.partner_id.id)  +  str(line.product_id.id)
                customerinfo = customerinfo.create({
                    "name": line.order_id.partner_id.id,
                    "product_tmpl_id": line.product_id.product_tmpl_id.id,
                    "product_id": line.product_id.id,
                    "product_code": code,
                })
                custom_code = [customerinfo.product_id.custom_code]
                if code not in custom_code:
                    custom_code.append(code)
                line.product_id.custom_code = custom_code

                special_code = customerinfo.product_code
                special_name = customerinfo.product_name
            line.special_code = special_code
            line.special_name = special_name

