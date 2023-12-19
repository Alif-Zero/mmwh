from odoo import models, fields, api
from odoo.osv import expression


class StockLocation(models.Model):
    _inherit = 'stock.location'

    code = fields.Char(readonly=True, string='Shade No')

    @api.model
    def create(self, vals):
        record = super(StockLocation, self).create(vals)
        shade_code = self.env['ir.sequence'].next_by_code('stock.location.code') or ('New')
        record['code'] = shade_code

        return record



    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not(name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
