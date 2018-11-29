from tornado.concurrent import run_on_executor
from ..base import BaseHandler
import requests
import traceback
from tornado.options import options
import config.setting


class SmsSendHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            telephone = self.get_argument("telephone", None)
            if not telephone:
                return self.response(code=10002, msg='参数错误')

            data = {
                'mobile': int(telephone),
                'typeCode': options.sms_type_code
            }
            res = requests.post(options.send_sms_url, data=data)
            if res.json()['status'] == '10000':
                return self.response(code=10001, msg='success')
            else:
                return self.response(code=10003, msg=res.json()['msg'])

        except Exception as e:
            self.logger.error(e)
            print(traceback.print_exc())
            return self.response(code=10000, msg='服务端异常')


class SmsVerifyHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            code = self.get_argument('code', None)
            telephone = self.get_argument("telephone", None)
            if not code or not telephone:
                return self.response(code=10002, msg='参数错误')

            data = {
                'mobile': int(telephone),
                'code': int(code)
            }

            res = requests.post(options.verify_sms_url, data=data)
            result = res.json()['result']['verify']
            if result:
                return self.response(code=10001, msg='success', data='verify success')
            else:
                return self.response(code=10001, msg='success', data='verify fail')

        except Exception as e:
            self.logger.error(e)
            print(traceback.print_exc())
            return self.response(code=10000, msg='服务端异常')
