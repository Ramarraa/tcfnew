# -*- coding: utf-8 -*-

import re

from odoo import models

PICKING_SC_COPY1_ARCH = """<t t-name="stock.report_picking_copy_1_copy_1">
            <t t-call="web.html_container">
                <t t-foreach="docs" t-as="o">
                    <t t-call="web.external_layout">
                        <div class="page o_tcf_sc_picking2">
                            <style t-translation="off">
                                .o_tcf_sc_picking2 .o_tcf_sc_picking_row {
                                    display: -webkit-box !important;
                                    display: flex !important;
                                    -webkit-box-orient: horizontal !important;
                                    -webkit-box-pack: start !important;
                                    flex-wrap: wrap !important;
                                }
                                .o_tcf_sc_picking2 .o_tcf_sc_picking_row > div {
                                    margin-right: 96px !important;
                                }
                                .o_tcf_sc_picking2 .o_tcf_sc_picking_row > div strong,
                                .o_tcf_sc_picking2 .o_tcf_sc_picking_row > div p {
                                    display: block !important;
                                    margin: 0 !important;
                                }
                                .o_tcf_sc_picking2 table.table-sm thead th {
                                    color: #af1015 !important;
                                    font-weight: 700 !important;
                                    text-align: center !important;
                                    text-transform: uppercase !important;
                                }
                            </style>
                            <div class="row justify-content-end mb16">
                                <div class="col-4" name="right_box">
                                    <div t-field="o.name" t-options="{'widget': 'barcode', 'width': 600, 'height': 100, 'img_style': 'width:300px;height:50px;'}"/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-6" name="div_outgoing_address">
                                    <div t-if="o.should_print_delivery_address()">
                                        <span><strong>Delivery Address:</strong></span>
                                        <div t-field="o.move_ids[0].partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                    <div t-elif="o.picking_type_id.code != 'internal' and o.picking_type_id.warehouse_id.partner_id">
                                        <span><strong>Warehouse Address:</strong></span>
                                        <div t-field="o.picking_type_id.warehouse_id.partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                </div>
                                <div class="col-5 offset-1" name="div_incoming_address">
                                    <t t-set="show_partner" t-value="False"/>
                                    <div t-if="o.picking_type_id.code=='incoming' and o.partner_id">
                                        <span><strong>Vendor Address:</strong></span>
                                        <t t-set="show_partner" t-value="True"/>
                                    </div>
                                    <div t-if="o.picking_type_id.code=='internal' and o.partner_id">
                                        <span><strong>Warehouse Address:</strong></span>
                                        <t t-set="show_partner" t-value="True"/>
                                    </div>
                                    <div t-if="o.picking_type_id.code=='outgoing' and o.partner_id and o.partner_id != o.partner_id.commercial_partner_id">
                                        <span><strong>Customer Address:</strong></span>
                                        <t t-set="show_partner" t-value="True"/>
                                    </div>
                                    <div t-if="show_partner" name="partner_header">
                                        <div t-field="o.partner_id.commercial_partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;, &quot;vat&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                </div>
                            </div>
                            <br/>
                            <h1 t-field="o.name" class="mt0" style="color: #043665;"/>
                            <div class="row mt48 mb32 o_tcf_sc_picking_row">
                                <div t-if="o.origin" class="col-auto" name="div_origin">
                                    <strong>Order:</strong>
                                    <p t-field="o.origin"/>
                                </div>
                                <div class="col-auto" name="div_state">
                                    <strong>Status:</strong>
                                    <p t-field="o.state"/>
                                </div>
                                <div class="col-auto" name="div_sched_date">
                                    <strong>Scheduled Date:</strong>
                                    <p t-field="o.scheduled_date"/>
                                </div>
            <div t-if="o.picking_type_id.code == 'outgoing' and o.carrier_id" class="col-auto">
                <strong>Carrier:</strong>
                <p t-field="o.carrier_id"/>
            </div>
            <div t-if="o.weight" class="col-auto">
                <strong>Weight:</strong>
                <br/>
                <span t-field="o.weight"/>
                <span t-field="o.weight_uom_name"/>
            </div>
                            </div>
                            <table class="table table-sm" t-if="o.move_line_ids and o.move_ids_without_package">
                                <t t-set="has_barcode" t-value="any(move_line.product_id and move_line.product_id.sudo().barcode or move_line.package_id for move_line in o.move_line_ids)"/>
                                <t t-set="has_serial_number" t-value="any(move_line.lot_id or move_line.lot_name for move_line in o.move_line_ids)" groups="stock.group_production_lot"/>
                                <thead>
                                    <tr>
                                        <th name="th_product">
                                            <strong>Product</strong>
                                        </th>
    <th>
      <span>Special Code</span>
    </th>
                                        <th>
                                            <strong>Quantity</strong>
                                        </th>
                                        <th name="th_from" t-if="o.picking_type_id.code != 'incoming'" align="left" groups="stock.group_stock_multi_locations">
                                            <strong>From</strong>
                                        </th>
                                        <th name="th_to" t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">
                                            <strong>To</strong>
                                        </th>
                                        <th name="th_serial_number" class="text-center" t-if="has_serial_number">
                                           <strong>Lot/Serial Number</strong>
                                        </th>
                                        <th name="th_barcode" class="text-center" t-if="has_barcode">
                                            <strong>Product Barcode</strong>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!-- In case you come across duplicated lines, ask NIM or LAP -->
                                    <t t-foreach="o.move_line_ids_without_package" t-as="ml">
                                        <tr>
                                            <td>
                                                <span t-field="ml.product_id.display_name"/><br/>
                                                <span t-field="ml.product_id.description_picking"/>
                                            </td>
    <td>
      <span t-field="ml.x_studio_special_code_1"/>
    </td>
                                            <td>
                                                <span t-if="o.state != 'done'" t-field="ml.reserved_uom_qty"/>
                                                <span t-if="o.state == 'done'" t-field="ml.qty_done"/>
                                                <span t-field="ml.product_uom_id" groups="uom.group_uom"/>
                                            </td>
                                            <td t-if="o.picking_type_id.code != 'incoming'" groups="stock.group_stock_multi_locations">
                                                <span t-esc="ml.location_id.display_name"/>
                                                    <t t-if="ml.package_id">
                                                        <span t-field="ml.package_id"/>
                                                    </t>
                                            </td>
                                            <td t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">
                                                <div>
                                                    <span t-field="ml.location_dest_id"/>
                                                    <t t-if="ml.result_package_id">
                                                        <span t-field="ml.result_package_id"/>
                                                    </t>
                                                </div>
                                            </td>
                                            <td class=" text-center h6" t-if="has_serial_number">
                                                <div t-if="has_serial_number and (ml.lot_id or ml.lot_name)" t-esc="ml.lot_id.name or ml.lot_name" t-options="{'widget': 'barcode', 'humanreadable': 1, 'width': 400, 'height': 100, 'img_style': 'width:100%;height:35px;'}"/>
                                            </td>
                                            <td class="text-center" t-if="has_barcode">
                                                <t t-if="product_barcode != ml.product_id.barcode">
                                                    <span t-if="ml.product_id and ml.product_id.barcode">
                                                        <div t-field="ml.product_id.barcode" t-options="{'widget': 'barcode', 'symbology': 'auto', 'width': 400, 'height': 100, 'quiet': 0, 'img_style': 'height:35px;'}"/>
                                                    </span>
                                                    <t t-set="product_barcode" t-value="ml.product_id.barcode"/>
                                                </t>
                                            </td>
                                        </tr>
                                    </t>
                                  </tbody>
                            </table>
                            <table class="table table-sm" t-if="o.package_level_ids and o.picking_type_entire_packs and o.state in ['assigned', 'done']">
                                <thead>
                                    <tr>
                                        <th name="th_package">Package</th>
                                        <th name="th_pko_from" t-if="o.picking_type_id.code != 'incoming'" groups="stock.group_stock_multi_locations">From</th>
                                        <th name="th_pki_from" t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">To</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr t-foreach="o.package_level_ids.sorted(key=lambda p: p.package_id.name)" t-as="package">
                                        <t t-set="package" t-value="package.with_context(picking_id=o.id)"/>
                                        <td name="td_pk_barcode">
                                            <div t-field="package.package_id.name" t-options="{'widget': 'barcode', 'humanreadable': 1, 'width': 600, 'height': 100, 'img_style': 'width:300px;height:50px;margin-left: -50px;'}"/><br/>
                                        </td>
                                        <td t-if="o.picking_type_id.code != 'incoming'" groups="stock.group_stock_multi_locations">
                                            <span t-field="package.location_id"/>
                                        </td>
                                        <td t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">
                                            <span t-field="package.location_dest_id"/>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <t t-set="no_reserved_product" t-value="o.move_ids.filtered(lambda x: x.product_uom_qty != x.reserved_availability and x.move_line_ids and x.state!='done')"/>
                            <p t-if="o.state in ['draft', 'waiting', 'confirmed'] or no_reserved_product"><i class="fa fa-exclamation-triangle"/>
                                All products could not be reserved. Click on the "Check Availability" button to try to reserve products.
                            </p>
                            <p t-field="o.note"/>
                        </div>
                    </t>
                </t>
            </t>
        </t>"""

