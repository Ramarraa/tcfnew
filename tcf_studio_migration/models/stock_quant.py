from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    special_code = fields.Char(string='Special Code')
