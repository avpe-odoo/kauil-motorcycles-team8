from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ##Action Method for the button
    def action_new_customer(self):
        for record in self:
            if record.partner_id.is_new_customer == True:
                order_line = self.env['sale.order.line'].search([('order_id','=',record.id)])

                # discount = 2500
                # price = order_line.product_template_id.base_unit_price
                # discount_percentage = discount/price*100
                # order_line.discount = discount_percentage

                # print()
                # print(discount_percentage)
                # print()

                # record.pricelist_id = self.env['product.pricelist'].search([('name','like','Motorcycle price')])
                pricelist_record = self.env['product.pricelist'].search([('name','like', 'Motorcycle price')])
                # print()
                # print(pricelist_record)
                # print()
                # record.partner_id.property_product_pricelist = pricelist_record
                record.pricelist_id = pricelist_record
                # print()
                # print(order_line.product_template_id.base_unit_price)
                # print()
                super(SaleOrder, self).action_update_prices()
                
            else:
                print()
                print("NOT A NEW CUSTOMER!!!!!!!")
                print()

            # super(SaleOrder,self)._recompute_prices()