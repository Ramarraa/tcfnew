# -*- coding: utf-8 -*-
from odoo import Command, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    _TCF_FRAGRANCE_CATEGORY = "ALL / SALEABLE / FRAGRANCE / TCF"
    _TCF_PACKAGING_EXCLUDED_CATEGORY = "ALL / PRODUCTION SUPPLIES / PACKAGING"
    _TCF_DEFAULT_PACKAGINGS = (
        ("10 ML SPRAY CAM SISE", 3.0),
        ("5 ML CAM NUMUNE", 3.5),
        ("10 ML CAM NUMUNE", 10.0),
        ("19 ML SAMPLES ALU", 15.0),
        ("ALUMINIUM 25 G", 25.0),
        ("ALUMINIUM 50 G", 50.0),
        ("100 CC ŞİŞE", 100.0),
        ("250CC ŞİŞE 50 DÜZ", 250.0),
        ("500CC ŞİŞE 50 DÜZ", 500.0),
        ("1 LT ŞİŞE 50 DÜZ", 1000.0),
        ("1 KG ALU", 1000.0),
        ("OMIN 1 KG ALU", 1000.0),
        ("1 KG ALCAN", 1000.0),
        ("5 LT SANAYİ 38 AĞIZ", 5000.0),
        ("5 KG ALU", 5000.0),
        ("5 KG ALCAN", 5000.0),
        ("10 LT BİDON", 10000.0),
        ("25 KG DRUM", 25000.0),
        ("30 LT BİDON", 25000.0),
        ("210 KG DRUM", 210000.0),
    )

    uom_root_path = fields.Char(compute="_compute_uom_root_path", store=True)
    sale_uom_id = fields.Many2one("uom.uom", string="Sales Unit of Measure", tracking=True,
                                  domain="[('parent_path', '=like', uom_root_path + '%')]")
    sale_samples_uom_id = fields.Many2one("uom.uom", string="Sales Samples Unit of Measure", tracking=True,
                                          domain="[('parent_path', '=like', uom_root_path + '%')]")
    purchase_uom_id = fields.Many2one("uom.uom", string="Purchase Unit of Measure", tracking=True,
                                      domain="[('parent_path', '=like', uom_root_path + '%')]")

    @api.depends("uom_id.parent_path")
    def _compute_uom_root_path(self):
        for template in self:
            template.uom_root_path = (
                template.uom_id.parent_path.split("/")[0] + "/"
                if template.uom_id and template.uom_id.parent_path else ""
            )

    # ------------------------------------------------------------------
    # Auto-fill Sales/Purchase UoM from the product category / base UoM
    #
    # Recovered from live (v16) behaviour, which had no code and no
    # base.automation for this - it was a Studio/manual convention. Verified
    # against live data (10,000+ products, uniform): every WEIGHT-based product
    # (base UoM in the same measure family as KG, e.g. G) - across RAW
    # MATERIALS, RM SUBSTITUE, ESSENCE OILS and all FRAGRANCE/* categories -
    # uses Sales UoM = KG and Purchase UoM = KG. Non-weight products (Units,
    # Hours...) had no auto-filled UoM, so we leave those for manual entry.
    #
    # We therefore fill Sales/Purchase UoM with KG whenever the base UoM is
    # weight-based and the field is still empty (never overwrite a value a user
    # set on purpose). KG is resolved by its stable external id, not a raw id.
    # ------------------------------------------------------------------
    def _tcf_weight_default_uom(self):
        """KG unit if this product's base UoM is weight-based, else empty."""
        self.ensure_one()
        kg = self.env.ref("uom.product_uom_kgm", raise_if_not_found=False)
        if kg and self.uom_id and self.uom_id._has_common_reference(kg):
            return kg
        return self.env["uom.uom"]

    def _tcf_fill_sale_purchase_uom(self):
        for template in self:
            if template.categ_id.complete_name == self._TCF_FRAGRANCE_CATEGORY:
                gram = self.env.ref("uom.product_uom_gram", raise_if_not_found=False)
                kg = self.env.ref("uom.product_uom_kgm", raise_if_not_found=False)
                if gram and kg:
                    if template.uom_id != gram:
                        template.uom_id = gram
                    if template.sale_uom_id != kg:
                        template.sale_uom_id = kg
                    if template.sale_samples_uom_id != gram:
                        template.sale_samples_uom_id = gram
                    if template.purchase_uom_id != kg:
                        template.purchase_uom_id = kg
                continue

            if template.categ_id.complete_name == self._TCF_PACKAGING_EXCLUDED_CATEGORY:
                continue

            kg = template._tcf_weight_default_uom()
            if not kg:
                continue
            if template.sale_ok and not template.sale_uom_id:
                template.sale_uom_id = kg
            if template.purchase_ok and not template.purchase_uom_id:
                template.purchase_uom_id = kg

    def _tcf_fill_default_packagings(self):
        """Link the legacy TCF packaging set using Odoo 19's UoM model.

        Runs for every product category except _TCF_PACKAGING_EXCLUDED_CATEGORY
        (packaging materials themselves should never get a default packaging set).
        """
        gram = self.env.ref("uom.product_uom_gram", raise_if_not_found=False)
        if not gram:
            return

        Uom = self.env["uom.uom"]
        PackageType = self.env["stock.package.type"]
        has_package_type = "package_type_id" in Uom._fields

        for template in self:
            if (
                template.categ_id.complete_name == self._TCF_PACKAGING_EXCLUDED_CATEGORY
                or template.uom_ids
            ):
                continue

            commands = []
            for sequence, (name, quantity) in enumerate(
                self._TCF_DEFAULT_PACKAGINGS, start=1
            ):
                packaging_uom = Uom.search([
                    ("name", "=", name),
                    ("relative_uom_id", "=", gram.id),
                    ("relative_factor", "=", quantity),
                ], limit=1)
                if not packaging_uom:
                    values = {
                        "name": name,
                        "relative_uom_id": gram.id,
                        "relative_factor": quantity,
                        "sequence": sequence,
                    }
                    if has_package_type:
                        package_type = PackageType.search(
                            [("name", "=", name)], limit=1
                        )
                        if package_type:
                            values["package_type_id"] = package_type.id
                    packaging_uom = Uom.create(values)
                commands.append(Command.link(packaging_uom.id))

            template.uom_ids = commands

    def _tcf_clear_defaults_for_packaging_category(self):
        """Packaging materials must not carry sales, purchase, or packaging defaults."""
        for template in self.filtered(
            lambda product: product.categ_id.complete_name
            == self._TCF_PACKAGING_EXCLUDED_CATEGORY
        ):
            template.sale_uom_id = False
            template.sale_samples_uom_id = False
            template.purchase_uom_id = False
            if template.uom_ids:
                template.uom_ids = [Command.clear()]

    @api.onchange("categ_id", "uom_id")
    def _onchange_fill_sale_purchase_uom(self):
        self._tcf_fill_sale_purchase_uom()

    @api.onchange("categ_id")
    def _onchange_clear_defaults_for_packaging_category(self):
        self._tcf_clear_defaults_for_packaging_category()

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        templates._tcf_fill_sale_purchase_uom()
        templates._tcf_fill_default_packagings()
        templates._tcf_clear_defaults_for_packaging_category()
        return templates

    def write(self, vals):
        res = super().write(vals)
        if "categ_id" in vals or "uom_id" in vals:
            self._tcf_fill_sale_purchase_uom()
            self._tcf_fill_default_packagings()
            self._tcf_clear_defaults_for_packaging_category()
        return res

    # --- keep existing clearing/validation onchanges -------------------
    @api.onchange("sale_ok")
    def onchange_uom_sale_ok(self):
        self.sale_uom_id = False
        self.sale_samples_uom_id = False

    @api.onchange("purchase_ok")
    def onchange_uom_purchase_ok(self):
        self.purchase_uom_id = False

    @api.onchange("uom_id")
    def onchange_uom_id(self):
        if self.sale_uom_id and self.uom_id and not self.uom_id._has_common_reference(self.sale_uom_id):
            self.sale_uom_id = False

        if self.sale_samples_uom_id and self.uom_id and not self.uom_id._has_common_reference(self.sale_samples_uom_id):
            self.sale_samples_uom_id = False

        if self.purchase_uom_id and self.uom_id and not self.uom_id._has_common_reference(self.purchase_uom_id):
            self.purchase_uom_id = False
