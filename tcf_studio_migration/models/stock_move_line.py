from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    special_code = fields.Char(string='Special Code')
    special_code_1 = fields.Char(string='Special Code 1')
    special_code_2 = fields.Char(string='Special Code 2')
