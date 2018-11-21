from api.v1.auth import UserAuthHandler
from api.v1.verify import WeChatVerifyHandler
from api.v1.user import UserLoginHandler, UserStoreInfoHandler
from api.v1.product import ProductListHandler
from api.v1.order import OrderDetailHandler, OrderPaymentHandler
from api.v1.payment_callback import PayCallbackHandler

handlers = [
    (r'/v1/verify', WeChatVerifyHandler),

    (r'/v1/user/auth', UserAuthHandler),
    (r'/v1/user/login', UserLoginHandler),
    (r'/v1/user/storeinfo', UserStoreInfoHandler),

    (r'/v1/product/list', ProductListHandler),

    (r'/v1/order/detail', OrderDetailHandler),
    (r'/v1/order/pay', OrderPaymentHandler),
    (r'/v1/order/paycallback', PayCallbackHandler)
]

Need_Token_URLs = [
    '/v1/user/storeinfo',
    '/v1/order/detail',
    '/v1/order/pay'
]
