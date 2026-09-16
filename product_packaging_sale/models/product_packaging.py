# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockPackageType(models.Model):
    _inherit = "stock.package.type"
    packaging_product_id = fields.Many2one("product.product", string="Packaging Product")


class ProductPackaging(models.Model):
    _inherit = "uom.uom"

    packaging_product_id = fields.Many2one(
        "product.product",
        string="Packaging Product",
    )

    def _packaging_suggestion_sort_key(self, reference_factor, reference_uom=False, reference_qty=1.0):
        self.ensure_one()
        reference_qty = reference_qty or 1.0
        if reference_uom:
            source_uom = self.relative_uom_id or self
            if not source_uom._has_common_reference(reference_uom):
                return (3, 0.0, self.sequence, self.id)
            packaging_quantity = source_uom._compute_quantity(
                self.relative_factor if self.relative_uom_id else 1.0,
                reference_uom,
                round=False,
            )
            difference = packaging_quantity - reference_qty
        else:
            difference = self.factor - reference_factor * reference_qty

        if abs(difference) < 1e-9:
            return (0, 0.0, self.sequence, self.id)
        if difference > 0:
            return (1, difference, self.sequence, self.id)
        return (2, -difference, self.sequence, self.id)

    def name_search(self, name="", domain=None, operator="ilike", limit=100):
        """Suggest packaging sizes closest to the sale line UoM first."""
        reference_factor = self.env.context.get("packaging_reference_factor")
        reference_uom_id = self.env.context.get("packaging_reference_uom_id")
        reference_qty = self.env.context.get("packaging_reference_qty") or 1.0
        if not reference_factor and not reference_uom_id:
            return super().name_search(name, domain, operator, limit)

        results = super().name_search(name, domain, operator, limit=None)
        reference_uom = self.browse(reference_uom_id).exists() if reference_uom_id else self
        if not reference_factor:
            if not reference_uom:
                return results[:limit] if limit else results
            reference_factor = reference_uom.factor

        result_names = dict(results)
        candidate_uoms = self.browse([uom_id for uom_id, _name in results])

        ordered_uoms = candidate_uoms.sorted(
            key=lambda uom: uom._packaging_suggestion_sort_key(
                reference_factor,
                reference_uom,
                reference_qty,
            )
        )
        if limit:
            ordered_uoms = ordered_uoms[:limit]
        return [(uom.id, result_names[uom.id]) for uom in ordered_uoms]

    @api.model
    def web_search_read(
        self,
        domain,
        specification,
        offset=0,
        limit=None,
        order=None,
        count_limit=None,
    ):
        """Apply the same packaging order in the Search More dialog."""
        reference_factor = self.env.context.get("packaging_reference_factor")
        reference_uom_id = self.env.context.get("packaging_reference_uom_id")
        reference_qty = self.env.context.get("packaging_reference_qty") or 1.0
        reference_uom = self.browse(reference_uom_id).exists() if reference_uom_id else self
        if not reference_factor and reference_uom:
            reference_factor = reference_uom.factor
        if not reference_factor:
            return super().web_search_read(
                domain,
                specification,
                offset=offset,
                limit=limit,
                order=order,
                count_limit=count_limit,
            )

        result = super().web_search_read(
            domain,
            specification,
            offset=0,
            limit=None,
            order=order,
            count_limit=count_limit,
        )
        values_by_id = {values["id"]: values for values in result["records"]}
        ordered_uoms = self.browse(values_by_id).sorted(
            key=lambda uom: uom._packaging_suggestion_sort_key(
                reference_factor,
                reference_uom,
                reference_qty,
            )
        )
        ordered_values = [values_by_id[uom.id] for uom in ordered_uoms]
        result["records"] = (
            ordered_values[offset:offset + limit]
            if limit
            else ordered_values[offset:]
        )
        return result
