from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPackagingSuggestionOrder(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.gram = cls.env.ref("uom.product_uom_gram")
        cls.kg = cls.env.ref("uom.product_uom_kgm")
        cls.packagings = cls.env["uom.uom"].create([
            {
                "name": "Test 10 G Packaging",
                "relative_uom_id": cls.gram.id,
                "relative_factor": 10.0,
            },
            {
                "name": "Test 1 KG Packaging",
                "relative_uom_id": cls.gram.id,
                "relative_factor": 1000.0,
            },
            {
                "name": "Test 5 KG Packaging",
                "relative_uom_id": cls.gram.id,
                "relative_factor": 5000.0,
            },
        ])

    def test_exact_kg_packaging_is_suggested_first(self):
        results = self.env["uom.uom"].with_context(
            packaging_reference_factor=self.kg.factor,
        ).name_search(domain=[("id", "in", self.packagings.ids)])

        self.assertEqual(results[0][0], self.packagings[1].id)
        self.assertEqual(
            [uom_id for uom_id, _name in results],
            [
                self.packagings[1].id,
                self.packagings[2].id,
                self.packagings[0].id,
            ],
        )

    def test_search_more_orders_exact_kg_packaging_first(self):
        result = self.env["uom.uom"].with_context(
            packaging_reference_uom_id=self.kg.id,
        ).web_search_read(
            [("id", "in", self.packagings.ids)],
            {"display_name": {}},
        )

        self.assertEqual(
            [values["id"] for values in result["records"]],
            [
                self.packagings[1].id,
                self.packagings[2].id,
                self.packagings[0].id,
            ],
        )