PICKING_SC_BASE_ARCH = """<t t-name="stock.report_picking_copy_1">
            <t t-call="web.html_container">
                <t t-foreach="docs" t-as="o">
                    <t t-call="web.external_layout">
                        <div class="page o_tcf_sc_picking1">
                            <style t-translation="off">
                                .o_tcf_sc_picking1 .o_tcf_sc_picking_row {
                                    display: -webkit-box !important;
                                    display: flex !important;
                                    -webkit-box-orient: horizontal !important;
                                    -webkit-box-pack: start !important;
                                    flex-wrap: wrap !important;
                                }
                                .o_tcf_sc_picking1 .o_tcf_sc_picking_row > div {
                                    margin-right: 96px !important;
                                }
                                .o_tcf_sc_picking1 .o_tcf_sc_picking_row > div strong,
                                .o_tcf_sc_picking1 .o_tcf_sc_picking_row > div p {
                                    display: block !important;
                                    margin: 0 !important;
                                }
                                .o_tcf_sc_picking1 table.table-sm thead th {
                                    color: #af1015 !important;
                                    font-weight: 700 !important;
                                    text-align: center !important;
                                    text-transform: uppercase !important;
                                }
                            </style>
                            <div class="row justify-content-end mb16">
                                <div class="col-4" name="right_box">
                                    <div t-field="o.name" t-options="{'widget': 'barcode', 'width': 600, 'height': 100, 'img_style': 'width:300px;height:50px;'}"/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-6" name="div_outgoing_address">
                                    <div t-if="o.should_print_delivery_address()">
                                        <span><strong>Delivery Address:</strong></span>
                                        <div t-field="o.move_ids[0].partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                    <div t-elif="o.picking_type_id.code != 'internal' and o.picking_type_id.warehouse_id.partner_id">
                                        <span><strong>Warehouse Address:</strong></span>
                                        <div t-field="o.picking_type_id.warehouse_id.partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                </div>
                                <div class="col-5 offset-1" name="div_incoming_address">
                                    <t t-set="show_partner" t-value="False"/>
                                    <div t-if="o.picking_type_id.code=='incoming' and o.partner_id">
                                        <span><strong>Vendor Address:</strong></span>
                                        <t t-set="show_partner" t-value="True"/>
                                    </div>
                                    <div t-if="o.picking_type_id.code=='internal' and o.partner_id">
                                        <span><strong>Warehouse Address:</strong></span>
                                        <t t-set="show_partner" t-value="True"/>
                                    </div>
                                    <div t-if="o.picking_type_id.code=='outgoing' and o.partner_id and o.partner_id != o.partner_id.commercial_partner_id">
                                        <span><strong>Customer Address:</strong></span>
                                        <t t-set="show_partner" t-value="True"/>
                                    </div>
                                    <div t-if="show_partner" name="partner_header">
                                        <div t-field="o.partner_id.commercial_partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;, &quot;vat&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                </div>
                            </div>
                            <br/>
                            <h1 t-field="o.name" class="mt0" style="color: #043665;"/>
                            <div class="row mt48 mb32 o_tcf_sc_picking_row">
                                <div t-if="o.origin" class="col-auto" name="div_origin">
                                    <strong>Order:</strong>
                                    <p t-field="o.origin"/>
                                </div>
                                <div class="col-auto" name="div_state">
                                    <strong>Status:</strong>
                                    <p t-field="o.state"/>
                                </div>
                                <div class="col-auto" name="div_sched_date">
                                    <strong>Scheduled Date:</strong>
                                    <p t-field="o.scheduled_date"/>
                                </div>
            <div t-if="o.picking_type_id.code == 'outgoing' and o.carrier_id" class="col-auto">
                <strong>Carrier:</strong>
                <p t-field="o.carrier_id"/>
            </div>
            <div t-if="o.weight" class="col-auto">
                <strong>Weight:</strong>
                <br/>
                <span t-field="o.weight"/>
                <span t-field="o.weight_uom_name"/>
            </div>
                            </div>
                            <table class="table table-sm" t-if="o.move_line_ids and o.move_ids">
                                <t t-set="has_barcode" t-value="any(move_line.product_id and move_line.product_id.sudo().barcode or move_line.package_id for move_line in o.move_line_ids)"/>
                                <t t-set="has_serial_number" t-value="any(move_line.lot_id or move_line.lot_name for move_line in o.move_line_ids)" groups="stock.group_production_lot"/>
                                <thead>
                                    <tr>
                                        <th name="th_product">
                                            <strong>Product</strong>
                                        </th>
                                        <th>
                                            <strong>Quantity</strong>
                                        </th>
                                        <th name="th_from" t-if="o.picking_type_id.code != 'incoming'" align="left" groups="stock.group_stock_multi_locations">
                                            <strong>From</strong>
                                        </th>
                                        <th name="th_to" t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">
                                            <strong>To</strong>
                                        </th>
                                        <th name="th_serial_number" class="text-center" t-if="has_serial_number">
                                           <strong>Lot/Serial Number</strong>
                                        </th>
                                        <th name="th_barcode" class="text-center" t-if="has_barcode">
                                            <strong>Product Barcode</strong>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!-- In case you come across duplicated lines, ask NIM or LAP -->
                                    <t t-foreach="o.move_line_ids" t-as="ml">
                                        <tr>
                                            <td>
                                                <span t-field="ml.product_id.display_name"/><br/>
                                                <span t-field="ml.product_id.description_picking"/>
                                            </td>
                                            <td>
                                                <span t-if="o.state != 'done'" t-field="ml.quantity"/>
                                                <span t-if="o.state == 'done'" t-field="ml.quantity"/>
                                                <span t-field="ml.product_uom_id" groups="uom.group_uom"/>
                                            </td>
                                            <td t-if="o.picking_type_id.code != 'incoming'" groups="stock.group_stock_multi_locations">
                                                <span t-esc="ml.location_id.display_name"/>
                                                    <t t-if="ml.package_id">
                                                        <span t-field="ml.package_id"/>
                                                    </t>
                                            </td>
                                            <td t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">
                                                <div>
                                                    <span t-field="ml.location_dest_id"/>
                                                    <t t-if="ml.result_package_id">
                                                        <span t-field="ml.result_package_id"/>
                                                    </t>
                                                </div>
                                            </td>
                                            <td class=" text-center h6" t-if="has_serial_number">
                                                <div t-if="has_serial_number and (ml.lot_id or ml.lot_name)" t-esc="ml.lot_id.name or ml.lot_name" t-options="{'widget': 'barcode', 'humanreadable': 1, 'width': 400, 'height': 100, 'img_style': 'width:100%;height:35px;'}"/>
                                            </td>
                                            <td class="text-center" t-if="has_barcode">
                                                <t t-if="product_barcode != ml.product_id.barcode">
                                                    <span t-if="ml.product_id and ml.product_id.barcode">
                                                        <div t-field="ml.product_id.barcode" t-options="{'widget': 'barcode', 'symbology': 'auto', 'width': 400, 'height': 100, 'quiet': 0, 'img_style': 'height:35px;'}"/>
                                                    </span>
                                                    <t t-set="product_barcode" t-value="ml.product_id.barcode"/>
                                                </t>
                                            </td>
                                        </tr>
                                    </t>
                                  </tbody>
                            </table>
<t t-set="no_reserved_product" t-value="o.move_ids.filtered(lambda x: x.product_uom_qty != x.quantity and x.move_line_ids and x.state!='done')"/>
                            <p t-if="o.state in ['draft', 'waiting', 'confirmed'] or no_reserved_product"><i class="fa fa-exclamation-triangle"/>
                                All products could not be reserved. Click on the "Check Availability" button to try to reserve products.
                            </p>
                            <p t-field="o.note"/>
                        </div>
                    </t>
                </t>
            </t>
        </t>"""

PICKING_SC_COPY1_COPY1_ARCH = """<t t-name="stock.report_picking_copy_1_copy_1_copy_1">
            <t t-call="web.html_container">
                <t t-foreach="docs" t-as="o">
                    <t t-call="web.external_layout">
                        <div class="page o_tcf_sc_picking3">
                            <style t-translation="off">
                                .o_tcf_sc_picking3 .o_tcf_sc_picking_row {
                                    display: -webkit-box !important;
                                    display: flex !important;
                                    -webkit-box-orient: horizontal !important;
                                    -webkit-box-pack: start !important;
                                    flex-wrap: wrap !important;
                                }
                                .o_tcf_sc_picking3 .o_tcf_sc_picking_row > div {
                                    margin-right: 96px !important;
                                }
                                .o_tcf_sc_picking3 .o_tcf_sc_picking_row > div strong,
                                .o_tcf_sc_picking3 .o_tcf_sc_picking_row > div p {
                                    display: block !important;
                                    margin: 0 !important;
                                }
                                .o_tcf_sc_picking3 table.table-sm thead th {
                                    color: #af1015 !important;
                                    font-weight: 700 !important;
                                    text-align: center !important;
                                    text-transform: uppercase !important;
                                }
                            </style>
                            <div class="row justify-content-end mb16">
                                <div class="col-4" name="right_box">
                                    <div t-field="o.name" t-options="{'widget': 'barcode', 'width': 600, 'height': 100, 'img_style': 'width:300px;height:50px;'}"/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-6" name="div_outgoing_address">
                                    <div t-if="o.should_print_delivery_address()">
                                        <span><strong>Delivery Address:</strong></span>
                                        <div t-field="o.move_ids[0].partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                    <div t-elif="o.picking_type_id.code != 'internal' and o.picking_type_id.warehouse_id.partner_id">
                                        <span><strong>Warehouse Address:</strong></span>
                                        <div t-field="o.picking_type_id.warehouse_id.partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                </div>
                                <div class="col-5 offset-1" name="div_incoming_address">
                                    <t t-set="show_partner" t-value="False"/>
                                    <div t-if="o.picking_type_id.code=='incoming' and o.partner_id">
                                        <span><strong>Vendor Address:</strong></span>
                                        <t t-set="show_partner" t-value="True"/>
                                    </div>
                                    <div t-if="o.picking_type_id.code=='internal' and o.partner_id">
                                        <span><strong>Warehouse Address:</strong></span>
                                        <t t-set="show_partner" t-value="True"/>
                                    </div>
                                    <div t-if="o.picking_type_id.code=='outgoing' and o.partner_id and o.partner_id != o.partner_id.commercial_partner_id">
                                        <span><strong>Customer Address:</strong></span>
                                        <t t-set="show_partner" t-value="True"/>
                                    </div>
                                    <div t-if="show_partner" name="partner_header">
                                        <div t-field="o.partner_id.commercial_partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;, &quot;vat&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                </div>
                            </div>
                            <br/>
                            <h1 t-field="o.name" class="mt0" style="color: #043665;"/>
                            <div class="row mt48 mb32 o_tcf_sc_picking_row">
                                <div t-if="o.origin" class="col-auto" name="div_origin">
                                    <strong>Order:</strong>
                                    <p t-field="o.origin"/>
                                </div>
                                <div class="col-auto" name="div_state">
                                    <strong>Status:</strong>
                                    <p t-field="o.state"/>
                                </div>
                                <div class="col-auto" name="div_sched_date">
                                    <strong>Scheduled Date:</strong>
                                    <p t-field="o.scheduled_date"/>
                                </div>
            <div t-if="o.picking_type_id.code == 'outgoing' and o.carrier_id" class="col-auto">
                <strong>Carrier:</strong>
                <p t-field="o.carrier_id"/>
            </div>
            <div t-if="o.weight" class="col-auto">
                <strong>Weight:</strong>
                <br/>
                <span t-field="o.weight"/>
                <span t-field="o.weight_uom_name"/>
            </div>
                            </div>
                            <table class="table table-sm" t-if="o.move_line_ids and o.move_ids">
                                <t t-set="has_barcode" t-value="any(move_line.product_id and move_line.product_id.sudo().barcode or move_line.package_id for move_line in o.move_line_ids)"/>
                                <t t-set="has_serial_number" t-value="any(move_line.lot_id or move_line.lot_name for move_line in o.move_line_ids)" groups="stock.group_production_lot"/>
                                <thead>
                                    <tr>
                                        <th name="th_product">
                                            <strong>Product</strong>
                                        </th>
    <th>
      <span>Special Code</span>
    </th>
                                        <th>
                                            <strong>Quantity</strong>
                                        </th>
                                        <th name="th_from" t-if="o.picking_type_id.code != 'incoming'" align="left" groups="stock.group_stock_multi_locations">
                                            <strong>From</strong>
                                        </th>
                                        <th name="th_to" t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">
                                            <strong>To</strong>
                                        </th>
                                        <th name="th_serial_number" class="text-center" t-if="has_serial_number">
                                           <strong>Lot/Serial Number</strong>
                                        </th>
                                        <th name="th_barcode" class="text-center" t-if="has_barcode">
                                            <strong>Product Barcode</strong>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!-- In case you come across duplicated lines, ask NIM or LAP -->
                                    <t t-foreach="o.move_line_ids" t-as="ml">
                                        <tr>
                                            <td>
                                                <span t-field="ml.product_id.display_name"/><br/>
                                                <span t-field="ml.product_id.description_picking"/>
                                            </td>
    <td>
      <span t-field="ml.special_code"/>
    </td>
                                            <td>
                                                <span t-if="o.state != 'done'" t-field="ml.quantity"/>
                                                <span t-if="o.state == 'done'" t-field="ml.quantity"/>
                                                <span t-field="ml.product_uom_id" groups="uom.group_uom"/>
                                            </td>
                                            <td t-if="o.picking_type_id.code != 'incoming'" groups="stock.group_stock_multi_locations">
                                                <span t-esc="ml.location_id.display_name"/>
                                                    <t t-if="ml.package_id">
                                                        <span t-field="ml.package_id"/>
                                                    </t>
                                            </td>
                                            <td t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">
                                                <div>
                                                    <span t-field="ml.location_dest_id"/>
                                                    <t t-if="ml.result_package_id">
                                                        <span t-field="ml.result_package_id"/>
                                                    </t>
                                                </div>
                                            </td>
                                            <td class=" text-center h6" t-if="has_serial_number">
                                                <div t-if="has_serial_number and (ml.lot_id or ml.lot_name)" t-esc="ml.lot_id.name or ml.lot_name" t-options="{'widget': 'barcode', 'humanreadable': 1, 'width': 400, 'height': 100, 'img_style': 'width:100%;height:35px;'}"/>
                                            </td>
                                            <td class="text-center" t-if="has_barcode">
                                                <t t-if="product_barcode != ml.product_id.barcode">
                                                    <span t-if="ml.product_id and ml.product_id.barcode">
                                                        <div t-field="ml.product_id.barcode" t-options="{'widget': 'barcode', 'symbology': 'auto', 'width': 400, 'height': 100, 'quiet': 0, 'img_style': 'height:35px;'}"/>
                                                    </span>
                                                    <t t-set="product_barcode" t-value="ml.product_id.barcode"/>
                                                </t>
                                            </td>
                                        </tr>
                                    </t>
                                  </tbody>
                            </table>
<t t-set="no_reserved_product" t-value="o.move_ids.filtered(lambda x: x.product_uom_qty != x.quantity and x.move_line_ids and x.state!='done')"/>
                            <p t-if="o.state in ['draft', 'waiting', 'confirmed'] or no_reserved_product"><i class="fa fa-exclamation-triangle"/>
                                All products could not be reserved. Click on the "Check Availability" button to try to reserve products.
                            </p>
                            <p t-field="o.note"/>
                        </div>
                    </t>
                </t>
            </t>
        </t>"""

