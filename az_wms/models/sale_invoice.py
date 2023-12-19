from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['invoice_date'] = fields.Date.today()
        res['bill_date_time'] = fields.Datetime.today()
        return res

    bill_date_time = fields.Datetime(string="Date")
    mill_id = fields.Many2one('az.mill', string="Mill Name")
    location_id = fields.Many2one('stock.location', string="Shade")

    vehicle_number = fields.Char(string="Vehicle")
    bilty_number = fields.Char(string="Bilty No.")
    lot_id = fields.Char(string="Lot Number:")
    in_date = fields.Date(string="In Date")
    out_date = fields.Date(string="Out Date")

    labour_partner_id = fields.Many2one('res.partner',string="Labour Paid By")
    contractor_id = fields.Many2one('res.partner',string="Contractor")
    labour_type = fields.Selection([
        ('type1','Type1'),
        ('type2','Type2')
        ],string="Labour Type")
    labour_charge = fields.Float(string="Labour Charges")

    labour_entry_id = fields.Many2one('account.move', copy=False)
    invoice_id = fields.Many2one('account.move',domain="[('move_type','=', 'out_invoice'),('partner_id','=', partner_id)]", string="Invoice No")

    partner_credit = fields.Monetary(related='partner_id.credit')
    partner_debit = fields.Monetary(related='partner_id.debit')


    def action_sale_invoice(self):
        return self.env.ref('account.account_invoices').report_action(self)
    
    def action_post(self):
        res = super().action_post()
        if self.labour_charge:
            self.action_labour_entry()
        return res

    def action_labour_entry(self):
        lines_vals_list = []
        labour_amount = self.labour_charge
        total_amount = sum(self.invoice_line_ids.mapped('labour'))
        if labour_amount == 0:
            return
    
        if self.labour_type == 'type1':
            if total_amount < labour_amount:
                raise ValidationError("""Contractor labour charges should be less than labour amount""")

            journal = self.env['account.journal'].search([('type','=','general')], limit=1)
            move = self.env['account.move'].create({
                'journal_id':journal.id,
                'move_type': 'entry',
                'ref':self.name
            })
            self.labour_entry_id = move.id
            line = {
                'name':self.name,
                'move_id': move.id,
                'partner_id': self.labour_partner_id.id,
                'account_id': self.labour_partner_id.property_account_receivable_id.id,
                'debit': total_amount,
            }
            lines_vals_list.append(line)
            line = {
                'name':self.name,
                'move_id': move.id,
                'partner_id': self.contractor_id.id,
                'account_id': self.contractor_id.property_account_payable_id.id,
                'credit': labour_amount,
            }
            lines_vals_list.append(line)
            if  total_amount - labour_amount != 0:
                line = {
                'name':self.name,
                'move_id': move.id,
                # 'partner_id': self.contractor_id.id,
                'account_id': self.company_id.labour_profit_account_id.id,
                'credit': total_amount - labour_amount,
                }
                lines_vals_list.append(line)
            jv = self.env['account.move.line'].create(lines_vals_list)
            move.action_post()
        elif self.labour_type == 'type2':
            journal = self.env['account.journal'].search([('type','=','general')], limit=1)
            move = self.env['account.move'].create({
                'journal_id':journal.id,
                'move_type': 'entry',
                'ref':self.name
            })
            self.labour_entry_id = move.id
            line = {
                'name':self.name,
                'move_id': move.id,
                'partner_id': self.partner_id.id,
                'account_id': self.company_id.labour_expense_account_id.id,
                'debit': total_amount,
            }
            lines_vals_list.append(line)
            line = {
                'name':self.name,
                'move_id': move.id,
                'partner_id': self.contractor_id.id,
                'account_id': self.contractor_id.property_account_payable_id.id,
                'credit': total_amount,
            }
            lines_vals_list.append(line)
            self.env['account.move.line'].create(lines_vals_list)
            move.action_post()

    @api.onchange('invoice_id')
    def _onchange_invoice_id(self):
        self.mill_id = self.invoice_id.mill_id.id
        self.location_id = self.invoice_id.location_id.id
        self.in_date = self.invoice_id.in_date
        invoice_line_ids = self.invoice_id.invoice_line_ids
        lines_vals_list = []
        self.invoice_line_ids = False
        for line in invoice_line_ids:
            copied_vals = line.copy_data()[0]
            product_id = line.product_id
            invoice_id = self.invoice_id.name
            lot_id = self.env['stock.lot'].search([
                ('name','=', invoice_id),
                ('product_id','=', product_id.id),
                ])
            # stock_quant = self.env['stock.quant'].search([
            #     ('product_id','=', product_id.id),
            #     ('lot_id','=', lot_id.id),
            #     ])

            copied_vals['quantity'] = lot_id.product_qty
            self.invoice_line_ids += self.env['account.move.line'].new(copied_vals)
             # Add interim account line.
            


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    code = fields.Char(related='product_id.default_code')
    labour = fields.Float()

