from tornado.concurrent import run_on_executor
from ..base import BaseHandler

from models.product import Product
from models.order import Order


class OrderDetailHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            openid = self.get_argument("openid", None)
            if not openid:
                return self.response(code=10002, msg='参数错误')

            orders = self.session.query(Order).filter(Order.openid == openid).order_by(Order.pay_status.asc()).order_by(Order.id.desc()).all()
            ret_data = []
            for order in orders:
                tmp = dict()
                tmp['order_id'] = order.id
                tmp['pay_status'] = order.pay_status
                tmp['product_id'] = order.product_id
                product = self.session.query(Product).filter(Product.id == order.product_id).first()
                tmp['name'] = product.name
                tmp['price'] = float(product.price)
                tmp['description'] = product.description
                tmp['create_time'] = order.create_ts
                ret_data.append(tmp)
            return self.response(data=ret_data, code=10001, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            return self.response(code=10000, msg='服务端异常')


class OrderPaymentHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            pass

        except Exception as e:
            self.logger.error(str(e))
            self.session.rollback()
            return self.response(code=10000, msg='服务端异常')
