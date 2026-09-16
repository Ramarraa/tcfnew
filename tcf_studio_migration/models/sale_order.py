from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    account_name = fields.Char(string='Account Name', readonly=True)
    bank_account_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Bank Account',
        ondelete='set null',
    )
    bank_account_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Bank Account Currency',
        ondelete='set null',
        readonly=True,
    )
    branch_code = fields.Char(string='Branch Code', readonly=True)
    iban_number = fields.Char(string='IBAN Number', readonly=True)
    swift_code = fields.Char(string='Swift Code')

    @api.onchange('bank_account_id')
    def _onchange_bank_account_id(self):
        bank = self.bank_account_id
        self.account_name = bank.acc_holder_name or bank.partner_id.name
        self.branch_code = bank.branch_code
        self.iban_number = bank.iban_number
        self.swift_code = bank.bank_id.bic
        self.bank_account_currency_id = bank.currency_id
