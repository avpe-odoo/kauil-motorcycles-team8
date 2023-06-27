from odoo import models, fields, api, _

class AccountInvoiceReportInherit(models.Model):
    _inherit = 'account.invoice.report'

    vin_name = fields.Char(string='VIN', compute="_compute_vin_name")

    @api.depends('vin_name')
    def _compute_vin_name(self):
        for invoice in self:
            print("CHUL")
            self.vin_name= self.env['account.move.line'].search([('id', '=', invoice.id)]).vin_name