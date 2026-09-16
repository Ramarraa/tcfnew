# -*- coding: utf-8 -*-

from collections import OrderedDict

from odoo import models


class ReportMoCostAnalysis(models.AbstractModel):
    _name = 'report.tcf_studio_migration.report_mo_cost_analysis'
    _description = 'Manufacturing Order Cost Analysis Report'

    def _get_report_values(self, docids, data=None):
        productions = self.env['mrp.production'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'mrp.production',
            'docs': productions,
            'cost_analysis': self._get_cost_analysis(productions),
        }

    def _get_cost_analysis(self, productions):
        product = productions.product_id[:1]
        uom = product.uom_id
        total_qty = sum(
            (production.qty_produced if production.state == 'done' else production.product_qty)
            for production in productions
        )

        components = OrderedDict()
        for production in productions:
            for move in production.move_raw_ids.filtered(lambda m: m.state != 'cancel'):
                qty = move.quantity if production.state == 'done' else move.product_uom_qty
                if not qty:
                    continue
                unit_cost = move._get_price_unit()
                line = components.setdefault(move.product_id.id, {
                    'code': move.product_id.default_code or '',
                    'name': move.product_id.name,
                    'qty': 0.0,
                    'uom_name': move.product_uom.name,
                    'unit_cost': unit_cost,
                    'total_cost': 0.0,
                })
                line['qty'] += qty
                line['unit_cost'] = unit_cost
                line['total_cost'] += qty * unit_cost

        operations = OrderedDict()
        for production in productions:
            for workorder in production.workorder_ids.filtered(lambda w: w.state != 'cancel'):
                duration_hours = (workorder.duration or 0.0) / 60.0
                cost_hour = workorder.costs_hour or workorder.workcenter_id.costs_hour
                key = (workorder.workcenter_id.id, workorder.name)
                line = operations.setdefault(key, {
                    'resource': workorder.workcenter_id.name,
                    'operation': workorder.name,
                    'duration_hours': 0.0,
                    'cost_hour': cost_hour,
                    'total_cost': 0.0,
                })
                line['duration_hours'] += duration_hours
                line['total_cost'] += duration_hours * cost_hour

        components = list(components.values())
        operations = list(operations.values())

        total_components_cost = sum(line['total_cost'] for line in components)
        total_operations_cost = sum(line['total_cost'] for line in operations)
        total_production_cost = total_components_cost + total_operations_cost

        return {
            'product': product,
            'uom_name': uom.name,
            'total_qty': total_qty,
            'mo_count': len(productions),
            'components': components,
            'operations': operations,
            'total_components_cost': total_components_cost,
            'components_cost_per_unit': (total_components_cost / total_qty) if total_qty else 0.0,
            'total_operations_cost': total_operations_cost,
            'operations_cost_per_unit': (total_operations_cost / total_qty) if total_qty else 0.0,
            'total_production_cost': total_production_cost,
            'total_cost_per_unit': (total_production_cost / total_qty) if total_qty else 0.0,
            'currency': (productions.company_id.currency_id[:1] or self.env.company.currency_id),
        }
