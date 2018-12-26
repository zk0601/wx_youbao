from tornado.concurrent import run_on_executor
import time
from ..base import BaseHandler
from tornado.options import options
import config.setting
import traceback
from utils.wx_payment import get_sign, random_str


class GetSignHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            jsApiList = self.get_argument("jsApiList", None)

            noncestr = random_str(16)
            data = {
                'debug': True,
                'appId': options.AppID,
                'timestamp': str(int(time.time())),
                'nonceStr': noncestr,
                'jsApiList': jsApiList
            }
            sgin = get_sign(data)
            data['signature'] = sgin
            return self.response(data=data, code=10001, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            print(traceback.print_exc())
            return self.response(code=10000, msg='服务端异常')

