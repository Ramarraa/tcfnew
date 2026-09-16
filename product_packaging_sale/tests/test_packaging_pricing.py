from odoo import Command
from odoo.tests import Form, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPackagingPricing(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Packaging Test Customer"})
        cls.product = cls.env["product.product"].create({
            "name": "Sold Product",
            "list_price": 100.0,
        })
        cls.packaging_product = cls.env["product.product"].create({
            "name": "Packaging Material",
            "list_price": 5.0,
        })
        cls.other_packaging_product = cls.env["product.product"].create({
            "name": "Other Packaging Material",
            "list_price": 10.0,
        })
        cls.packaging_uom = cls.env.ref("uom.product_uom_dozen").copy({
            "name": "Test Packaging",
            "packaging_product_id": cls.packaging_product.id,
        })
        cls.other_packaging_uom = cls.packaging_uom.copy({
            "name": "Other Test Packaging",
            "packaging_product_id": cls.other_packaging_product.id,
        })
        cls.product.product_tmpl_id.uom_ids = [
            Command.link(cls.packaging_uom.id),
            Command.link(cls.other_packaging_uom.id),
        ]
        cls.order = cls.env["sale.order"].create({
            "partner_id": cls.partner.id,
        })

    def _new_line(self, quantity=10.0):
        return self.env["sale.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product.id,
            "product_uom_id": self.product.uom_id.id,
            "product_uom_qty": quantity,
        })

    def test_packaging_price_and_independent_quantity_uom(self):
        line = self._new_line()
        original_qty = line.product_uom_qty
        original_uom = line.product_uom_id
        original_price = line.price_unit_original

        line.write({
            "packaging_uom_id": self.packaging_uom.id,
            "packaging_qty": 2.0,
            "extra_price": 5.0,
        })

        self.assertEqual(line.product_uom_qty, original_qty)
        self.assertEqual(line.product_uom_id, original_uom)
        self.assertAlmostEqual(line.extra_price, 5.0)
        self.assertAlmostEqual(line.price_unit, ((10 * original_price) + (2 * 5)) / 10)

    def test_changing_packaging_does_not_accumulate(self):
        line = self._new_line()
        original_price = line.price_unit_original
        line.write({
            "packaging_uom_id": self.packaging_uom.id,
            "packaging_qty": 2.0,
            "extra_price": 7.0,
        })
        line.write({"packaging_uom_id": self.other_packaging_uom.id})

        self.assertAlmostEqual(line.extra_price, 7.0)
        self.assertAlmostEqual(line.price_unit, ((10 * original_price) + (2 * 7)) / 10)

    def test_clearing_packaging_restores_original_price(self):
        line = self._new_line()
        original_price = line.price_unit_original
        line.write({
            "packaging_uom_id": self.packaging_uom.id,
            "packaging_qty": 2.0,
            "extra_price": 5.0,
        })
        line.write({"packaging_uom_id": False})

        self.assertEqual(line.packaging_qty, 0.0)
        self.assertEqual(line.extra_price, 0.0)
        self.assertAlmostEqual(line.price_unit, original_price)

    def test_product_change_clears_invalid_packaging(self):
        other_product = self.env["product.product"].create({
            "name": "Other Sold Product",
            "list_price": 20.0,
        })
        line = self._new_line()
        with Form(line) as line_form:
            line_form.packaging_uom_id = self.packaging_uom
            line_form.packaging_qty = 1.0
            line_form.product_id = other_product
        self.assertFalse(line.packaging_uom_id)

    def test_zero_quantity_does_not_divide_by_zero(self):
        line = self._new_line(quantity=0.0)
        line.write({
            "packaging_uom_id": self.packaging_uom.id,
            "packaging_qty": 2.0,
            "extra_price": 5.0,
        })
        self.assertAlmostEqual(line.price_unit, line.price_unit_original)
