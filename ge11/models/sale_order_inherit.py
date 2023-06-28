from odoo import api,fields,models

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'



    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", compute="_compute_pricelist_id")
    
    @api.depends('partner_id')
    def _compute_pricelist_id(self):
        for order in self:
            if not order.partner_id:
                order.warehouse_id = False
                continue
            # partner_state=self.env["res.partner"].search(["id","=",self.partner_id])
            partner_state=self.env["res.partner"].search([("id", "=", self.partner_id.id)]).state_id.id
            if partner_state>100:
                self.warehouse_id=3
            else:
                self.warehouse_id=4
            print(partner_state)
