from odoo import models, fields


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    branch_code = fields.Char(string='Branch Code')
    iban_number = fields.Char(string='IBAN Number')
