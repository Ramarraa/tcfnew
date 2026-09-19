# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools.sql import SQL, drop_view_if_exists


class ProductPackagingReport(models.Model):
    _name = "product.packaging.report"
    _description = "Product Packaging"
    _auto = False
    _rec_name = "product_id"
    _order = "packaging_id, product_id"

    product_id = fields.Many2one("product.product", string="Product", readonly=True)
    packaging_id = fields.Many2one("uom.uom", string="Packaging", readonly=True)
    package_type_id = fields.Many2one(
        "stock.package.type", string="Package Type", readonly=True
    )
    contained_quantity = fields.Float(string="Contained Quantity", readonly=True)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure", readonly=True)
    sales = fields.Boolean(string="Sales", readonly=True)
    purchase = fields.Boolean(string="Purchase", readonly=True)
    active = fields.Boolean(readonly=True)

    def init(self):
        packaging_field = self.env["product.template"]._fields["uom_ids"]
        drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(SQL(
            """
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    ROW_NUMBER() OVER (
                        ORDER BY relation.%s, product.id, packaging.id
                    ) AS id,
                    product.id AS product_id,
                    packaging.id AS packaging_id,
                    packaging.package_type_id AS package_type_id,
                    COALESCE(packaging.relative_factor, 1.0)
                        AS contained_quantity,
                    COALESCE(packaging.relative_uom_id, packaging.id) AS uom_id,
                    TRUE AS sales,
                    (template.purchase_uom_id = packaging.id) AS purchase,
                    template.active AS active
                FROM %s AS relation
                JOIN product_template AS template
                    ON template.id = relation.%s
                JOIN product_product AS product
                    ON product.product_tmpl_id = template.id
                JOIN uom_uom AS packaging
                    ON packaging.id = relation.%s
            )
            """,
            SQL.identifier(self._table),
            SQL.identifier(packaging_field.column1),
            SQL.identifier(packaging_field.relation),
            SQL.identifier(packaging_field.column1),
            SQL.identifier(packaging_field.column2),
        ))
