from tornado.concurrent import run_on_executor
import time
import json
from ..base import BaseHandler
from tornado.options import options
import config.setting
import traceback
from utils.wx_payment import random_str
from template_smg.event_notice import get_sign


class GetSignHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            jsapilist = self.get_argument("jsApiList", None)
            url = self.get_body_argument('url', None)
            if not url or not jsapilist:
                return self.response(code=10002, msg='缺少参数')
            jsapilist = json.loads(jsapilist)

            noncestr = random_str(16)
            data = {
                'appId': options.AppID,
                'timestamp': str(int(time.time())),
                'nonceStr': noncestr,
                'jsApiList': jsapilist
            }
            sign_data = {
                'nonceStr': noncestr,
                'timestamp': int(time.time()),
                'url': url
            }
            sign = get_sign(sign_data)
            data['signature'] = sign
            return self.response(data=data, code=10001, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            print(traceback.print_exc())
            return self.response(code=10000, msg='服务端异常')

