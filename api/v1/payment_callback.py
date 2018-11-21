from tornado.concurrent import run_on_executor
from ..base import BaseHandler
import datetime
from utils.wx_payment import trans_xml_to_dict, get_sign
from models.order import Order
from models.product import Product


class PayCallbackHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            data = trans_xml_to_dict(self.request.body)
            sign = data.pop('sign')
            back_sign = get_sign(data)
            if sign == back_sign:
                order_id = data["attach"]
                order = self.session.query(Order).filter(Order.id == order_id).first()
                if order.pay_status == 1:
                    order.pay_status = 2
                    order.complete_time = datetime.datetime.now()
                    product = self.session.query(Product).filter(Product.id == order.product_id).first()
                    product.sell_amount = product.sell_amount + 1
                    self.session.commit()
                return self.write("<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>")
            else:
                return self.write("<xml><return_code><![CDATA[]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>")

        except Exception as e:
            self.logger.error(str(e))
            self.session.rollback()
            return self.write("<xml><return_code><![CDATA[]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>")
