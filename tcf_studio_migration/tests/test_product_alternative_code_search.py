from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestProductAlternativeCodeSearch(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env['product.category'].create({
            'name': 'Alternative Code Search',
        })
        cls.other_category = cls.env['product.category'].create({
            'name': 'Other Search Category',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'ABREEV',
            'default_code': 'FO2506840',
            'categ_id': cls.category.id,
        })
        cls.product.product_tmpl_id.alternative_code = 'ARFW 433'
        cls.same_name_product = cls.env['product.product'].create({
            'name': 'ABREEV',
            'default_code': 'FO2506841',
            'categ_id': cls.category.id,
        })
        cls.same_name_product.product_tmpl_id.alternative_code = 'ARFW 434'
        cls.other_product = cls.env['product.product'].create({
            'name': 'Other Product',
            'default_code': 'OTHER-001',
            'categ_id': cls.other_category.id,
        })
        cls.other_product.product_tmpl_id.alternative_code = 'OTHER ALT'

    def _ids(self, term, operator='ilike', domain=None, limit=100):
        return {
            product_id
            for product_id, _name in self.env['product.product'].name_search(
                name=term,
                domain=domain,
                operator=operator,
                limit=limit,
            )
        }

    def test_search_by_internal_reference(self):
        self.assertIn(self.product.id, self._ids('FO2506840'))

    def test_search_by_product_name_returns_all_matches(self):
        result_ids = self._ids('ABREEV')
        self.assertIn(self.product.id, result_ids)
        self.assertIn(self.same_name_product.id, result_ids)

    def test_search_by_alternative_code(self):
        self.assertIn(self.product.id, self._ids('ARFW 433'))

    def test_exact_alternative_code(self):
        self.assertEqual(self._ids('ARFW 433', operator='='), {self.product.id})

    def test_partial_alternative_code(self):
        result_ids = self._ids('ARFW 43')
        self.assertIn(self.product.id, result_ids)
        self.assertIn(self.same_name_product.id, result_ids)

    def test_limit_and_domain_are_preserved(self):
        result_ids = self._ids(
            'ARFW',
            domain=[('categ_id', '=', self.category.id)],
            limit=1,
        )
        self.assertEqual(len(result_ids), 1)
        self.assertNotIn(
            self.other_product.id,
            self._ids('OTHER ALT', domain=[('categ_id', '=', self.category.id)]),
        )

    def test_inactive_product_respects_active_test(self):
        self.product.active = False
        self.assertNotIn(self.product.id, self._ids('ARFW 433'))

        inactive_ids = {
            product_id
            for product_id, _name in self.env['product.product'].with_context(
                active_test=False,
            ).name_search(name='ARFW 433')
        }
        self.assertIn(self.product.id, inactive_ids)
