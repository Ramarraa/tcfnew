from collections import defaultdict
from odoo.tools.float_utils import float_is_zero

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    packaging_uom_id = fields.Many2one(
        "uom.uom",
        string="Packaging",
    )
    packaging_qty = fields.Float(
        string="Packaging Quantity",
        default=0.0,
    )
    extra_price = fields.Float(
        string="Extra Price",
        digits="Product Price",
    )
    current_extra_price = fields.Float(
        string="Old Extra Price",
        digits="Product Price",
    )
    price_unit_original = fields.Float(
        compute="_compute_price_unit",
        string="Unit Price (Original)",
        digits="Product Price",
        store=True,
        readonly=True,
        precompute=True,
    )
    available_packaging_uom_ids = fields.Many2many(
        "uom.uom",
        compute="_compute_available_packaging_uom_ids",
        string="Available Packagings",
    )
    packaging_reference_factor = fields.Float(
        compute="_compute_packaging_reference_factor",
    )

    @api.depends("product_id", "product_id.product_tmpl_id.uom_ids")
    def _compute_available_packaging_uom_ids(self):
        for line in self:
            line.available_packaging_uom_ids = line.product_id.product_tmpl_id.uom_ids

    @api.depends("product_uom_id", "product_uom_id.factor")
    def _compute_packaging_reference_factor(self):
        for line in self:
            line.packaging_reference_factor = line.product_uom_id.factor or 0.0

    def _onchange_product_id_clear_invalid_packaging(self):
        """Compatibility helper; suggestion onchange owns product changes."""
        for line in self:
            _logger.warning(
                "PACKAGING DEBUG | CLEAR ONCHANGE TRIGGERED | product=%s",
                line.product_id.display_name,
            )

            if line.packaging_uom_id not in line.product_id.product_tmpl_id.uom_ids:
                line.packaging_uom_id = False

    def _get_packaging_quantity_in_line_uom(self, packaging):
        self.ensure_one()
        packaging.ensure_one()

        _logger.warning(
            "PACKAGING DEBUG | Converting packaging=%s | line_uom=%s | "
            "relative_uom=%s | relative_factor=%s | factor=%s",
            packaging.display_name,
            self.product_uom_id.display_name,
            packaging.relative_uom_id.display_name,
            packaging.relative_factor,
            packaging.factor,
        )

        if not self.product_uom_id:
            _logger.warning(
                "PACKAGING DEBUG | No product_uom_id on sale order line"
            )
            return 0.0

        source_uom = packaging.relative_uom_id or packaging

        if not source_uom._has_common_reference(self.product_uom_id):
            _logger.warning(
                "PACKAGING DEBUG | No common reference | packaging=%s | "
                "source_uom=%s | line_uom=%s",
                packaging.display_name,
                source_uom.display_name,
                self.product_uom_id.display_name,
            )
            return 0.0

        source_quantity = (
            packaging.relative_factor
            if packaging.relative_uom_id
            else 1.0
        )

        converted_quantity = source_uom._compute_quantity(
            source_quantity,
            self.product_uom_id,
            round=False,
        )

        _logger.warning(
            "PACKAGING DEBUG | Converted packaging=%s | "
            "source_quantity=%s | result=%s %s",
            packaging.display_name,
            source_quantity,
            converted_quantity,
            self.product_uom_id.display_name,
        )

        return converted_quantity

    def _find_suitable_packaging_uom(self):
        self.ensure_one()

        _logger.warning(
            "PACKAGING DEBUG | Finding packaging | product=%s | qty=%s | "
            "uom=%s",
            self.product_id.display_name,
            self.product_uom_qty,
            self.product_uom_id.display_name,
        )

        if (
                not self.product_id
                or not self.product_uom_id
                or not self.product_uom_qty
        ):
            _logger.warning(
                "PACKAGING DEBUG | Missing required value | "
                "product=%s | qty=%s | uom=%s",
                self.product_id.display_name,
                self.product_uom_qty,
                self.product_uom_id.display_name,
            )
            return self.env["uom.uom"]

        packagings = self.product_id.product_tmpl_id.uom_ids

        _logger.warning(
            "PACKAGING DEBUG | Available packagings count=%s | values=%s",
            len(packagings),
            packagings.mapped("display_name"),
        )

        packaging_values = []

        for packaging in packagings:
            packaging_quantity = (
                self._get_packaging_quantity_in_line_uom(packaging)
            )

            _logger.warning(
                "PACKAGING DEBUG | Candidate=%s | converted_size=%s",
                packaging.display_name,
                packaging_quantity,
            )

            if packaging_quantity > 0:
                packaging_values.append(
                    (packaging, packaging_quantity)
                )

        # Prefer the largest suitable packaging.  For equal capacities, use
        # the same sequence shown in Packaging Ordered on the product.
        packaging_values.sort(
            key=lambda value: (
                -value[1],
                *self._get_packaging_suggestion_order_key(value[0]),
            ),
        )

        _logger.warning(
            "PACKAGING DEBUG | Ordered candidates=%s",
            [
                (packaging.display_name, quantity)
                for packaging, quantity in packaging_values
            ],
        )

        for packaging, packaging_quantity in packaging_values:
            packaging_count = (
                    self.product_uom_qty / packaging_quantity
            )
            difference = packaging_count - round(packaging_count)

            _logger.warning(
                "PACKAGING DEBUG | Testing=%s | packaging_size=%s | "
                "package_count=%s | difference=%s",
                packaging.display_name,
                packaging_quantity,
                packaging_count,
                difference,
            )

            if float_is_zero(
                    difference,
                    precision_rounding=1e-6,
            ):
                _logger.warning(
                    "PACKAGING DEBUG | SELECTED packaging=%s",
                    packaging.display_name,
                )
                return packaging

        _logger.warning(
            "PACKAGING DEBUG | No suitable packaging found"
        )

        return self.env["uom.uom"]

    def _get_packaging_suggestion_order_key(self, packaging):
        """Tie-break equal capacities using the default UoM order."""
        self.ensure_one()
        return packaging.sequence, packaging.id

    @api.onchange(
        "product_id",
        "product_uom_qty",
        "product_uom_id",
    )
    def _onchange_suggest_packaging_uom(self):
        for line in self:
            _logger.warning(
                "PACKAGING DEBUG | Onchange triggered | product=%s | "
                "qty=%s | uom=%s | current_packaging=%s",
                line.product_id.display_name,
                line.product_uom_qty,
                line.product_uom_id.display_name,
                line.packaging_uom_id.display_name,
            )

            if (
                    not line.product_id
                    or not line.product_uom_id
                    or not line.product_uom_qty
            ):
                _logger.warning(
                    "PACKAGING DEBUG | Clearing packaging because values "
                    "are incomplete"
                )
                line.packaging_uom_id = False
                line.packaging_qty = 0.0
                continue

            suggested_packaging = (
                line._find_suitable_packaging_uom()
            )

            _logger.warning(
                "PACKAGING DEBUG | Suggested result=%s",
                suggested_packaging.display_name,
            )

            line.packaging_uom_id = suggested_packaging
            line.packaging_qty = line._get_packaging_count(
                suggested_packaging
            )

    def _get_packaging_count(self, packaging=None):
        """Return the line quantity expressed as a number of packages."""
        self.ensure_one()
        packaging = packaging or self.packaging_uom_id
        if not packaging or not self.product_uom_qty:
            return 0.0

        packaging_quantity = self._get_packaging_quantity_in_line_uom(
            packaging
        )
        if not packaging_quantity:
            return 0.0

        return self.product_uom_qty / packaging_quantity

    @api.onchange("packaging_uom_id")
    def _onchange_packaging_uom_id(self):
        for line in self:
            if not line.packaging_uom_id:
                line.packaging_qty = 0.0
                line.extra_price = 0.0
            else:
                line.packaging_qty = line._get_packaging_count()

    @api.depends(
        "packaging_uom_id",
        "packaging_qty",
        "extra_price",
        "product_uom_qty",
        "product_id",
        "product_uom_id",
        "order_id.pricelist_id",
        "order_id.date_order",
    )
    def _compute_price_unit(self):
        super()._compute_price_unit()
        for line in self:
            original_price = line.technical_price_unit
            line.price_unit_original = original_price

            if line.display_type or not line.product_id:
                continue

            if line.packaging_uom_id and line.product_uom_qty:
                final_price = (
                    (line.product_uom_qty * original_price)
                    + (line.packaging_qty * line.extra_price)
                ) / line.product_uom_qty
            else:
                final_price = original_price

            # Keep the technical price aligned so the packaging adjustment is not
            # mistaken for a manual price and never accumulates on recomputation.
            line.price_unit = final_price
            line.technical_price_unit = final_price

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("packaging_uom_id"):
                vals["packaging_qty"] = 0.0
                vals["extra_price"] = 0.0
        return super().create(vals_list)

    def write(self, vals):
        if "packaging_uom_id" in vals and not vals["packaging_uom_id"]:
            vals = dict(vals, packaging_qty=0.0, extra_price=0.0)
        return super().write(vals)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    picking_packaging_ids = fields.Many2many("stock.picking", string="Transfers Packaging", copy=False)
    delivery_packaging_count = fields.Integer(compute="_compute_delivery_packaging_count", string="Delivery Packaging Orders")

    def _compute_delivery_packaging_count(self):
        for order in self:
            order.delivery_packaging_count = len(order.picking_packaging_ids)

    def _get_packaging_product_quantities(self):
        self.ensure_one()
        quantities = defaultdict(float)
        for line in self.order_line:
            packaging_product = line.packaging_uom_id.packaging_product_id
            if packaging_product and line.packaging_qty > 0:
                quantities[packaging_product] += line.packaging_qty
        return quantities

    def create_picking_packaging_products(self):
        """Create one idempotent, aggregated packaging picking for this order."""
        self.ensure_one()

        existing_pickings = self.picking_packaging_ids.filtered(
            lambda picking: picking.state != "cancel"
        )
        if existing_pickings:
            return existing_pickings[:1]

        product_quantities = self._get_packaging_product_quantities()
        if not product_quantities:
            return self.env["stock.picking"]

        picking_type = (
            self.warehouse_id.packaging_product_out_type_id
            or self.warehouse_id.out_type_id
        )
        source_location = picking_type.default_location_src_id
        destination_location = (
            picking_type.default_location_dest_id
            or self.partner_shipping_id.property_stock_customer
        )
        if not source_location or not destination_location:
            raise UserError(_(
                "The packaging operation type must have a source location, and "
                "the order must have a customer destination location."
            ))

        move_commands = []
        for packaging_product, quantity in product_quantities.items():
            move_commands.append(Command.create({
                "product_id": packaging_product.id,
                "product_uom": packaging_product.uom_id.id,
                "product_uom_qty": quantity,
                "location_id": source_location.id,
                "location_dest_id": destination_location.id,
                "description_picking": _(
                    "Packaging for %(order)s: %(product)s",
                    order=self.name,
                    product=packaging_product.display_name,
                ),
            }))

        picking = self.env["stock.picking"].create({
            "picking_type_id": picking_type.id,
            "location_id": source_location.id,
            "location_dest_id": destination_location.id,
            "partner_id": self.partner_shipping_id.id,
            "origin": self.name,
            "scheduled_date": self.date_order,
            "move_type": self.picking_policy,
            "company_id": self.company_id.id,
            "move_ids": move_commands,
        })
        picking.action_confirm()
        self.write({"picking_packaging_ids": [Command.link(picking.id)]})
        return picking

    # Odoo 19 merged product.packaging into uom.uom (packaging is now a UoM record with a
    # package_type_id); sale.order.line no longer has a separate product_packaging_id/
    # product_packaging_qty field to key this logic off. Needs a redesign around the new
    # UoM-based packaging model, not a rename. Also note: _prepare_picking_packaging_product()
    # above (still active) references sale.order.procurement_group_id, which no longer exists
    # either (procurement.group was removed in Odoo 19, see MIGRATION_TRACKER.md Section 6) —
    # currently harmless only because nothing calls it while this method stays commented out.
    # def create_picking_packaging_products(self):
    #     moves = []
    #     warehouse = self.warehouse_id
    #     picking_type = warehouse.packaging_product_out_type_id or warehouse.out_type_id
    #
    #     if picking_type.default_location_dest_id:
    #         location_dest_id = picking_type.default_location_dest_id.id
    #     elif self.partner_id.property_stock_customer:
    #         location_dest_id = self.partner_id.property_stock_customer.id
    #     else:
    #         location_dest_id, _ = self.env['stock.warehouse']._get_partner_locations()
    #
    #     for line in self.order_line.filtered(lambda l: l.product_packaging_id):
    #         if line.product_packaging_id.packaging_product_id:
    #             moves.append((0, 0, line._prepare_move_packaging_product(picking_type, location_dest_id)))
    #
    #     if moves:
    #         picking = self.env["stock.picking"].create(
    #             self._prepare_picking_packaging_product(moves, picking_type, location_dest_id))
    #         picking.action_confirm()
    #         self.write({"picking_packaging_ids": [(4, picking.id)]})
    #
    #     return True

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            order.create_picking_packaging_products()
        return result

    def _action_cancel(self):
        self.picking_packaging_ids.filtered(
            lambda picking: picking.state not in ("done", "cancel")
        ).action_cancel()
        return super(SaleOrder, self)._action_cancel()

    def action_view_delivery_packaging(self):
        if not self.picking_packaging_ids:
            return

        action = self.sudo().env.ref("stock.action_picking_tree_all")
        result = action.read()[0]
        result["domain"] = [("id", "=", self.picking_packaging_ids.ids)]
        return result