DELIVERY_SC_ARCH = """<t t-name="stock.report_delivery_document_copy_1">
        <t t-call="web.html_container">
            <t t-call="web.external_layout">
                <t t-set="o" t-value="o.with_context(lang=o._get_report_lang())"/>
                <t t-set="partner" t-value="o.partner_id or (o.move_ids and o.move_ids[0].partner_id) or False"/>

                <t t-set="address">
                    <div name="div_outgoing_address">
                        <div name="outgoing_delivery_address" t-if="o.should_print_delivery_address()">
                            <span><strong>Delivery Address:</strong></span>
                            <div t-field="o.move_ids[0].partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                        </div>
                        <div name="outgoing_warehouse_address" t-elif="o.picking_type_id.code != 'internal' and o.picking_type_id.warehouse_id.partner_id">
                            <span><strong>Warehouse Address:</strong></span>
                            <div t-field="o.picking_type_id.warehouse_id.partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                        </div>
                    </div>
                </t>
                <t t-set="information_block">
                    <div class="row">
                        <div class="col-7" name="div_incoming_address">
                            <t t-set="show_partner" t-value="False"/>
                            <div name="vendor_address" t-if="o.picking_type_id.code=='incoming' and partner">
                                <span><strong>Vendor Address:</strong></span>
                                <t t-set="show_partner" t-value="True"/>
                            </div>
                            <div name="customer_address" t-if="o.picking_type_id.code=='outgoing' and partner and partner != partner.commercial_partner_id">
                                <span><strong>Customer Address:</strong></span>
                                <t t-set="show_partner" t-value="True"/>
                            </div>
                            <div t-if="show_partner" name="partner_header">
                                <div t-field="partner.commercial_partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;, &quot;vat&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                            </div>
                        </div>
                    </div>
                </t>
                <div class="page o_tcf_sc_deliveryslip">
                    <style t-translation="off">
                        .o_tcf_sc_deliveryslip .o_tcf_sc_header_row {
                            display: -webkit-box !important;
                            display: flex !important;
                            -webkit-box-orient: horizontal !important;
                            -webkit-box-pack: start !important;
                            flex-wrap: wrap !important;
                        }
                        .o_tcf_sc_deliveryslip .o_tcf_sc_header_row > div {
                            margin-right: 400px !important;
                        }
                        .o_tcf_sc_deliveryslip .o_tcf_sc_header_row > div strong,
                        .o_tcf_sc_deliveryslip .o_tcf_sc_header_row > div p {
                            display: block !important;
                            margin: 0 !important;
                        }
                        .o_tcf_sc_deliveryslip table[name='stock_move_line_table'] thead th,
                        .o_tcf_sc_deliveryslip table[name='stock_move_table'] thead th {
                            color: #af1015 !important;
                            text-align: center !important;
                            text-transform: uppercase !important;
                        }
                        .o_tcf_sc_deliveryslip table[name='stock_move_line_table'] tbody td:last-child,
                        .o_tcf_sc_deliveryslip table[name='stock_move_table'] tbody td:last-child {
                            background-color: #e9ecef !important;
                        }
                    </style>
                    <h2 style="color: #043665;">
                        <span t-field="o.name"/>
                    </h2>
                    <div class="row mt32 mb32 o_tcf_sc_header_row">
                        <div t-if="o.origin" class="col-auto" name="div_origin">
                            <strong>Order:</strong>
                            <p t-field="o.origin"/>
                        </div>
                        <div t-if="o.state" class="col-auto" name="div_sched_date">
                            <strong>Shipping Date:</strong>
                            <t t-if="o.state == 'done'">
                                <p t-field="o.date_done"/>
                            </t>
                            <t t-if="o.state != 'done'">
                                <p t-field="o.scheduled_date"/>
                           </t>
                        </div>
            <div t-if="o.picking_type_id.code == 'outgoing' and o.carrier_id" class="col-auto">
                <strong>Carrier:</strong>
                <p t-field="o.carrier_id"/>
            </div>
            <div t-if="o.shipping_weight" class="col-auto">
                <strong>Total Weight:</strong>
                <br/>
                <span t-field="o.shipping_weight"/>
                <span t-field="o.weight_uom_name"/>
            </div>
            <div t-if="o.carrier_tracking_ref" class="col-auto" style="max-width:30%;">
                <strong>Tracking Number:</strong>
                <p t-field="o.carrier_tracking_ref"/>
            </div>
            <t t-set="has_hs_code" t-value="o.move_ids.filtered(lambda l: l.product_id.hs_code)"/>
            <div class="col-auto justify-content-end" t-if="o.sudo().sale_id.client_order_ref">
                <strong>Customer Reference:</strong>
                <p t-field="o.sudo().sale_id.client_order_ref"/>
            </div>
                    </div>
                    <table class="table table-sm" t-if="o.state!='done'" name="stock_move_table">
                        <thead>
                            <tr>
                                <th name="th_sm_product"><strong>Product</strong></th>
                                <th name="th_sm_ordered"><strong>Ordered</strong></th>
                                <th name="th_sm_quantity"><strong>Delivered</strong></th>
            <th t-if="has_hs_code"><strong>HS Code</strong></th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-set="lines" t-value="o.move_ids.filtered(lambda x: x.product_uom_qty)"/>
                            <tr t-foreach="lines" t-as="move">
                                <td>
                                    <span t-field="move.product_id"/>
                                    <p t-if="move.description_picking != move.product_id.name and move.description_picking != move.product_id.display_name">
                                        <span t-field="move.description_picking"/>
                                    </p>
                                </td>
                                <td>
                                    <span t-field="move.product_uom_qty"/>
                                    <span t-field="move.product_uom"/>
                                </td>
                                <td>
                                    <span t-field="move.quantity"/>
                                    <span t-field="move.product_uom"/>
                                </td>
            <td t-if="has_hs_code">
                <span t-field="move.product_id.hs_code"/>
            </td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="table table-sm mt48" t-if="o.move_line_ids and o.state=='done'" name="stock_move_line_table">
                        <t t-set="has_serial_number" t-value="False"/>
                        <t t-set="has_serial_number" t-value="o.move_line_ids.mapped('lot_id')" groups="stock.group_lot_on_delivery_slip"/>
                        <thead>
                            <tr>
                                <th name="th_sml_product"><strong>Product</strong></th>
                                <t name="lot_serial" t-if="has_serial_number">
                                    <th>
                                        Lot/Serial Number
                                    </th>
                                </t>
            <t t-set="has_expiry_date" t-value="False"/>
            <t t-set="has_expiry_date" t-value="o.move_line_ids.filtered(lambda ml: ml.lot_id.expiration_date)" groups="product_expiry.group_expiry_date_on_delivery_slip"/>
            <t name="expiry_date" t-if="has_expiry_date">
                <th>Expiration Date</th>
            </t>
                                <th name="th_sml_qty_ordered" class="text-center" t-if="not has_serial_number">
                                    <strong>Ordered</strong>
                                </th>
                                <th name="th_sml_quantity" class="text-center"><strong>Delivered</strong></th>
            <th t-if="has_hs_code"><strong>HS Code</strong></th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-if="o.has_packages" name="has_packages">
                                <t t-set="packages" t-value="o.move_line_ids.mapped('result_package_id')"/>
                                <t t-foreach="packages" t-as="package">
                                    <t t-call="stock.stock_report_delivery_package_section_line_copy_1"/>
                                    <t t-set="package_move_lines" t-value="o.move_line_ids.filtered(lambda l: l.result_package_id == package)"/>
                                    <t t-if="has_serial_number">
                                        <tr t-foreach="package_move_lines" t-as="move_line">
                                            <t t-call="stock.stock_report_delivery_has_serial_move_line_copy_1"/>
                                        </tr>
                                    </t>
                                    <t t-else="">
                                        <t t-set="aggregated_lines" t-value="package_move_lines._get_aggregated_product_quantities(strict=True)"/>
                                        <t t-call="stock.stock_report_delivery_aggregated_move_lines_copy_1"/>
                                    </t>
                                </t>
                                <t t-set="move_lines" t-value="o.move_line_ids.filtered(lambda l: not l.result_package_id)"/>
                                <t t-set="aggregated_lines" t-value="o.move_line_ids._get_aggregated_product_quantities(except_package=True)"/>
                                <t t-if="move_lines or aggregated_lines" name="no_package_move_lines">
            <t t-set="has_kits" t-value="o.move_line_ids.filtered(lambda l: l.move_id.bom_line_id and l.move_id.bom_line_id.bom_id.type == 'phantom')"/>
            <t t-if="has_kits">
                <t t-set="move_lines" t-value="move_lines.filtered(lambda m: not m.move_id.bom_line_id)"/>
            </t>
                                    <t t-call="stock.stock_report_delivery_no_package_section_line_copy_1" name="no_package_section"/>
                                    <t t-if="has_serial_number">
                                        <tr t-foreach="move_lines" t-as="move_line">
                                            <t t-call="stock.stock_report_delivery_has_serial_move_line_copy_1"/>
                                        </tr>
                                    </t>
                                    <t t-elif="aggregated_lines">
                                        <t t-call="stock.stock_report_delivery_aggregated_move_lines_copy_1"/>
                                    </t>
            <t t-call="mrp.stock_report_delivery_kit_sections_copy_1"/>
                                </t>
                            </t>
            <t t-elif="has_kits and not has_packages">
                <t t-call="mrp.stock_report_delivery_kit_sections_copy_1"/>
                <t t-call="mrp.stock_report_delivery_no_kit_section_copy_1"/>
            </t>
                            <t t-else="">
                                <t t-if="has_serial_number">
                                    <tr t-foreach="o.move_line_ids" t-as="move_line">
                                        <t t-call="stock.stock_report_delivery_has_serial_move_line_copy_1"/>
                                    </tr>
                                </t>
                                <t t-else="" name="aggregated_move_lines">
                                    <t t-set="aggregated_lines" t-value="o.move_line_ids._get_aggregated_product_quantities()"/>
                                    <t t-call="stock.stock_report_delivery_aggregated_move_lines_copy_1"/>
                                </t>
                            </t>
                        </tbody>
                    </table>
                    <t t-set="backorders" t-value="o.backorder_ids.filtered(lambda x: x.state not in ('done', 'cancel'))"/>
                    <t t-if="o.backorder_ids and backorders">
                        <p class="mt-5">
                            <span>Remaining quantities not yet delivered:</span>
                        </p>
                        <table class="table table-sm" name="stock_backorder_table" style="table-layout: fixed;">
                            <thead>
                                <tr>
                                    <th name="th_sb_product"><strong>Product</strong></th>
                                    <th/>
                                    <th name="th_sb_quantity" class="text-center"><strong>Quantity</strong></th>
                                </tr>
                            </thead>
                            <tbody>
                                <t t-foreach="backorders" t-as="backorder">
                                    <t t-set="bo_lines" t-value="backorder.move_ids.filtered(lambda x: x.product_uom_qty)"/>
                                    <tr t-foreach="bo_lines" t-as="bo_line">
                                        <td class="w-auto">
                                            <span t-field="bo_line.product_id"/>
                                            <p t-if="bo_line.description_picking != bo_line.product_id.name and bo_line.description_picking != bo_line.product_id.display_name">
                                                <span t-field="bo_line.description_picking"/>
                                            </p>
                                        </td>
                                        <td/>
                                        <td class="text-center w-auto">
                                            <span t-field="bo_line.product_uom_qty"/>
                                            <span t-field="bo_line.product_uom"/>
                                        </td>
                                    </tr>
                                </t>
                            </tbody>
                        </table>
                    </t>

                    <div t-if="o.signature" class="mt32 ml64 mr4" name="signature">
                        <div class="offset-8">
                            <strong>Signature</strong>
                        </div>
                        <div class="offset-8">
                            <img t-att-src="image_data_uri(o.signature)" style="max-height: 4cm; max-width: 8cm;"/>
                        </div>
                        <div class="offset-8 text-center">
                            <p t-field="o.partner_id.name"/>
                        </div>
                    </div>
                </div>
            </t>
         </t>
    </t>"""


