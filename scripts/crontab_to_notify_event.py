from tornado.options import options
from config import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import traceback
import os

from models.order import Order
from models.user import Phone_Name


class TemplateNotify(object):
    def __init__(self):
        self.baseDir = os.path.dirname(os.path.realpath(__file__))

        database_url = 'mysql+mysqldb://{}:{}@{}/{}?charset=utf8'.format(options.mysql_user, options.mysql_password,
                                                                         options.mysql_host, options.mysql_database)
        engine = create_engine(database_url, encoding='utf8', pool_size=options.pool_size,
                               pool_recycle=options.pool_recycle, echo=False, echo_pool=False)
        self.session = scoped_session(sessionmaker(bind=engine, autocommit=False))

    def push_event(self):
        try:
            url = 'https://temp.mibaoxian.com/youbao/v2/template/event'
            push_list = []
            pay_users = self.session.query(Order).filter(Order.pay_status == 2).all()
            for user in pay_users:
                phone = self.session.query(Phone_Name).filter(Phone_Name.openid == user.user_openid).first()
                if not phone:
                    push_list.append(user.user_openid)

            for openid in push_list:
                data = {'openid': openid}
                res = requests.post(url, data=data)
                if res.json()['state'] == 10001:
                    pass
                else:
                    print(res.json()['msg'])

        except Exception as e:
            print(e)
            print(traceback.print_exc())

if __name__ == '__main__':
    a = TemplateNotify()
    a.push_event()
