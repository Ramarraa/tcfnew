from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Refresh stored packaging on existing, unfinished sale transfers."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    Move = env['stock.move']
    last_id = 0
    while True:
        moves = Move.search([
            ('id', '>', last_id),
            ('state', 'not in', ['done', 'cancel']),
            ('sale_line_id.packaging_uom_id', '!=', False),
        ], order='id', limit=1000)
        if not moves:
            break
        moves._compute_packaging_uom_id()
        moves._compute_packaging_uom_qty()
        moves.flush_recordset(['packaging_uom_id', 'packaging_uom_qty'])
        last_id = moves[-1].id
