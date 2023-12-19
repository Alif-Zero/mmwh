from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    code = fields.Char()
    ntn = fields.Char(string='NTN')
    gst = fields.Char(string='GST')
    cell_no = fields.Many2many("partner.cell",string="Cell# ")
    contact_person = fields.Many2one('res.partner', trace=True)
    strn = fields.Char(string='STRN')
    full_address = fields.Text(string="Full Address")

    @api.model
    def create(self, vals):
        record = super(ResPartner, self).create(vals)
        customer_code = self.env['ir.sequence'].next_by_code('wms.customer.code') or ('New')
        record['code'] = customer_code

        return record

class PartnerCell(models.Model):
    _name = 'partner.cell'
    name = fields.Char(string="Cell#")