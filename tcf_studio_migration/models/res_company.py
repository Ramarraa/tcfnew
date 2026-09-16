# -*- coding: utf-8 -*-

from odoo import models


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _tcf_disable_quotation_terms_link(self):
        """One-shot: v19 enabled 'Default Terms & Conditions' which prints a
        'Terms: <url>' line on quotations that v16 never had. Disable it once;
        a marker key lets accountants re-enable it later without us fighting
        them on every module update."""
        icp = self.env['ir.config_parameter'].sudo()
        if not icp.get_param('tcf.terms_link_reset_done'):
            icp.set_param('account.use_invoice_terms', 'False')
            icp.set_param('tcf.terms_link_reset_done', '1')
