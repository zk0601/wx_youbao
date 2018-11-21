from tornado.concurrent import run_on_executor
import tornado.web
import config.setting
from tornado.options import options
import hashlib
from ..base import BaseHandler


class WeChatVerifyHandler(BaseHandler):
    @run_on_executor
    def get(self):
        try:
            signature = self.get_argument('signature', None)
            timestamp = self.get_argument('timestamp', None)
            nonce = self.get_argument('nonce', None)
            echostr = self.get_argument('echostr', None)

            if not signature or not timestamp or not nonce or not echostr:
                return False

            alist = [options.token, timestamp, nonce]
            alist.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, alist)
            hashcode = sha1.hexdigest()

            if hashcode == signature:
                return self.write(echostr)
            else:
                return False

        except Exception as e:
            self.logger.error(str(e))
            return False