# Odoo 19 merged product.packaging into uom.uom; sale.order.line no longer has a separate
# product_packaging_id/product_packaging_qty field, so this extra-price-per-packaging logic has
# no field to key off. Needs a redesign around the new UoM-based packaging model, not a rename.
# class SaleOrderLine(models.Model):
#     _inherit = "sale.order.line"
#
#     extra_price = fields.Float(compute="_compute_extra_price", string="Extra Price",
#                              digits="Product Price", store=True, readonly=False, precompute=True)
#     current_extra_price = fields.Float(compute="_compute_current_extra_price", string="Old Extra Price",
#                                      digits="Product Price", store=True, readonly=False, precompute=True)
#     price_unit_original = fields.Float(compute="_compute_price_unit_original", string="Unit Price (Original)",
#                                      digits="Product Price", store=True, readonly=True, precompute=True)
#
#     @api.depends("product_packaging_id", "product_packaging_qty")
#     def _compute_extra_price(self):
#         ...
#
#     @api.depends("extra_price")
#     def _compute_current_extra_price(self):
#         ...
#
#     @api.depends("current_extra_price", "price_unit")
#     def _compute_price_unit_original(self):
#         ...
#
#     @api.depends("extra_price", "price_unit_original")
#     def _compute_price_unit(self):
#         ...
#
#     def _prepare_move_packaging_product(self, picking_type, location_dest_id):
#         ...
