from odoo import models, fields, api


class BrandBrand(models.Model):
    _name = 'brand.brand'
    _description = 'Brand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, translate=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence', default=10)
    pipeline_status = fields.Selection(
        selection=[('status2', 'DRAFT'), ('status1', 'CONFIRMED')],
        string='Pipeline Status',
        tracking=True,
    )
    tag_ids = fields.Many2many(
        comodel_name='brand.tag',
        string='Tags',
    )
    perfume_ids = fields.One2many(
        comodel_name='perfume.perfume',
        inverse_name='brand_id',
        string='Perfumes',
    )
    perfume_count = fields.Integer(
        string='Perfume Count',
        compute='_compute_perfume_count',
    )

    @api.depends('perfume_ids')
    def _compute_perfume_count(self):
        for record in self:
            record.perfume_count = len(record.perfume_ids)

    def action_perfume_ids(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Perfumes',
            'res_model': 'perfume.perfume',
            'view_mode': 'list,form',
            'domain': [('brand_id', '=', self.id)],
            'context': {'default_brand_id': self.id},
        }