DELIVERY_SC_LAB_ARCH = """<t t-name="stock.report_delivery_document_copy_1_copy_1">
        <t t-call="web.html_container">
            <t t-call="web.external_layout">
                <t t-set="o" t-value="o.with_context(lang=o._get_report_lang())"/>
                <t t-set="partner" t-value="o.partner_id or (o.move_ids and o.move_ids[0].partner_id) or False"/>

                <t t-set="address">
                    <div name="div_outgoing_address">
                        <div name="outgoing_delivery_address" t-if="o.should_print_delivery_address()">
                            <span><strong>Delivery Address:</strong></span>
                            <div t-field="o.move_ids[0].partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                        </div>
                        <div name="outgoing_warehouse_address" t-elif="o.picking_type_id.code != 'internal' and o.picking_type_id.warehouse_id.partner_id">
                            <span><strong>Warehouse Address:</strong></span>
                            <div t-field="o.picking_type_id.warehouse_id.partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                        </div>
                    </div>
                </t>
                <t t-set="information_block">
                    <div class="row">
                        <div class="col-7" name="div_incoming_address">
                            <t t-set="show_partner" t-value="False"/>
                            <div name="vendor_address" t-if="o.picking_type_id.code=='incoming' and partner">
                                <span><strong>Vendor Address:</strong></span>
                                <t t-set="show_partner" t-value="True"/>
                            </div>
                            <div name="customer_address" t-if="o.picking_type_id.code=='outgoing' and partner and partner != partner.commercial_partner_id">
                                <span><strong>Customer Address:</strong></span>
                                <t t-set="show_partner" t-value="True"/>
                            </div>
                            <div t-if="show_partner" name="partner_header">
                                <div t-field="partner.commercial_partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;, &quot;vat&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                            </div>
                        </div>
                    </div>
                </t>
                <div class="page o_tcf_sc_deliveryslip_lab">
                    <style t-translation="off">
                        .o_tcf_sc_deliveryslip_lab .o_tcf_sc_header_row {
                            display: -webkit-box !important;
                            display: flex !important;
                            -webkit-box-orient: horizontal !important;
                            -webkit-box-pack: start !important;
                            flex-wrap: wrap !important;
                        }
                        .o_tcf_sc_deliveryslip_lab .o_tcf_sc_header_row > div {
                            margin-right: 400px !important;
                        }
                        .o_tcf_sc_deliveryslip_lab .o_tcf_sc_header_row > div strong,
                        .o_tcf_sc_deliveryslip_lab .o_tcf_sc_header_row > div p {
                            display: block !important;
                            margin: 0 !important;
                        }
                        .o_tcf_sc_deliveryslip_lab table[name='stock_move_line_table'] thead th,
                        .o_tcf_sc_deliveryslip_lab table[name='stock_move_table'] thead th {
                            color: #af1015 !important;
                            text-align: center !important;
                            text-transform: uppercase !important;
                        }
                        .o_tcf_sc_deliveryslip_lab table[name='stock_move_line_table'] tbody td:last-child,
                        .o_tcf_sc_deliveryslip_lab table[name='stock_move_table'] tbody td:last-child {
                            background-color: #e9ecef !important;
                        }
                    </style>
                    <h2 style="color: #043665;">
                        <span t-field="o.name"/>
                    </h2>
                    <div class="row mt32 mb32 o_tcf_sc_header_row">
                        <div t-if="o.origin" class="col-auto" name="div_origin">
                            <strong>Order:</strong>
                            <p t-field="o.origin"/>
                        </div>
                        <div t-if="o.state" class="col-auto" name="div_sched_date">
                            <strong>Shipping Date:</strong>
                            <t t-if="o.state == 'done'">
                                <p t-field="o.date_done"/>
                            </t>
                            <t t-if="o.state != 'done'">
                                <p t-field="o.scheduled_date"/>
                           </t>
                        </div>
            <div t-if="o.picking_type_id.code == 'outgoing' and o.carrier_id" class="col-auto">
                <strong>Carrier:</strong>
                <p t-field="o.carrier_id"/>
            </div>
            <div t-if="o.shipping_weight" class="col-auto">
                <strong>Total Weight:</strong>
                <br/>
                <span t-field="o.shipping_weight"/>
                <span t-field="o.weight_uom_name"/>
            </div>
            <div t-if="o.carrier_tracking_ref" class="col-auto" style="max-width:30%;">
                <strong>Tracking Number:</strong>
                <p t-field="o.carrier_tracking_ref"/>
            </div>
            <t t-set="has_hs_code" t-value="o.move_ids.filtered(lambda l: l.product_id.hs_code)"/>
            <div class="col-auto justify-content-end" t-if="o.sudo().sale_id.client_order_ref">
                <strong>Customer Reference:</strong>
                <p t-field="o.sudo().sale_id.client_order_ref"/>
            </div>
                    </div>
                    <table class="table table-sm" t-if="o.state!='done'" name="stock_move_table">
                        <thead>
                            <tr>
                                <th name="th_sm_product"><strong>Product</strong></th>
                                <th name="th_sm_ordered"><strong>Ordered</strong></th>
                                <th name="th_sm_quantity"><strong>Delivered</strong></th>
            <th t-if="has_hs_code"><strong>HS Code</strong></th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-set="lines" t-value="o.move_ids.filtered(lambda x: x.product_uom_qty)"/>
                            <tr t-foreach="lines" t-as="move">
                                <td>
                                    <span t-field="move.product_id"/>
                                    <p t-if="move.description_picking != move.product_id.name and move.description_picking != move.product_id.display_name">
                                        <span t-field="move.description_picking"/>
                                    </p>
                                </td>
                                <td>
                                    <span t-field="move.product_uom_qty"/>
                                    <span t-field="move.product_uom"/>
                                </td>
                                <td>
                                    <span t-field="move.quantity"/>
                                    <span t-field="move.product_uom"/>
                                </td>
            <td t-if="has_hs_code">
                <span t-field="move.product_id.hs_code"/>
            </td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="table table-sm mt48" t-if="o.move_line_ids and o.state=='done'" name="stock_move_line_table">
                        <t t-set="has_serial_number" t-value="False"/>
                        <t t-set="has_serial_number" t-value="o.move_line_ids.mapped('lot_id')" groups="stock.group_lot_on_delivery_slip"/>
                        <thead>
                            <tr>
                                <th name="th_sml_product"><strong>Product</strong></th>
                                <t name="lot_serial" t-if="has_serial_number">
                                    <th>
                                        Lot/Serial Number
                                    </th>
                                </t>
            <t t-set="has_expiry_date" t-value="False"/>
            <t t-set="has_expiry_date" t-value="o.move_line_ids.filtered(lambda ml: ml.lot_id.expiration_date)" groups="product_expiry.group_expiry_date_on_delivery_slip"/>
            <t name="expiry_date" t-if="has_expiry_date">
                <th>Expiration Date</th>
            </t>
                                <th name="th_sml_qty_ordered" class="text-center" t-if="not has_serial_number">
                                    <strong>Ordered</strong>
                                </th>
                                <th name="th_sml_quantity" class="text-center"><strong>Delivered</strong></th>
            <th t-if="has_hs_code"><strong>HS Code</strong></th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-if="o.has_packages" name="has_packages">
                                <t t-set="packages" t-value="o.move_line_ids.mapped('result_package_id')"/>
                                <t t-foreach="packages" t-as="package">
                                    <t t-call="stock.stock_report_delivery_package_section_line_copy_1_copy_1"/>
                                    <t t-set="package_move_lines" t-value="o.move_line_ids.filtered(lambda l: l.result_package_id == package)"/>
                                    <t t-if="has_serial_number">
                                        <tr t-foreach="package_move_lines" t-as="move_line">
                                            <t t-call="stock.stock_report_delivery_has_serial_move_line_copy_1_copy_1"/>
                                        </tr>
                                    </t>
                                    <t t-else="">
                                        <t t-set="aggregated_lines" t-value="package_move_lines._get_aggregated_product_quantities(strict=True)"/>
                                        <t t-call="stock.stock_report_delivery_aggregated_move_lines_copy_1_copy_1"/>
                                    </t>
                                </t>
                                <t t-set="move_lines" t-value="o.move_line_ids.filtered(lambda l: not l.result_package_id)"/>
                                <t t-set="aggregated_lines" t-value="o.move_line_ids._get_aggregated_product_quantities(except_package=True)"/>
                                <t t-if="move_lines or aggregated_lines" name="no_package_move_lines">
            <t t-set="has_kits" t-value="o.move_line_ids.filtered(lambda l: l.move_id.bom_line_id and l.move_id.bom_line_id.bom_id.type == 'phantom')"/>
            <t t-if="has_kits">
                <t t-set="move_lines" t-value="move_lines.filtered(lambda m: not m.move_id.bom_line_id)"/>
            </t>
                                    <t t-call="stock.stock_report_delivery_no_package_section_line_copy_1_copy_1" name="no_package_section"/>
                                    <t t-if="has_serial_number">
                                        <tr t-foreach="move_lines" t-as="move_line">
                                            <t t-call="stock.stock_report_delivery_has_serial_move_line_copy_1_copy_1"/>
                                        </tr>
                                    </t>
                                    <t t-elif="aggregated_lines">
                                        <t t-call="stock.stock_report_delivery_aggregated_move_lines_copy_1_copy_1"/>
                                    </t>
            <t t-call="mrp.stock_report_delivery_kit_sections_copy_1_copy_1"/>
                                </t>
                            </t>
            <t t-elif="has_kits and not has_packages">
                <t t-call="mrp.stock_report_delivery_kit_sections_copy_1_copy_1"/>
                <t t-call="mrp.stock_report_delivery_no_kit_section_copy_1_copy_1"/>
            </t>
                            <t t-else="">
                                <t t-if="has_serial_number">
                                    <tr t-foreach="o.move_line_ids" t-as="move_line">
                                        <t t-call="stock.stock_report_delivery_has_serial_move_line_copy_1_copy_1"/>
                                    </tr>
                                </t>
                                <t t-else="" name="aggregated_move_lines">
                                    <t t-set="aggregated_lines" t-value="o.move_line_ids._get_aggregated_product_quantities()"/>
                                    <t t-call="stock.stock_report_delivery_aggregated_move_lines_copy_1_copy_1"/>
                                </t>
                            </t>
                        </tbody>
                    </table>
                    <t t-set="backorders" t-value="o.backorder_ids.filtered(lambda x: x.state not in ('done', 'cancel'))"/>
                    <t t-if="o.backorder_ids and backorders">
                        <p class="mt-5">
                            <span>Remaining quantities not yet delivered:</span>
                        </p>
                        <table class="table table-sm" name="stock_backorder_table" style="table-layout: fixed;">
                            <thead>
                                <tr>
                                    <th name="th_sb_product"><strong>Product</strong></th>
                                    <th/>
                                    <th name="th_sb_quantity" class="text-center"><strong>Quantity</strong></th>
                                </tr>
                            </thead>
                            <tbody>
                                <t t-foreach="backorders" t-as="backorder">
                                    <t t-set="bo_lines" t-value="backorder.move_ids.filtered(lambda x: x.product_uom_qty)"/>
                                    <tr t-foreach="bo_lines" t-as="bo_line">
                                        <td class="w-auto">
                                            <span t-field="bo_line.product_id"/>
                                            <p t-if="bo_line.description_picking != bo_line.product_id.name and bo_line.description_picking != bo_line.product_id.display_name">
                                                <span t-field="bo_line.description_picking"/>
                                            </p>
                                        </td>
                                        <td/>
                                        <td class="text-center w-auto">
                                            <span t-field="bo_line.product_uom_qty"/>
                                            <span t-field="bo_line.product_uom"/>
                                        </td>
                                    </tr>
                                </t>
                            </tbody>
                        </table>
                    </t>

                    <div t-if="o.signature" class="mt32 ml64 mr4" name="signature">
                        <div class="offset-8">
                            <strong>Signature</strong>
                        </div>
                        <div class="offset-8">
                            <img t-att-src="image_data_uri(o.signature)" style="max-height: 4cm; max-width: 8cm;"/>
                        </div>
                        <div class="offset-8 text-center">
                            <p t-field="o.partner_id.name"/>
                        </div>
                    </div>
                </div>
            </t>
         </t>
    </t>"""


