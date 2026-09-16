from odoo import Command
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPackagingDelivery(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({
            "name": "Packaging Delivery Customer",
        })
        cls.sold_product = cls.env["product.product"].create({
            "name": "Delivered Product",
            "is_storable": True,
            "list_price": 100.0,
        })
        cls.packaging_product_a = cls.env["product.product"].create({
            "name": "Packaging Product A",
            "is_storable": True,
        })
        cls.packaging_product_b = cls.env["product.product"].create({
            "name": "Packaging Product B",
            "is_storable": True,
        })
        cls.packaging_uom_a = cls.env.ref("uom.product_uom_dozen").copy({
            "name": "Packaging A",
            "packaging_product_id": cls.packaging_product_a.id,
        })
        cls.packaging_uom_b = cls.packaging_uom_a.copy({
            "name": "Packaging B",
            "packaging_product_id": cls.packaging_product_b.id,
        })
        cls.sold_product.product_tmpl_id.uom_ids = [
            Command.link(cls.packaging_uom_a.id),
            Command.link(cls.packaging_uom_b.id),
        ]

    def _new_order(self):
        return self.env["sale.order"].create({
            "partner_id": self.partner.id,
        })

    def _add_line(self, order, packaging=False, packaging_qty=0.0, quantity=1.0):
        return self.env["sale.order.line"].create({
            "order_id": order.id,
            "product_id": self.sold_product.id,
            "product_uom_id": self.sold_product.uom_id.id,
            "product_uom_qty": quantity,
            "packaging_uom_id": packaging.id if packaging else False,
            "packaging_qty": packaging_qty,
        })

    def test_no_packaging_does_not_create_packaging_picking(self):
        order = self._new_order()
        self._add_line(order)
        order.action_confirm()
        self.assertFalse(order.picking_packaging_ids)
        self.assertEqual(order.delivery_packaging_count, 0)

    def test_sale_packaging_reaches_all_delivery_steps(self):
        warehouse = self.env["stock.warehouse"].create({
            "name": "Packaging Transfer Test", "code": "PKTST",
            "delivery_steps": "pick_pack_ship",
        })
        order = self._new_order()
        order.warehouse_id = warehouse
        lines = (
            self._add_line(order, self.packaging_uom_a, 2, quantity=24)
            | self._add_line(order, self.packaging_uom_b, 3, quantity=36)
            | self._add_line(order, quantity=5)
        )
        order.action_confirm()
        pickings = order.picking_ids.filtered(
            lambda picking: bool(picking.move_ids.sale_line_id & lines)
        )
        self.assertEqual(len(pickings), 3)
        for picking in pickings:
            moves = picking.move_ids.filtered(lambda move: move.sale_line_id in lines)
            self.assertEqual(len(moves), 3)
            for move in moves:
                line = move.sale_line_id
                self.assertEqual(
                    move.packaging_uom_id,
                    line.packaging_uom_id or line.product_uom_id,
                )
                self.assertAlmostEqual(
                    move.packaging_uom_qty,
                    line.packaging_qty if line.packaging_uom_id else 5,
                )
                self.assertEqual(move.product_uom, line.product_uom_id)

    def test_packaging_recomputes_and_split_uses_its_own_quantity(self):
        order = self._new_order()
        line = self._add_line(order, self.packaging_uom_a, 2, quantity=24)
        order.action_confirm()
        moves = order.picking_ids.move_ids.filtered(lambda move: move.sale_line_id == line)
        self.assertTrue(moves)
        line.packaging_uom_id = self.packaging_uom_b
        for move in moves:
            self.assertEqual(move.packaging_uom_id, self.packaging_uom_b)
        split = moves[:1].copy({"product_uom_qty": 12})
        self.assertEqual(split.packaging_uom_id, self.packaging_uom_b)
        self.assertAlmostEqual(split.packaging_uom_qty, 1)
        line.packaging_uom_id = False
        for move in moves | split:
            self.assertEqual(move.packaging_uom_id, line.product_uom_id)
        for move in order.picking_packaging_ids.move_ids:
            self.assertEqual(move.packaging_uom_id, move.product_uom)

    def test_packaging_quantity_converts_stock_uom_to_sale_uom(self):
        order = self._new_order()
        line = self._add_line(order, self.packaging_uom_a, 2, quantity=20)
        order.action_confirm()
        move = order.picking_ids.move_ids.filtered(lambda move: move.sale_line_id == line)[:1]
        self.assertTrue(move)
        small_unit = self.env['uom.uom'].create({
            'name': 'Thousandth of sale unit',
            'relative_uom_id': line.product_uom_id.id,
            'relative_factor': 0.001,
            'rounding': 0.001,
        })
        converted = move.copy({
            'product_uom': small_unit.id, 'product_uom_qty': 20000,
        })
        self.assertEqual(converted.packaging_uom_id, line.packaging_uom_id)
        self.assertAlmostEqual(converted.packaging_uom_qty, 2)
        converted.product_uom_qty = 10000
        self.assertAlmostEqual(converted.packaging_uom_qty, 1)

    def test_same_packaging_product_is_aggregated(self):
        order = self._new_order()
        line_a = self._add_line(order, self.packaging_uom_a, 2.0, quantity=10.0)
        line_b = self._add_line(order, self.packaging_uom_a, 3.0, quantity=20.0)
        original_quantities = (line_a.product_uom_qty, line_b.product_uom_qty)
        original_uoms = (line_a.product_uom_id, line_b.product_uom_id)

        order.action_confirm()

        self.assertEqual(len(order.picking_packaging_ids), 1)
        picking = order.picking_packaging_ids
        self.assertNotEqual(picking.state, "draft")
        self.assertEqual(len(picking.move_ids), 1)
        self.assertEqual(picking.move_ids.product_id, self.packaging_product_a)
        self.assertEqual(picking.move_ids.product_uom_qty, 5.0)
        self.assertEqual(order.delivery_packaging_count, 1)
        self.assertEqual(
            (line_a.product_uom_qty, line_b.product_uom_qty),
            original_quantities,
        )
        self.assertEqual(
            (line_a.product_uom_id, line_b.product_uom_id),
            original_uoms,
        )

    def test_different_packaging_products_share_one_picking(self):
        order = self._new_order()
        self._add_line(order, self.packaging_uom_a, 2.0)
        self._add_line(order, self.packaging_uom_b, 4.0)

        order.action_confirm()

        self.assertEqual(len(order.picking_packaging_ids), 1)
        moves_by_product = {
            move.product_id: move.product_uom_qty
            for move in order.picking_packaging_ids.move_ids
        }
        self.assertEqual(moves_by_product[self.packaging_product_a], 2.0)
        self.assertEqual(moves_by_product[self.packaging_product_b], 4.0)

    def test_repeated_creation_does_not_duplicate_picking(self):
        order = self._new_order()
        self._add_line(order, self.packaging_uom_a, 2.0)
        order.action_confirm()
        first_picking = order.picking_packaging_ids

        second_result = order.create_picking_packaging_products()

        self.assertEqual(second_result, first_picking)
        self.assertEqual(len(order.picking_packaging_ids), 1)
        self.assertEqual(len(order.picking_packaging_ids.move_ids), 1)

    def test_cancelling_order_cancels_active_packaging_picking(self):
        order = self._new_order()
        self._add_line(order, self.packaging_uom_a, 2.0)
        order.action_confirm()
        picking = order.picking_packaging_ids

        order.action_cancel()

        self.assertEqual(picking.state, "cancel")
