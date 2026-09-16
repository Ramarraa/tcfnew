from odoo import api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _TCF_SALES_PRICE_CATEGORY = 'ALL / SALEABLE / FRAGRANCE / TCF'

    fragrance_use_id = fields.Many2one(
        comodel_name='fragrance.uses',
        string='Fragrance Use',
        ondelete='set null',
    )
    admin_key = fields.Char(string='Admin Key')
    alternative_code = fields.Char(string='Alternative Code')
    brand_company = fields.Char(string='Brand Company')
    cas_number = fields.Char(string='CAS Number')
    common_code = fields.Char(string='Common Code')
    common_name = fields.Char(string='Common Name')
    fcost = fields.Float(string='FCost')
    fcost_monetary = fields.Monetary(
        string='FCost (Monetary)',
        currency_field='currency_id',
    )
    purpose_ids = fields.Many2many(
        comodel_name='product.purpose',
        string='Purposes',
    )
    scrap_arabic_name = fields.Char(string='Scrap Arabic Name')
    scrap_name = fields.Char(string='Scrap Name')
    scrapped = fields.Boolean(string='Scrapped')
    kg_price = fields.Monetary(
        string='KG Price',
        currency_field='currency_id',
        readonly=True,
    )

    # ------------------------------------------------------------------
    # Product-code auto-generation by category.
    #
    # Recovered from the v16 Studio automations "PM/FO/PS/QSP product
    # sequence" (on_create), which the v16->v19 upgrade deactivated
    # (active=False). Re-implemented in code so it is durable across Upgrade
    # Restorations and works on Odoo 19.
    #
    #   RAW MATERIALS  subtree -> default_code = sequence PMPRDIR
    #   SALEABLE       subtree -> default_code = sequence FOPRDIR
    #                             common_code  = sequence QSPPRDIR
    #   PRODUCTION SUPPLIES subtree -> default_code = sequence PSPRDIR
    #
    # Categories are matched by parent_path subtree (no hard-coded ids, robust
    # to renames of leaf categories); the sequence records already exist and are
    # reused by their `code`; each field is filled ONLY when empty so an
    # existing/imported code is never overwritten.
    # ------------------------------------------------------------------
    _TCF_CODE_RULES = [
        ('ALL / RAW MATERIALS', 'default_code', 'PMPRDIR'),
        ('ALL / SALEABLE', 'default_code', 'FOPRDIR'),
        ('ALL / SALEABLE', 'common_code', 'QSPPRDIR'),
        ('ALL / PRODUCTION SUPPLIES', 'default_code', 'PSPRDIR'),
    ]

    @staticmethod
    def _tcf_normalize_category_name(name):
        return (name or '').strip().casefold()

    def _tcf_category_matches_path(self, category, expected_path):
        """Match a category through its ancestors without relying on complete_name."""
        expected_names = [
            self._tcf_normalize_category_name(name)
            for name in expected_path.split('/')
        ]
        actual_names = []
        current = category
        while current:
            actual_names.append(self._tcf_normalize_category_name(current.name))
            current = current.parent_id
        actual_names.reverse()
        return actual_names[:len(expected_names)] == expected_names

    def _tcf_apply_category_code_sequences(self):
        Seq = self.env['ir.sequence']
        for tmpl in self:
            if not tmpl.categ_id:
                continue
            for root_name, field_name, seq_code in self._TCF_CODE_RULES:
                if not self._tcf_category_matches_path(tmpl.categ_id, root_name):
                    continue
                if tmpl[field_name]:
                    continue
                code = Seq.next_by_code(seq_code)
                if code:
                    tmpl[field_name] = code

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        templates._tcf_apply_category_code_sequences()
        return templates

    def write(self, vals):
        result = super().write(vals)
        if 'categ_id' in vals:
            self._tcf_apply_category_code_sequences()
        return result

    def action_tcf_update_sales_price_from_cost(self):
        updated_count = 0
        wrong_category = []
        zero_cost = []

        for product in self:
            if (
                not product.categ_id
                or product.categ_id.complete_name != self._TCF_SALES_PRICE_CATEGORY
            ):
                wrong_category.append(product.display_name)
                continue

            cost = product.standard_price or 0.0
            if cost == 0.0:
                zero_cost.append(product.display_name)
                continue

            new_price = cost * 2.5
            if product.list_price != new_price:
                product.write({'list_price': new_price})

            updated_count += 1

        if updated_count == 0:
            parts = ['No product was updated.']
            if wrong_category:
                parts.append(
                    'Wrong category (%s): %s'
                    % (len(wrong_category), ', '.join(wrong_category[:10]))
                )
            if zero_cost:
                parts.append(
                    'Cost = 0 (%s): %s'
                    % (len(zero_cost), ', '.join(zero_cost[:10]))
                )
            raise UserError('\n\n'.join(parts))

        message_lines = ['Updated products: %s' % updated_count]
        if wrong_category:
            message_lines.append(
                'Skipped بسبب category غير صحيحة: %s' % len(wrong_category)
            )
        if zero_cost:
            message_lines.append(
                'Skipped بسبب Cost = 0: %s' % len(zero_cost)
            )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sales Price Update',
                'message': '\n'.join(message_lines),
                'type': (
                    'warning' if wrong_category or zero_cost else 'success'
                ),
                'sticky': False,
                'next': {
                    'type': 'ir.actions.client',
                    'tag': 'soft_reload',
                },
            },
        }
