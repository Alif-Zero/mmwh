from odoo import models, fields, api
from odoo.osv import expression


class ProductCategory(models.Model):
    _inherit = 'product.category'

    code = fields.Char()

    @api.model
    def create(self, vals):
        record = super(ProductCategory, self).create(vals)
        categ_code = self.env['ir.sequence'].next_by_code('product.category.code') or ('New')
        record['code'] = categ_code
        return record
    
    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not(name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
