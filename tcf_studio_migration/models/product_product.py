from odoo import api, models
from odoo.fields import Domain


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _search_display_name(self, operator, value):
        """Extend Odoo 19's display-name search with the template alternative code."""
        standard_domain = Domain(super()._search_display_name(operator, value))
        alternative_domain = Domain(
            'product_tmpl_id.alternative_code',
            operator,
            value,
        )
        if operator in Domain.NEGATIVE_OPERATORS:
            return Domain.AND([standard_domain, alternative_domain])
        return Domain.OR([standard_domain, alternative_domain])

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        """Preserve product.product's optimized lookup and add Alternative Code."""
        if not name:
            return super().name_search(name, domain, operator, limit)

        search_domain = Domain(domain or Domain.TRUE)
        if operator in Domain.NEGATIVE_OPERATORS:
            products = self.search_fetch(
                search_domain & Domain('display_name', operator, name),
                ['display_name'],
                limit=limit,
            )
            return [(product.id, product.display_name) for product in products.sudo()]

        standard_results = super().name_search(
            name=name,
            domain=domain,
            operator=operator,
            limit=limit,
        )
        standard_ids = [product_id for product_id, _display_name in standard_results]

        exact_products = self.search_fetch(
            search_domain
            & Domain('product_tmpl_id.alternative_code', '=', name),
            ['display_name'],
            limit=limit,
        )
        remaining = None if not limit else max(limit - len(exact_products), 0)
        partial_products = self.browse()
        if remaining is None or remaining:
            partial_products = self.search_fetch(
                search_domain
                & Domain('id', 'not in', exact_products.ids + standard_ids)
                & Domain('product_tmpl_id.alternative_code', operator, name),
                ['display_name'],
                limit=remaining,
            )

        ordered_ids = []
        for product_id in exact_products.ids + standard_ids + partial_products.ids:
            if product_id not in ordered_ids:
                ordered_ids.append(product_id)
            if limit and len(ordered_ids) >= limit:
                break

        products_by_id = {
            product.id: product
            for product in self.browse(ordered_ids).sudo()
        }
        return [
            (product_id, products_by_id[product_id].display_name)
            for product_id in ordered_ids
        ]
