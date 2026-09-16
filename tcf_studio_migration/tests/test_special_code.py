from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSpecialCode(TransactionCase):
    def test_customer_code_reaches_stock_move_without_circular_source(self):
        partner = self.env['res.partner'].create({'name': 'Code test customer'})
        product = self.env['product.product'].create({'name': 'Code test product'})
        order = self.env['sale.order'].new({'partner_id': partner.id})
        line = self.env['sale.order.line'].new({
            'order_id': order.id, 'product_id': product.id,
            'special_code': 'TCF-CODE-REGRESSION',
        })
        self.assertEqual(line.special_code, 'TCF-CODE-REGRESSION')
        move = self.env['stock.move'].new({
            'product_id': product.id, 'sale_line_id': line.id,
        })
        detail = self.env['stock.move.line'].new({'move_id': move.id})
        self.assertEqual(move.special_code, line.special_code)
        self.assertEqual(detail.special_code, line.special_code)
        line.special_code = 'TCF-CODE-UPDATED'
        self.assertEqual(move.special_code, 'TCF-CODE-UPDATED')
        self.assertEqual(detail.special_code, 'TCF-CODE-UPDATED')
        move.sale_line_id = False
        self.assertFalse(move.special_code)
        self.assertFalse(detail.special_code)
