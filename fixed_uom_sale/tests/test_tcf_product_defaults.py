from odoo import Command
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestTcfProductDefaults(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Category = cls.env["product.category"]
        parent = False
        for name in ("ALL", "SALEABLE", "FRAGRANCE", "TCF"):
            parent = Category.create({
                "name": name,
                "parent_id": parent.id if parent else False,
            })
        cls.tcf_category = parent

        parent = False
        for name in ("ALL", "PRODUCTION SUPPLIES", "PACKAGING"):
            parent = Category.create({
                "name": name,
                "parent_id": parent.id if parent else False,
            })
        cls.packaging_materials_category = parent

        cls.other_category = Category.create({"name": "Unrelated Category"})

        cls.gram = cls.env.ref("uom.product_uom_gram")
        cls.kg = cls.env.ref("uom.product_uom_kgm")

    def _create_product(self, **extra_values):
        values = {
            "name": "TCF Default Product",
            "categ_id": self.tcf_category.id,
            "uom_id": self.kg.id,
            "sale_ok": True,
            "purchase_ok": True,
        }
        values.update(extra_values)
        return self.env["product.template"].create(values)

    def test_tcf_uom_defaults_and_packagings_are_applied_together(self):
        product = self._create_product()

        self.assertEqual(product.uom_id, self.gram)
        self.assertEqual(product.sale_uom_id, self.kg)
        self.assertEqual(product.sale_samples_uom_id, self.gram)
        self.assertEqual(product.purchase_uom_id, self.kg)
        self.assertEqual(len(product.uom_ids), 20)
        self.assertEqual(
            product.uom_ids.filtered(
                lambda uom: uom.name == "210 KG DRUM"
            ).relative_factor,
            210000.0,
        )

    def test_existing_packaging_is_preserved_without_adding_defaults(self):
        existing = self.env["uom.uom"].create({
            "name": "Customer-specific packaging",
            "relative_uom_id": self.gram.id,
            "relative_factor": 42.0,
        })
        product = self._create_product(uom_ids=[Command.link(existing.id)])

        self.assertEqual(product.uom_id, self.gram)
        self.assertEqual(product.sale_uom_id, self.kg)
        self.assertEqual(product.sale_samples_uom_id, self.gram)
        self.assertEqual(product.purchase_uom_id, self.kg)
        self.assertEqual(product.uom_ids, existing)

    def test_default_packagings_apply_outside_tcf_category_too(self):
        product = self._create_product(categ_id=self.other_category.id)

        self.assertEqual(product.sale_uom_id, self.kg)
        self.assertEqual(product.purchase_uom_id, self.kg)
        self.assertEqual(len(product.uom_ids), 20)
        self.assertEqual(
            product.uom_ids.filtered(
                lambda uom: uom.name == "210 KG DRUM"
            ).relative_factor,
            210000.0,
        )

    def test_packaging_materials_category_is_excluded(self):
        product = self._create_product(categ_id=self.packaging_materials_category.id)

        self.assertFalse(product.uom_ids)
        self.assertFalse(product.sale_uom_id)
        self.assertFalse(product.purchase_uom_id)
