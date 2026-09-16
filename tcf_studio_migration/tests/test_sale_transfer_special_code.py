from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSaleTransferSpecialCode(TransactionCase):
    def test_confirmation_copies_codes_through_three_step_delivery(self):
        warehouse = self.env['stock.warehouse'].create({
            'name': 'Special Code Warehouse', 'code': 'SCTST',
            'delivery_steps': 'pick_pack_ship',
        })
        customer = self.env['res.partner'].create({'name': 'Special Code Customer'})
        product = self.env['product.product'].create({
            'name': 'Special Code Product', 'is_storable': True,
        })
        self.env['stock.quant']._update_available_quantity(
            product, warehouse.lot_stock_id, 10,
        )
        order = self.env['sale.order'].create({
            'partner_id': customer.id, 'warehouse_id': warehouse.id,
            'order_line': [(0, 0, {
                'product_id': product.id, 'product_uom_qty': 1,
                'price_unit': 10, 'special_code': code,
            }) for code in ('SALE-A', 'SALE-B', False)],
        })
        order.action_confirm()
        self.assertEqual(len(order.picking_ids), 3)
        for picking in order.picking_ids:
            self.assertEqual(len(picking.move_ids), 3)
            for move in picking.move_ids:
                expected = move.sale_line_id.special_code
                self.assertEqual(move.special_code, expected)
                vals = move._prepare_move_line_vals(quantity=1)
                self.assertEqual(vals['special_code'], expected)
                detail = self.env['stock.move.line'].create(vals)
                self.assertEqual(detail.special_code, expected)
        for detail in order.picking_ids.move_line_ids:
            self.assertEqual(detail.special_code, detail.move_id.sale_line_id.special_code)
