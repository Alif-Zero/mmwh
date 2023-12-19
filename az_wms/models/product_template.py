from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        record = super(ProductTemplate, self).create(vals)
        item_code = self.env['ir.sequence'].next_by_code('wms.product.code') or ('New')
        record['default_code'] = item_code
        return record
