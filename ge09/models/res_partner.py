from odoo import api, models, fields

class Partner(models.Model):
    _inherit = ['res.partner']

    is_new_customer = fields.Boolean(compute="_check_first")
                    
    def _check_first(self):
        for record in self:
            ## Get all sale orders for the person
            all_sale_order_lines = self.env['sale.order.line'].search([('order_partner_id','=',record.id)])
            
            for line in all_sale_order_lines:
                detailed_type = line.product_id.detailed_type
                order_state = line.order_id.state
                if detailed_type == 'motorcycle' and order_state not in ('draft','cancel'):
                    record.is_new_customer = False
                    return
            
            record.is_new_customer = True
