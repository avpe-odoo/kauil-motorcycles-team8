from odoo import api, fields, models


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    vin_name = fields.Char(string="VIN", compute="_compute_vin_name")

    @api.depends('vin_name')
    def _compute_vin_name(self):
        for order in self:
            print()
            print("LOLWA")
            print()
            print(self.id)
            print()
            self.env.cr.execute("""SELECT sl."name"  FROM sale_order_line_invoice_rel solir
left join stock_move sm on solir.order_line_id = sm.sale_line_id 
left join stock_move_line sml on sml.move_id = sm.id 
left join stock_lot sl on sl.id = sml.lot_id 
where solir.invoice_line_id = %s""", (self.id,))
            order_line_id=self.env.cr.fetchall()
            print(type(order_line_id[0]))
            print(order_line_id[0][0])
            
            self.vin_name=order_line_id[0][0]