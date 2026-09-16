from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestProductSalesPriceAction(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        all_category = cls.env['product.category'].create({'name': 'ALL'})
        saleable_category = cls.env['product.category'].create({
            'name': 'SALEABLE',
            'parent_id': all_category.id,
        })
        fragrance_category = cls.env['product.category'].create({
            'name': 'FRAGRANCE',
            'parent_id': saleable_category.id,
        })
        cls.tcf_category = cls.env['product.category'].create({
            'name': 'TCF',
            'parent_id': fragrance_category.id,
        })
        cls.other_category = cls.env['product.category'].create({
            'name': 'Other Category',
        })

    def test_updates_sales_price_from_cost(self):
        product = self.env['product.template'].create({
            'name': 'TCF Price Test',
            'categ_id': self.tcf_category.id,
            'standard_price': 100.0,
            'list_price': 10.0,
        })

        result = product.action_tcf_update_sales_price_from_cost()

        self.assertEqual(product.list_price, 250.0)
        self.assertEqual(result['params']['type'], 'success')

    def test_rejects_wrong_category(self):
        product = self.env['product.template'].create({
            'name': 'Wrong Category Price Test',
            'categ_id': self.other_category.id,
            'standard_price': 100.0,
            'list_price': 10.0,
        })

        with self.assertRaises(UserError):
            product.action_tcf_update_sales_price_from_cost()

        self.assertEqual(product.list_price, 10.0)

    def test_rejects_zero_cost(self):
        product = self.env['product.template'].create({
            'name': 'Zero Cost Price Test',
            'categ_id': self.tcf_category.id,
            'standard_price': 0.0,
            'list_price': 10.0,
        })

        with self.assertRaises(UserError):
            product.action_tcf_update_sales_price_from_cost()

        self.assertEqual(product.list_price, 10.0)
