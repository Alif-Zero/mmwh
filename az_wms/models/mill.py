from odoo import models, fields, api
from odoo.osv import expression



class AZMill(models.Model):
    _name = 'az.mill'

    name = fields.Char()
    code = fields.Char(readonly=True)

    @api.model
    def create(self, vals):
        record = super(AZMill, self).create(vals)
        shade_code = self.env['ir.sequence'].next_by_code('self.mill.code') or ('New')
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
