from odoo import fields, models, api, _




class ResCompany(models.Model):
    _name = "res.company"
    _inherit = ["res.company", "mail.thread"]

    labour_profit_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Labour Profit Account")
    
    labour_expense_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Labour Expense Account")
    

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    labour_profit_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.labour_profit_account_id",
        string="Labour Profit Account",
        readonly=False,)
    labour_expense_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.labour_expense_account_id",
        string="Labour Expense Account",
        readonly=False,)