DELIVERY_SC_MAN_ARCH = """<t t-name="stock.report_delivery_document_copy_1_copy_1_copy_1">
        <t t-call="web.html_container">
            <t t-call="web.external_layout">
                <t t-set="o" t-value="o.with_context(lang=o._get_report_lang())"/>
                <t t-set="partner" t-value="o.partner_id or (o.move_ids and o.move_ids[0].partner_id) or False"/>

                <t t-set="address">
                    <div name="div_outgoing_address">
                        <div name="outgoing_delivery_address" t-if="o.should_print_delivery_address()">
                            <span><strong>Delivery Address:</strong></span>
                            <div t-field="o.move_ids[0].partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                        </div>
                        <div name="outgoing_warehouse_address" t-elif="o.picking_type_id.code != 'internal' and o.picking_type_id.warehouse_id.partner_id">
                            <span><strong>Warehouse Address:</strong></span>
                            <div t-field="o.picking_type_id.warehouse_id.partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                        </div>
                    </div>
                </t>
                <t t-set="information_block">
                    <div class="row">
                        <div class="col-7" name="div_incoming_address">
                            <t t-set="show_partner" t-value="False"/>
                            <div name="vendor_address" t-if="o.picking_type_id.code=='incoming' and partner">
                                <span><strong>Vendor Address:</strong></span>
                                <t t-set="show_partner" t-value="True"/>
                            </div>
                            <div name="customer_address" t-if="o.picking_type_id.code=='outgoing' and partner and partner != partner.commercial_partner_id">
                                <span><strong>Customer Address:</strong></span>
                                <t t-set="show_partner" t-value="True"/>
                            </div>
                            <div t-if="show_partner" name="partner_header">
                                <div t-field="partner.commercial_partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;, &quot;vat&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                            </div>
                        </div>
                    </div>
                </t>
                <div class="page o_tcf_sc_deliveryslip_man">
                    <style t-translation="off">
                        .o_tcf_sc_deliveryslip_man .o_tcf_sc_header_row {
                            display: -webkit-box !important;
                            display: flex !important;
                            -webkit-box-orient: horizontal !important;
                            -webkit-box-pack: start !important;
                            flex-wrap: wrap !important;
                        }
                        .o_tcf_sc_deliveryslip_man .o_tcf_sc_header_row > div {
                            margin-right: 400px !important;
                        }
                        .o_tcf_sc_deliveryslip_man .o_tcf_sc_header_row > div strong,
                        .o_tcf_sc_deliveryslip_man .o_tcf_sc_header_row > div p {
                            display: block !important;
                            margin: 0 !important;
                        }
                        .o_tcf_sc_deliveryslip_man table[name='stock_move_line_table'] thead th,
                        .o_tcf_sc_deliveryslip_man table[name='stock_move_table'] thead th {
                            color: #af1015 !important;
                            text-align: center !important;
                            text-transform: uppercase !important;
                        }
                        .o_tcf_sc_deliveryslip_man table[name='stock_move_line_table'] tbody td:last-child,
                        .o_tcf_sc_deliveryslip_man table[name='stock_move_table'] tbody td:last-child {
                            background-color: #e9ecef !important;
                        }
                    </style>
                    <h2 style="color: #043665;">
                        <span t-field="o.name"/>
                    </h2>
                    <div class="row mt32 mb32 o_tcf_sc_header_row">
                        <div t-if="o.origin" class="col-auto" name="div_origin">
                            <strong>Order:</strong>
                            <p t-field="o.origin"/>
                        </div>
                        <div t-if="o.state" class="col-auto" name="div_sched_date">
                            <strong>Shipping Date:</strong>
                            <t t-if="o.state == 'done'">
                                <p t-field="o.date_done"/>
                            </t>
                            <t t-if="o.state != 'done'">
                                <p t-field="o.scheduled_date"/>
                           </t>
                        </div>
            <div t-if="o.picking_type_id.code == 'outgoing' and o.carrier_id" class="col-auto">
                <strong>Carrier:</strong>
                <p t-field="o.carrier_id"/>
            </div>
            <div t-if="o.shipping_weight" class="col-auto">
                <strong>Total Weight:</strong>
                <br/>
                <span t-field="o.shipping_weight"/>
                <span t-field="o.weight_uom_name"/>
            </div>
            <div t-if="o.carrier_tracking_ref" class="col-auto" style="max-width:30%;">
                <strong>Tracking Number:</strong>
                <p t-field="o.carrier_tracking_ref"/>
            </div>
            <t t-set="has_hs_code" t-value="o.move_ids.filtered(lambda l: l.product_id.hs_code)"/>
            <div class="col-auto justify-content-end" t-if="o.sudo().sale_id.client_order_ref">
                <strong>Customer Reference:</strong>
                <p t-field="o.sudo().sale_id.client_order_ref"/>
            </div>
                    </div>
                    <table class="table table-sm" t-if="o.state!='done'" name="stock_move_table">
                        <thead>
                            <tr>
    <th>
      <span>NO</span>
  </th>
                                <th name="th_sm_product"><strong>ÜRÜN</strong>
  </th>
    <th>
      <span>ADRES</span>
  </th>
    <th>
      <span>Special Code</span>
    </th>
                                <th name="th_sm_ordered"><strong>MİKTAR</strong>
  </th>
                                <th t-if="has_hs_code"><strong>HS Code</strong></th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-set="lines" t-value="o.move_ids.filtered(lambda x: x.product_uom_qty)"/>
                            <tr t-foreach="lines" t-as="move">
    <td>
      <span t-field="move.number"/>
    </td>
                                <td>
                                    <span t-field="move.product_id"/>
                                    <p t-if="move.description_picking != move.product_id.name and move.description_picking != move.product_id.display_name">
                                        <span t-field="move.description_picking"/>
                                    </p>
                                </td>
    <td>
      <span t-field="move.move_line_ids.location_id"/>
    </td>
    <td>
      <span t-esc="move.move_line_ids[:1].special_code if move.move_line_ids else False"/>
    </td>
                                <td>
                                    <span t-field="move.product_uom_qty"/>
                                    <span t-field="move.product_uom"/>
                                </td>
                                <td t-if="has_hs_code">
                <span t-field="move.product_id.hs_code"/>
            </td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="table table-sm mt48" t-if="o.move_line_ids and o.state=='done'" name="stock_move_line_table">
                        <t t-set="has_serial_number" t-value="False"/>
                        <t t-set="has_serial_number" t-value="o.move_line_ids.mapped('lot_id')" groups="stock.group_lot_on_delivery_slip"/>
                        <thead>
                            <tr>
                                <th name="th_sml_product"><strong>Product</strong></th>
                                <t name="lot_serial" t-if="has_serial_number">
                                    <th>
                                        Lot/Serial Number
                                    </th>
                                </t>
            <t t-set="has_expiry_date" t-value="False"/>
            <t t-set="has_expiry_date" t-value="o.move_line_ids.filtered(lambda ml: ml.lot_id.expiration_date)" groups="product_expiry.group_expiry_date_on_delivery_slip"/>
            <t name="expiry_date" t-if="has_expiry_date">
                <th>Expiration Date</th>
            </t>
                                <th name="th_sml_qty_ordered" class="text-center" t-if="not has_serial_number">
                                    <strong>Ordered</strong>
                                </th>
                                <th name="th_sml_quantity" class="text-center"><strong>Delivered</strong></th>
            <th t-if="has_hs_code"><strong>HS Code</strong></th>
                            </tr>
                        </thead>
                        <tbody>
                        <!-- This part gets complicated with different use cases (additional use cases in extensions of this report):
                                1. If serial numbers are used and set to print on delivery slip => print lines as is, otherwise group them by overlapping
                                    product + description + uom combinations
                                2. If any packages are assigned => split products up by package (or non-package) and then apply use case 1 -->
                            <!-- If has destination packages => create sections of corresponding products -->
            <!-- get only the top level kits' (i.e. no subkit) move lines for easier mapping later on + we ignore subkit groupings-->
            <!-- note that move.name uses top level kit's product.template.display_name value instead of product.template.name -->
            <t t-set="has_kits" t-value="o.move_line_ids.filtered(lambda l: l.move_id.bom_line_id and l.move_id.bom_line_id.bom_id.type == 'phantom')"/>
                            <t t-if="o.has_packages" name="has_packages">
                                <t t-set="packages" t-value="o.move_line_ids.mapped('result_package_id')"/>
                                <t t-foreach="packages" t-as="package">
                                    <t t-call="stock.stock_report_delivery_package_section_line_copy_1_copy_1_copy_1"/>
                                    <t t-set="package_move_lines" t-value="o.move_line_ids.filtered(lambda l: l.result_package_id == package)"/>
                                    <!-- If printing lots/serial numbers => keep products in original lines -->
                                    <t t-if="has_serial_number">
                                        <tr t-foreach="package_move_lines" t-as="move_line">
                                            <t t-call="stock.stock_report_delivery_has_serial_move_line_copy_1_copy_1_copy_1"/>
                                        </tr>
                                    </t>
                                    <!-- If not printing lots/serial numbers => merge lines with same product+description+uom -->
                                    <t t-else="">
                                        <t t-set="aggregated_lines" t-value="package_move_lines._get_aggregated_product_quantities(strict=True)"/>
                                        <t t-call="stock.stock_report_delivery_aggregated_move_lines_copy_1_copy_1_copy_1"/>
                                    </t>
                                </t>
                                <!-- Make sure we do another section for package-less products if they exist -->
                                <t t-set="move_lines" t-value="o.move_line_ids.filtered(lambda l: not l.result_package_id)"/>
                                <t t-set="aggregated_lines" t-value="o.move_line_ids._get_aggregated_product_quantities(except_package=True)"/>
                                <t t-if="move_lines or aggregated_lines" name="no_package_move_lines">
            <t t-set="has_kits" t-value="o.move_line_ids.filtered(lambda l: l.move_id.bom_line_id and l.move_id.bom_line_id.bom_id.type == 'phantom')"/>
            <t t-if="has_kits">
                <!-- print the products not in a package or kit first -->
                <t t-set="move_lines" t-value="move_lines.filtered(lambda m: not m.move_id.bom_line_id)"/>
            </t>
                                    <t t-call="stock.stock_report_delivery_no_package_section_line_copy_1_copy_1_copy_1" name="no_package_section"/>
                                    <t t-if="has_serial_number">
                                        <tr t-foreach="move_lines" t-as="move_line">
                                            <t t-call="stock.stock_report_delivery_has_serial_move_line_copy_1_copy_1_copy_1"/>
                                        </tr>
                                    </t>
                                    <t t-elif="aggregated_lines">
                                        <t t-call="stock.stock_report_delivery_aggregated_move_lines_copy_1_copy_1_copy_1"/>
                                    </t>
            <t t-call="mrp.stock_report_delivery_kit_sections_copy_1_copy_1_copy_1"/>
                                </t>
                            </t>
            <!-- Additional use case: group by kits when no packages exist and then apply use case 1. (serial/lot numbers used/printed) -->
            <t t-elif="has_kits and not has_packages">
                <t t-call="mrp.stock_report_delivery_kit_sections_copy_1_copy_1_copy_1"/>
                <t t-call="mrp.stock_report_delivery_no_kit_section_copy_1_copy_1_copy_1"/>
            </t>
                            <!-- No destination packages -->
                            <t t-else="">
                                <!-- If printing lots/serial numbers => keep products in original lines -->
                                <t t-if="has_serial_number">
                                    <tr t-foreach="o.move_line_ids" t-as="move_line">
                                        <t t-call="stock.stock_report_delivery_has_serial_move_line_copy_1_copy_1_copy_1"/>
                                    </tr>
                                </t>
                                <!-- If not printing lots/serial numbers => merge lines with same product -->
                                <t t-else="" name="aggregated_move_lines">
                                    <t t-set="aggregated_lines" t-value="o.move_line_ids._get_aggregated_product_quantities()"/>
                                    <t t-call="stock.stock_report_delivery_aggregated_move_lines_copy_1_copy_1_copy_1"/>
                                </t>
                            </t>
                        </tbody>
                    </table>
                    <t t-set="backorders" t-value="o.backorder_ids.filtered(lambda x: x.state not in ('done', 'cancel'))"/>
                    <t t-if="o.backorder_ids and backorders">
                        <p class="mt-5">
                            <span>Remaining quantities not yet delivered:</span>
                        </p>
                        <table class="table table-sm" name="stock_backorder_table" style="table-layout: fixed;">
                            <thead>
                                <tr>
                                    <th name="th_sb_product"><strong>Product</strong></th>
                                    <th/>
                                    <th name="th_sb_quantity" class="text-center"><strong>Quantity</strong></th>
                                </tr>
                            </thead>
                            <tbody>
                                <t t-foreach="backorders" t-as="backorder">
                                    <t t-set="bo_lines" t-value="backorder.move_ids.filtered(lambda x: x.product_uom_qty)"/>
                                    <tr t-foreach="bo_lines" t-as="bo_line">
                                        <td class="w-auto">
                                            <span t-field="bo_line.product_id"/>
                                            <p t-if="bo_line.description_picking != bo_line.product_id.name and bo_line.description_picking != bo_line.product_id.display_name">
                                                <span t-field="bo_line.description_picking"/>
                                            </p>
                                        </td>
                                        <td/>
                                        <td class="text-center w-auto">
                                            <span t-field="bo_line.product_uom_qty"/>
                                            <span t-field="bo_line.product_uom"/>
                                        </td>
                                    </tr>
                                </t>
                            </tbody>
                        </table>
                    </t>

                    <div t-if="o.signature" class="mt32 ml64 mr4" name="signature">
                        <div class="offset-8">
                            <strong>Signature</strong>
                        </div>
                        <div class="offset-8">
                            <img t-att-src="image_data_uri(o.signature)" style="max-height: 4cm; max-width: 8cm;"/>
                        </div>
                        <div class="offset-8 text-center">
                            <p t-field="o.partner_id.name"/>
                        </div>
                    </div>
                </div>
            </t>
         </t>
    </t>"""


