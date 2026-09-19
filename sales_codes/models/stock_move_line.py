# -*- coding: utf-8 -*-
from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    special_code = fields.Char(related="move_id.special_code", string="Special Code", store=True, readonly=True)
