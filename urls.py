from api.v1.auth import UserAuthHandler
from api.v1.verify import WeChatVerifyHandler
from api.v1.user import UserLoginHandler, UserStoreInfoHandler
from api.v1.product import ProductListHandler
from api.v1.order import OrderDetailHandler, OrderPaymentHandler

handlers = [
    (r'/v1/verify', WeChatVerifyHandler),

    (r'/v1/user/auth', UserAuthHandler),
    (r'/v1/user/login', UserLoginHandler),
    (r'/v1/user/storeinfo', UserStoreInfoHandler),

    (r'/v1/product/list', ProductListHandler),

    (r'/v1/order/detaul', OrderDetailHandler),
    (r'/v1/order/pay', OrderPaymentHandler)
]

Need_Token_URLs = [
    '/v1/user/storeinfo',
    '/v1/order/detaul',
    '/v1/order/pay'
]