REPORT_BY_PACKAGE_COPY1_ARCH = """<t t-name="smartr_multi_level_pack.report_products_id_package_copy_1">
            <t t-call="web.html_container">
                <t t-call="web.external_layout">
                    <t t-foreach="docs" t-as="o">
                        <t t-set="o" t-value="o.with_context(lang=o.partner_id.lang)"/>
                        <t t-set="partner" t-value="o.partner_id or (o.move_ids and o.move_ids[0].partner_id) or False"/>

                        <t t-set="address">
                            <div name="div_outgoing_address">
                                <div name="outgoing_delivery_address" t-if="o.should_print_delivery_address()">
                                    <span>
                                        <strong>Delivery Address:</strong>
                                    </span>
                                    <div t-field="o.move_ids[0].partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                </div>
                                <div name="outgoing_warehouse_address" t-elif="o.picking_type_id.code != 'internal' and o.picking_type_id.warehouse_id.partner_id">
                                    <span>
                                        <strong>Warehouse Address:</strong>
                                    </span>
                                    <div t-field="o.picking_type_id.warehouse_id.partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                </div>
                            </div>
                        </t>
                        <t t-set="information_block">
                            <div class="row">
                                <div class="col-7" name="div_incoming_address">
                                    <div name="vendor_address" t-if="o.picking_type_id.code=='incoming' and partner">
                                        <span>
                                            <strong>Vendor Address:</strong>
                                        </span>
                                    </div>
                                    <div name="warehouse_address" t-if="o.picking_type_id.code=='internal' and partner">
                                        <span>
                                            <strong>Warehouse Address:</strong>
                                        </span>
                                    </div>
                                    <div name="customer_address" t-if="o.picking_type_id.code=='outgoing' and partner">
                                        <span>
                                            <strong>Customer Address:</strong>
                                        </span>
                                    </div>
                                    <div t-if="partner" name="partner_header">
                                        <div t-field="partner.commercial_partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;, &quot;vat&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/>
                                    </div>
                                </div>
                            </div>
                        </t>
                        <div class="page o_tcf_report_by_package_copy1">
                            <style t-translation="off">
                                .o_tcf_report_by_package_copy1 .o_tcf_header_row {
                                    display: -webkit-box !important;
                                    display: flex !important;
                                    -webkit-box-orient: horizontal !important;
                                    -webkit-box-pack: start !important;
                                    flex-wrap: wrap !important;
                                }
                                .o_tcf_report_by_package_copy1 .o_tcf_header_row > div {
                                    margin-right: 48px !important;
                                }
                                .o_tcf_report_by_package_copy1 .o_tcf_header_row > div strong,
                                .o_tcf_report_by_package_copy1 .o_tcf_header_row > div p {
                                    display: block !important;
                                    margin: 0 !important;
                                    font-weight: 700 !important;
                                }
                                .o_tcf_report_by_package_copy1 table.table-condensed thead th,
                                .o_tcf_report_by_package_copy1 table.table-condensed thead th strong {
                                    color: #af1015 !important;
                                    font-weight: 700 !important;
                                    text-align: center !important;
                                    text-transform: uppercase !important;
                                }
                            </style>
                            <h2 style="color: #043665; font-weight: 700;">
                                <span t-field="o.name"/>
                            </h2>
                            <div class="row mt32 mb32 o_tcf_header_row">
                                <div t-if="o.origin" class="col-auto" name="div_origin">
                                    <strong>Order:</strong>
                                    <p t-field="o.origin"/>
                                </div>
                                <div t-if="o.state" class="col-auto" name="div_sched_date">
                                    <strong>Shipping Date:</strong>
                                    <t t-if="o.state == 'done'">
                                        <p t-field="o.date_done"/>
                                    </t>
                                    <t t-if="o.state != 'done'">
                                        <p t-field="o.scheduled_date"/>
                                    </t>
                                </div>
                            </div>
                            <table class="table table-condensed" style="border: 3px solid black !important;">
                                <thead>
                                    <th name="" class="text-center">
                                        <strong>BOX NO.</strong>
                                    </th>
                                    <th name="" class="text-center">
                                        <strong>Net Weight Kilo</strong>
                                    </th>
                                    <th name="" class="text-center">
                                        <strong>Packing</strong>
                                    </th>
                                    <th name="" class="text-center">
                                        <strong>Product Code</strong>
                                    </th>
                                    <th name="" class="text-center">
                                        <strong>Item Description</strong>
                                    </th>
                                    <th name="" class="text-center">
                                        <strong>Comment</strong>
                                    </th>
                                    <th name="" class="text-center">
                                        <strong>Gross Weight Kilo</strong>
                                    </th>
                                </thead>
                                <t t-set="num_child" t-value="0"/>
                                <t t-set="records" t-value="o.parent_package_ids"/>
                                <t t-set="num_parent" t-value="0"/>
                                <t t-foreach="records" t-as="parent">
                                    <t t-set="num_parent" t-value="num_parent + 1"/>

                                    <tr>

                                        <td name="parent.parent_package_id" class="text-center" colspan="6">

                                            <strong class="text-center">
                                                <span t-field="parent.pallet_display_name"/>
                                            </strong>
                                        </td>
                                        <td name="parent.parent_package_id" class="text-center">
                                            <strong class="text-center">
                                                <span t-field="parent.package_type_id.base_weight"/>
                                            </strong>
                                        </td>
                                    </tr>
                                    <t t-set="package_ids" t-value="o.package_ids"/>

                                    <t t-foreach="package_ids" t-as="child">

                                        <t t-if="child.parent_package_id.id == parent.id">

                                            <t t-set="num_child" t-value="num_child + 1"/>
                                            <t t-set="quant_no" t-value="1"/>
                                            <t t-foreach="child.quant_ids" t-as="quant_id">

                                                <tr>
                                                    <td class="text-center">
                                                        <span t-field="child.name"/>
                                                    </td>
                                                    <td class="text-center">
                                                        <span t-field="quant_id.weight"/>
                                                    </td>
                                                    <td class="text-center">
                                                        </td>
                                                    <td class="text-center">
                                                        <span t-field="quant_id.special_code"/>
                                                    </td>
                                                    <td class="text-left">

                                                        <t t-set="name" t-value="quant_id.product_id.name + '    1 ' + quant_id.product_uom_id.name"/>
                                                        <span t-esc="name"/>
                                                    </td>
                                                    <td>
                                                    </td>
                                                    <td class="text-center">
                                                        <t t-if="quant_no">
                                                            <span t-field="child.shipping_weight"/>
                                                        </t>
                                                    </td>
                                                </tr>
                                                <t t-set="quant_no" t-value="0"/>
                                            </t>
                                        </t>

                                    </t>
                                </t>
                            </table>
                            <strong>No. of Pallets :</strong>
                            <span t-esc="num_parent"/>
                            <br/>
                            <strong>No. of Boxes :</strong>
                            <span t-esc="num_child"/>
                            <br/>
                            <strong>Total Net Weight:</strong>
                            <span t-field="o.total_net_weight"/>
                            <br/>
                            <strong>Total Gross Weight:</strong>
                            <span t-field="o.total_gross_weight"/>
                            <br/>
                            <strong>Tare Pallets Weight:</strong>
                            <span t-field="o.total_pallets_weight"/>
                            <br/>
                            <strong>Total Gross Weight including Pallets</strong>
                            <span t-field="o.total_pallets_weight_inc"/>
                        </div>
                    </t>
                </t>
            </t>
        </t>"""


