# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


from odoo.tools import float_compare

_logger = logging.getLogger(__name__)




class CustomerInfo(models.Model):
    _name = "product.customerinfo"
    _description = "Customer Pricelist"
    _order = 'sequence, min_qty desc, price'

    name = fields.Many2one(
        'res.partner', 'Customer',
        ondelete='cascade', required=True,
        help="Customer of this product", check_company=True)
    product_name = fields.Char(
        'Customer Product Name',
        help="This Customer's product name will be used when printing a request for quotation. Keep empty to use the internal one.")
    product_code = fields.Char(
        'Customer Product Code',
        help="This Customer's product code will be used when printing a request for quotation. Keep empty to use the internal one.")
    sequence = fields.Integer(
        'Sequence', default=1, help="Assigns the priority to the list of product Customer.")
    product_tmpl_id = fields.Many2one(
    'product.template', 'Product Template', check_company=True,
    index=True,required=True, ondelete='cascade')
    product_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        related='product_tmpl_id.uom_id',
        help="This comes from the product form.")
    min_qty = fields.Float(
        'Quantity', default=0.0, required=True, digits="Product Unit Of Measure",
        help="The quantity to purchase from this Customer to benefit from the price, expressed in the Customer Product Unit of Measure if not any, in the default unit of measure of the product otherwise.")
    price = fields.Float(
        'Price', default=0.0, digits='Product Price',
        required=True, help="The price to purchase a product")
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company.id, index=1)
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True)
    date_start = fields.Date('Start Date', help="Start date for this Customer price")
    date_end = fields.Date('End Date', help="End date for this Customer price")
    product_id = fields.Many2one(
        'product.product', 'Product Variant', check_company=True,required=True,
        help="If not set, the Customer price will apply to all variants of this product.")
    product_variant_count = fields.Integer('Variant Count', related='product_tmpl_id.product_variant_count')
    delay = fields.Integer(
        'Delivery Lead Time', default=1, required=True,
        help="Lead time in days between the confirmation of the purchase order and the receipt of the products in your warehouse. Used by the scheduler for automatic computation of the purchase order planning.")


    @api.constrains('product_code')
    def _check_product_code(self):
        for rec in self:
            if self.search_count([("product_code", "=", rec.product_code), ("id", "!=", rec.id)]) != 0:
                raise ValidationError(_("Product Code must be unique"))







class ProductTemplate(models.Model):
    _inherit = 'product.template'
    custom_code = fields.Char(copy=False, readonly=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'


    custom_code = fields.Char(copy=False, readonly=True)



    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        search = super(ProductProduct, self)._name_search(name, args, operator, limit, name_get_uid)
        if not search:
            search = self._search(expression.AND([[('custom_code', operator, name)], args]), limit=limit, access_rights_uid=name_get_uid)
        return search


