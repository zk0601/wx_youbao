from tornado.concurrent import run_on_executor
import time
import datetime
from ..base import BaseHandler
from utils.wx_payment import request_prepayment, get_sign, random_str, order_num
from models.product import Product
from models.order import Order
from models.user import UserFrom
from tornado.options import options
import config.setting


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
            openid = self.get_argument("openid", None)
            product_id = self.get_argument("product_id", None)
            if not openid or not product_id:
                return self.response(code=10002, msg='参数错误')

            user = self.session.query(UserFrom).filter(UserFrom.openid == openid).first()
            phone = user.phone
            product = self.session.query(Product).filter(Product.id == product_id).first()
            fee = float(product.price)
            out_trade_no = order_num(phone)

            order = Order(product_id=product_id, product_name=product.name, product_description=product.description,
                          total_fee=float(product.price), create_ts=datetime.datetime.now(), openid=openid, pay_status=1,
                          out_trade_no=out_trade_no)
            self.session.add(order)
            self.session.flush()
            orderid = order.id

            pay_data = request_prepayment(openid, int(fee * 100), out_trade_no, orderid)
            if pay_data['return_code'] == 'FAIL':
                return self.response(code=10003, msg=pay_data["return_msg"])
            if pay_data['result_code'] == 'FAIL':
                return self.response(code=10003, msg="%s:%s" % (pay_data['errcode'], pay_data['errmsg']))

            self.session.commit()
            sign_data = dict()
            sign_data['appid'] = options.AppID
            sign_data['timeStamp'] = int(time.time())
            sign_data['nonceStr'] = random_str(16)
            sign_data['package'] = 'prepay_id=' + pay_data['prepay_id']
            sign_data['signType'] = 'MD5'
            sign = get_sign(sign_data)
            return_data = {
                'timeStamp': sign_data['timeStamp'],
                'nonceStr': sign_data['nonceStr'],
                'package': sign_data['package'],
                'signType': sign_data['signType'],
                'paySign': sign
            }
            return self.response(data=return_data, code=10001, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            self.session.rollback()
            return self.response(code=10000, msg='服务端异常')