PICKING_COPY2_IRFAN_ARCH = """<t t-name="stock.report_picking_copy_2">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="o">
            <t t-call="web.external_layout">
                <div class="page o_tcf_sc_picking_irfan">
                    <style t-translation="off">
                        .o_tcf_sc_picking_irfan .o_tcf_sc_picking_row {
                            display: -webkit-box !important;
                            display: flex !important;
                            -webkit-box-orient: horizontal !important;
                            -webkit-box-pack: start !important;
                            flex-wrap: wrap !important;
                        }
                        .o_tcf_sc_picking_irfan .o_tcf_sc_picking_row > div {
                            margin-right: 48px !important;
                        }
                        .o_tcf_sc_picking_irfan .o_tcf_sc_picking_row > div strong,
                        .o_tcf_sc_picking_irfan .o_tcf_sc_picking_row > div p {
                            display: block !important;
                            margin: 0 !important;
                        }
                        .o_tcf_sc_picking_irfan table.table-sm thead th {
                            color: #af1015 !important;
                            font-weight: 700 !important;
                            text-align: center !important;
                            text-transform: uppercase !important;
                        }
                        .o_tcf_sc_picking_irfan .o_underline {
                            text-decoration: underline !important;
                        }
                        .o_tcf_sc_picking_irfan table.table-sm tbody td:last-child {
                            background-color: #e9ecef !important;
                        }
                    </style>
                    <div class="row justify-content-end mb16">
                        <div class="col-4" name="right_box">
                            <div t-field="o.name" t-options="{'widget': 'barcode', 'width': 600, 'height': 100, 'img_style': 'width:300px;height:50px;'}"/></div>
                    </div>
                    <div class="row">
                        <div class="col-6" name="div_outgoing_address">
                            <div t-if="o.should_print_delivery_address()">
                                <span>
                                    <strong>Delivery Address:</strong>
                                </span>
                                <div t-field="o.move_ids[0].partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/></div>
                            <div t-elif="o.picking_type_id.code != 'internal' and o.picking_type_id.warehouse_id.partner_id">
                                <span>
                                    <strong>Warehouse Address:</strong>
                                </span>
                                <div t-field="o.picking_type_id.warehouse_id.partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/></div>
                        </div>
                        <div class="col-5 offset-1" name="div_incoming_address">
                            <t t-set="show_partner" t-value="False"/>
                            <div t-if="o.picking_type_id.code=='incoming' and o.partner_id">
                                <span>
                                    <strong>Vendor Address:</strong>
                                </span>
                                <t t-set="show_partner" t-value="True"/>
                            </div>
                            <div t-if="o.picking_type_id.code=='internal' and o.partner_id">
                                <span>
                                    <strong>Warehouse Address:</strong>
                                </span>
                                <t t-set="show_partner" t-value="True"/>
                            </div>
                            <div t-if="o.picking_type_id.code=='outgoing' and o.partner_id and o.partner_id != o.partner_id.commercial_partner_id">
                                <span>
                                    <strong>Customer Address:</strong>
                                </span>
                                <t t-set="show_partner" t-value="True"/>
                            </div>
                            <div t-if="show_partner" name="partner_header">
                                <div t-field="o.partner_id.commercial_partner_id" t-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;, &quot;phone&quot;, &quot;vat&quot;], &quot;no_marker&quot;: True, &quot;phone_icons&quot;: True}"/></div>
                        </div>
                    </div>
                    <br/>
                    <h1 t-field="o.name" class="mt0" style="color: #043665;"/>
                    <div class="row mt48 mb32 o_tcf_sc_picking_row">
                        <div t-if="o.origin" class="col-auto" name="div_origin">
                            <strong>Order:</strong>
                            <p t-field="o.origin" class="o_underline"/>
                        </div>
                        <div class="col-auto" name="div_state">
                            <strong>Status:</strong>
                            <p t-field="o.state"/>
                        </div>
                        <div class="col-auto" name="div_sched_date">
                            <strong>Scheduled Date:</strong>
                            <p t-field="o.scheduled_date"/>
                        </div>
                        <div t-if="o.picking_type_id.code == 'outgoing' and o.carrier_id" class="col-auto">
                            <strong>Carrier:</strong>
                            <p t-field="o.carrier_id"/>
                        </div>
                        <div t-if="o.weight" class="col-auto">
                            <strong>Weight:</strong>
                            <br/>
                            <span t-field="o.weight"/>
                            <span t-field="o.weight_uom_name"/>
                        </div>
                    </div>
                    <table class="table table-sm" t-if="o.move_line_ids and o.move_ids">
                        <t t-set="has_barcode" t-value="any(move_line.product_id and move_line.product_id.sudo().barcode or move_line.package_id for move_line in o.move_line_ids)"/>
                        <t t-set="has_serial_number" t-value="any(move_line.lot_id or move_line.lot_name for move_line in o.move_line_ids)" groups="stock.group_production_lot"/>
                        <thead>
                            <tr>
                                <th name="th_product">
                                    <strong>Product</strong>
                                </th>
                                <th>
                                    <strong>Quantity</strong>
                                </th>
                                <th name="th_from" t-if="o.picking_type_id.code != 'incoming'" align="left" groups="stock.group_stock_multi_locations">
                                    <strong>From</strong>
                                </th>
                                <th name="th_to" t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">
                                    <strong>To</strong>
                                </th>
                                <th name="th_serial_number" class="text-center" t-if="has_serial_number">
                                    <strong>Lot/Serial Number</strong>
                                </th>
                                <th name="th_barcode" class="text-center" t-if="has_barcode">
                                    <strong>Product Barcode</strong>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- In case you come across duplicated lines, ask NIM or LAP -->
                            <t t-foreach="o.move_line_ids.sorted(key=lambda ml: ml.location_id.id)" t-as="ml">
                                <tr>
                                    <td>
                                        <span t-field="ml.product_id.display_name"/>
                                        <br/>
                                        <span t-field="ml.product_id.description_picking"/>
                                    </td>
                                    <td>
                                        <span t-if="o.state != 'done'" t-field="ml.quantity"/>
                                        <span t-if="o.state == 'done'" t-field="ml.quantity"/>
                                        <span t-field="ml.product_uom_id" groups="uom.group_uom"/>
                                    </td>
                                    <td t-if="o.picking_type_id.code != 'incoming'" groups="stock.group_stock_multi_locations">
                                        <span t-esc="ml.location_id.display_name"/>
                                        <t t-if="ml.package_id">
                                            <span t-field="ml.package_id"/>
                                        </t>
                                    </td>
                                    <td t-if="o.picking_type_id.code != 'outgoing'" groups="stock.group_stock_multi_locations">
                                        <div>
                                            <span t-field="ml.location_dest_id"/>
                                            <t t-if="ml.result_package_id">
                                                <span t-field="ml.result_package_id"/>
                                            </t>
                                        </div>
                                    </td>
                                    <td class=" text-center h6" t-if="has_serial_number">
                                        <div t-if="has_serial_number and (ml.lot_id or ml.lot_name)" t-esc="ml.lot_id.name or ml.lot_name" t-options="{'widget': 'barcode', 'humanreadable': 1, 'width': 400, 'height': 100, 'img_style': 'width:100%;height:35px;'}"/>
                                    </td>
                                    <td class="text-center" t-if="has_barcode">
                                        <t t-if="product_barcode != ml.product_id.barcode">
                                            <span t-if="ml.product_id and ml.product_id.barcode">
                                                <div t-field="ml.product_id.barcode" t-options="{'widget': 'barcode', 'symbology': 'auto', 'width': 400, 'height': 100, 'quiet': 0, 'img_style': 'height:35px;'}"/>
                                            </span>
                                            <t t-set="product_barcode" t-value="ml.product_id.barcode"/></t>
                                    </td>
                                </tr>
                            </t>
                        </tbody>
                    </table>
<t t-set="no_reserved_product" t-value="o.move_ids.filtered(lambda x: x.product_uom_qty != x.quantity and x.move_line_ids and x.state!='done')"/>
                    <p t-if="o.state in ['draft', 'waiting', 'confirmed'] or no_reserved_product">
                        <i class="fa fa-exclamation-triangle"/>
                                All products could not be reserved. Click on the "Check Availability" button to try to reserve products.



                    </p>
                    <p t-field="o.note"/>
                </div>
            </t>
        </t>
    </t>
</t>"""


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _tcf_apply_studio_report_fixes(self):
        """One-shot, idempotent: the Studio-duplicated 'Picking Operations SC',
        'Picking Operations SC copy(1)' and 'Delivery Slip SC' report bodies
        live purely as ir.ui.view records with no XML file backing them, so a
        normal `<record>`/xpath cannot target them. Overwrite their arch
        directly by `key` (a stable identifier tied to their own t-name, not
        a random Studio id) so this reliably targets the same records across
        databases derived from the same install.

        Both picking reports' Special Code column is intentional (TCF asked
        to keep it) and is added by a separate inheriting view per report
        (auto-generated key, so not referenced by name here) that either
        inserts the column outright or redirects an existing cell to the
        migrated `special_code`/`special_code_1` fields - keep those enabled;
        they are what fixes the raw `[False, '...']` display, not something
        to remove.

        Re-runs on every module update (this data file is not noupdate), so
        it keeps re-asserting the fix even if someone touches these views by
        hand again.
        """
        View = self.env['ir.ui.view'].sudo()

        picking_sc_base = View.search([('key', '=', 'stock.report_picking_copy_1')], limit=1)
        if picking_sc_base:
            picking_sc_base.write({'arch_db': PICKING_SC_BASE_ARCH})
            self._tcf_reenable_special_code_views(View, picking_sc_base)

        picking_sc_copy1 = View.search([('key', '=', 'stock.report_picking_copy_1_copy_1')], limit=1)
        if picking_sc_copy1:
            picking_sc_copy1.write({'arch_db': PICKING_SC_COPY1_ARCH})
            self._tcf_reenable_special_code_views(View, picking_sc_copy1)

        # 'Picking Operations SC copy(1) copy(1)': a Turkish delivery-form
        # variant (title/labels in Turkish, extra Number/Packaging columns,
        # signature lines) built through ~40 chained, position-based xpaths
        # in a separate inheriting view (auto-generated key). Overwriting
        # only adds a <style> tag and CSS classes here - it adds/removes no
        # <div> elements, so it does not shift the div[N] positions that
        # chain depends on.
        picking_sc_copy1_copy1 = View.search([('key', '=', 'stock.report_picking_copy_1_copy_1_copy_1')], limit=1)
        if picking_sc_copy1_copy1:
            picking_sc_copy1_copy1.write({'arch_db': PICKING_SC_COPY1_COPY1_ARCH})
            self._tcf_reenable_special_code_views(View, picking_sc_copy1_copy1)
            self._tcf_fix_picking3_packaging_column(View, picking_sc_copy1_copy1)

        delivery_sc = View.search([('key', '=', 'stock.report_delivery_document_copy_1')], limit=1)
        if delivery_sc:
            delivery_sc.write({'arch_db': DELIVERY_SC_ARCH})

        delivery_sc_lab = View.search([('key', '=', 'stock.report_delivery_document_copy_1_copy_1')], limit=1)
        if delivery_sc_lab:
            delivery_sc_lab.write({'arch_db': DELIVERY_SC_LAB_ARCH})

        # 'Delivery Slip SC copy(1) MAN': also fixes a pre-existing Studio bug
        # that broke this report outright - a t-esc expression left as
        # "... if move.move_line_ids else " (missing else-value) is a
        # SyntaxError at QWeb compile time. Completed with `False` (renders
        # blank), matching how the same Special Code field behaves elsewhere.
        delivery_sc_man = View.search([('key', '=', 'stock.report_delivery_document_copy_1_copy_1_copy_1')], limit=1)
        if delivery_sc_man:
            delivery_sc_man.write({'arch_db': DELIVERY_SC_MAN_ARCH})

        # 'Report By Package copy(1)': Studio duplicate of smartr_multi_level_pack's
        # 'Report By Package' (the base has its own XML file in that module and
        # is fixed there directly; this duplicate has no file backing, same as
        # the other Studio-made "copy(1)" reports above).
        report_by_package_copy1 = View.search([('key', '=', 'smartr_multi_level_pack.report_products_id_package_copy_1')], limit=1)
        if report_by_package_copy1:
            report_by_package_copy1.write({'arch_db': REPORT_BY_PACKAGE_COPY1_ARCH})

        # 'İRFAN BEY': another Studio-duplicated Picking report (report_picking
        # copy(2)), built through its own ~50-xpath chain in a separate
        # inheriting view (auto-generated key). Same approach as the Turkish
        # picking report above: only adds a <style> tag, a color style on
        # the <h1>, and CSS classes - no <div>/<table>/<th>/<td> added,
        # removed, or reordered, so the xpath chain's div[N]/th[N]/td[N]
        # positions keep resolving correctly.
        picking_copy2_irfan = View.search([('key', '=', 'stock.report_picking_copy_2')], limit=1)
        if picking_copy2_irfan:
            picking_copy2_irfan.write({'arch_db': PICKING_COPY2_IRFAN_ARCH})
            self._tcf_fix_picking2_irfan_final_product_fields(View, picking_copy2_irfan)

    def _tcf_fix_picking2_irfan_final_product_fields(self, View, parent_view):
        """'İRFAN BEY' (report_picking copy(2)) carries a Studio child view
        (auto-generated key, differs per database) that adds a "Final
        Product" / "Lot For Final Product" / "Miktar" section. On some
        databases that section was never migrated off the raw Studio field
        names (x_studio_final_product, x_studio_lot_for_final_product,
        x_studio_final_product_quantity_to_produce), which don't exist on
        stock.picking any more - printing raises a KeyError and the view
        gets left disabled to hide the crash. Rewrite it to the migrated
        field names (final_product_id, lot_for_final_product_id,
        final_product_qty) and re-enable it.

        Looked up by inherit_id + content (not a fixed key), and only
        touched when the stale field names are actually present, so this
        is a no-op on a database where the view was already migrated (or
        doesn't exist).
        """
        child_view = View.search([
            ('inherit_id', '=', parent_view.id),
            ('arch_db', 'like', 'x_studio_final_product'),
        ], limit=1)
        if not child_view:
            return
        arch = child_view.arch_db
        replacements = [
            ('o.x_studio_final_product_quantity_to_produce', 'o.final_product_qty'),
            ('o.x_studio_lot_for_final_product', 'o.lot_for_final_product_id'),
            ('o.x_studio_final_product', 'o.final_product_id'),
        ]
        fixed_arch = arch
        for old, new in replacements:
            fixed_arch = fixed_arch.replace(old, new)
        vals = {'active': True}
        if fixed_arch != arch:
            vals['arch_db'] = fixed_arch
        child_view.write(vals)

    def _tcf_fix_picking3_packaging_column(self, View, parent_view):
        """The Turkish form's Studio xpath chain adds a 'Product Packaging'
        <th> to the header but its matching <td> insertion in the body was
        left empty (Studio bug), so every body cell from Quantity onward
        renders one column to the left of its header (Quantity's value
        lands under "Product Packaging", "To"'s value lands under
        "Quantity", etc). Fix by inserting the missing empty <td>
        placeholder - Product Packaging never had a bound field on this
        form, so an empty cell is the correct/intended body content.

        Looked up by inherit_id + content (not a fixed key: this child view
        has an auto-generated Studio key that can differ per database).
        """
        packaging_view = View.search([
            ('inherit_id', '=', parent_view.id),
            ('arch_db', 'like', 'Product Packaging'),
        ], limit=1)
        if not packaging_view:
            return
        arch = packaging_view.arch_db
        pattern = re.compile(
            r'(<xpath[^>]*expr="[^"]*tbody/t/tr/td\[3\]"[^>]*position="after">)\s*(</xpath>)'
        )
        if not pattern.search(arch):
            return
        fixed_arch = pattern.sub(r'\1\n    <td></td>\n  \2', arch, count=1)
        if fixed_arch != arch:
            packaging_view.write({'arch_db': fixed_arch})

    def _tcf_reenable_special_code_views(self, View, parent_view):
        special_code_views = View.search([
            ('inherit_id', '=', parent_view.id),
            ('arch_db', 'like', 'special_code'),
            ('active', '=', False),
        ])
        if special_code_views:
            special_code_views.write({'active': True})
