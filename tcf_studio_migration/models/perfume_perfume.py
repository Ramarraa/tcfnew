from odoo import api, fields, models


class PerfumePerfume(models.Model):
    _name = 'perfume.perfume'
    _description = 'Perfume'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, translate=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    avatar_image = fields.Image(string='Avatar Image', max_width=256, max_height=256)
    code = fields.Char(string='Code', tracking=True)
    matching_products_count = fields.Integer(
        string='Matching Products Count',
        compute='_compute_matching_products_count',
        compute_sudo=True,
    )
    brand_id = fields.Many2one(
        comodel_name='brand.brand',
        string='Brand',
        ondelete='set null',
        tracking=True,
    )
    notes = fields.Html(string='Notes')
    priority = fields.Selection(
        selection=[('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')],
        string='Priority',
        default='0',
        tracking=True,
    )
    sequence = fields.Integer(string='Sequence', default=10)
    status = fields.Selection(
        selection=[
            ('checking', 'Checking'),
            ('Not Printed', 'Not Printed'),
            ('To Print', 'To Print'),
            ('Printed', 'Printed'),
        ],
        string='Status',
        tracking=True,
    )

    @api.depends('code')
    def _compute_matching_products_count(self):
        Product = self.env['product.template']
        for perfume in self:
            code = (perfume.code or '').strip()
            if not code:
                perfume.matching_products_count = 0
                continue

            normalized_code = code.replace(' ', '').upper()
            perfume.matching_products_count = Product.search_count([
                '|',
                ('alternative_code', '=', code),
                ('alternative_code', 'ilike', normalized_code),
            ])

    def action_set_status_not_printed(self):
        self.write({'status': 'Not Printed'})
        for perfume in self:
            perfume.message_post(body='Status set to NOT PRINTED')

    def action_set_status_printed(self):
        self.write({'status': 'Printed'})
        for perfume in self:
            perfume.message_post(body='Status set to PRINTED')

    def action_set_status_to_print(self):
        self.write({'status': 'To Print'})
        for perfume in self:
            perfume.message_post(body='Status set to TO PRINT')

    def action_set_status_checking(self):
        self.write({'status': 'checking'})
        for perfume in self:
            perfume.message_post(body='Status set to CHECKING')
