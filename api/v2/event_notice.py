from tornado.concurrent import run_on_executor
import datetime
from ..base import BaseHandler
from tornado.options import options
import config.setting
import traceback
from template_smg.event_notice import send_template_msg


class EventNoticeHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            openid = self.get_argument("openid", None)
            if not openid:
                return self.response(code=10002, msg='参数错误')

            result = send_template_msg(openid)
            result_code = result["errcode"]
            if result_code == 0:
                return self.response(code=10001, msg='success')
            else:
                return self.response(code=10003, msg='error code: %s' % result_code)

        except Exception as e:
            self.logger.error(str(e))
            print(traceback.print_exc())
            return self.response(code=10000, msg='服务端异常')
