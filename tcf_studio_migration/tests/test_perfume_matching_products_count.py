from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestPerfumeMatchingProductsCount(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.template'].create({
            'name': 'Matching Product',
            'alternative_code': 'TEST123',
        })

    def test_matching_product_is_counted(self):
        perfume = self.env['perfume.perfume'].create({
            'name': 'Matching Perfume',
            'code': 'TEST 123',
        })

        self.assertEqual(perfume.matching_products_count, 1)

    def test_empty_code_has_zero_matches(self):
        perfume = self.env['perfume.perfume'].create({
            'name': 'Perfume Without Code',
        })

        self.assertEqual(perfume.matching_products_count, 0)

    def test_set_status_not_printed_action(self):
        perfumes = self.env['perfume.perfume'].create([
            {'name': 'First Status Test', 'status': 'checking'},
            {'name': 'Second Status Test', 'status': 'Printed'},
        ])

        perfumes.action_set_status_not_printed()

        self.assertEqual(perfumes.mapped('status'), ['Not Printed', 'Not Printed'])
        messages = self.env['mail.message'].search([
            ('model', '=', 'perfume.perfume'),
            ('res_id', 'in', perfumes.ids),
            ('body', 'ilike', 'Status set to NOT PRINTED'),
        ])
        self.assertEqual(len(messages), 2)

    def test_set_status_printed_action(self):
        perfumes = self.env['perfume.perfume'].create([
            {'name': 'First Printed Test', 'status': 'checking'},
            {'name': 'Second Printed Test', 'status': 'Not Printed'},
        ])

        perfumes.action_set_status_printed()

        self.assertEqual(perfumes.mapped('status'), ['Printed', 'Printed'])
        messages = self.env['mail.message'].search([
            ('model', '=', 'perfume.perfume'),
            ('res_id', 'in', perfumes.ids),
            ('body', 'ilike', 'Status set to PRINTED'),
        ])
        self.assertEqual(len(messages), 2)

    def test_set_status_to_print_action(self):
        perfumes = self.env['perfume.perfume'].create([
            {'name': 'First To Print Test', 'status': 'checking'},
            {'name': 'Second To Print Test', 'status': 'Not Printed'},
        ])

        perfumes.action_set_status_to_print()

        self.assertEqual(perfumes.mapped('status'), ['To Print', 'To Print'])
        messages = self.env['mail.message'].search([
            ('model', '=', 'perfume.perfume'),
            ('res_id', 'in', perfumes.ids),
            ('body', 'ilike', 'Status set to TO PRINT'),
        ])
        self.assertEqual(len(messages), 2)

    def test_set_status_checking_action(self):
        perfumes = self.env['perfume.perfume'].create([
            {'name': 'First Checking Test', 'status': 'Printed'},
            {'name': 'Second Checking Test', 'status': 'To Print'},
        ])

        perfumes.action_set_status_checking()

        self.assertEqual(perfumes.mapped('status'), ['checking', 'checking'])
        messages = self.env['mail.message'].search([
            ('model', '=', 'perfume.perfume'),
            ('res_id', 'in', perfumes.ids),
            ('body', 'ilike', 'Status set to CHECKING'),
        ])
        self.assertEqual(len(messages), 2)
