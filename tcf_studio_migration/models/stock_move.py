from odoo import api, models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Odoo 19 renamed ``quantity_done`` to ``quantity``.  Keep the former
    # field available for migrated Studio/QWeb views, which live in the
    # database and therefore cannot all be updated from this repository.
    quantity_done = fields.Float(
        string='Quantity Done',
        related='quantity',
        readonly=True,
    )
    reserved_availability = fields.Float(
        string='Reserved Quantity',
        related='quantity',
        readonly=True,
    )

    special_code = fields.Char(compute='_compute_special_codes', store=False)
    special_code_1 = fields.Char(compute='_compute_special_codes', store=False)
    special_code_2 = fields.Char(compute='_compute_special_codes', store=False)

    @api.depends(
        'sale_line_id.special_code',
        'move_line_ids.special_code',
        'move_line_ids.special_code_1',
        'move_line_ids.special_code_2',
    )
    def _compute_special_codes(self):
        for move in self:
            line = move.move_line_ids[:1]
            move.special_code = (
                move.sale_line_id.special_code if move.sale_line_id
                else line.special_code if line else False
            )
            move.special_code_1 = line.special_code_1 if line else False
            move.special_code_2 = line.special_code_2 if line else False

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super()._prepare_move_line_vals(
            quantity=quantity, reserved_quant=reserved_quant,
        )
        if self.sale_line_id:
            vals['special_code'] = self.sale_line_id.special_code
        return vals
