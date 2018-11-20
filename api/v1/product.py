from tornado.concurrent import run_on_executor
from ..base import BaseHandler

from models.product import Product


class ProductListHandler(BaseHandler):
    @run_on_executor
    def get(self):
        try:
            ret_data = []
            products = self.session.query(Product).filter(Product.is_available == 1).all()
            for product in products:
                tmp = dict()
                tmp["id"] = product.id
                tmp["name"] = product.name
                tmp["price"] = float(product.price)
                tmp["description"] = product.description
                ret_data.append(tmp)

            return self.response(data=ret_data, code=10001, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            return self.response(code=10000, msg='服务端异常')

