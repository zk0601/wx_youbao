import traceback
import csv
import os
import datetime

from .crontab_to_notify_event import TemplateNotify
from models.user import Phone_Name, User_Base, User_From
from models.order import Order


class Export(TemplateNotify):
    def __init__(self):
        super(TemplateNotify, self).__init__()

    def main(self):
        try:
            headers = ['用户微信昵称', '用户微信头像', '是否填写姓名电话', '姓名', '电话', '是否填写详细信息']
            csv_list = []
            data_template = {
                'nick_name': '',
                'image': '',
                'is_phone': '',
                'name': '',
                'phone': '',
                'is_detail': ''
            }
            users = self.session.query(Order).filter(Order.pay_status == 2).all()
            for user in users:
                data = data_template.copy()
                openid = user.user_openid
                base = self.session.query(User_Base).filter(User_Base.openid == openid).first()
                data['nice_name'] = base.nickname
                data['image'] = base.image_url
                phone = self.session.query(Phone_Name).filter(Phone_Name.openid == openid).first()
                if not phone:
                    data['is_phone'] = '否'
                    data['name'], data['phone'] = '', ''
                else:
                    data['is_phone'] = '是'
                    data['name'], data['phone'] = phone.name, phone.phone
                form_data = self.session.query(User_From).filter(User_From.openid == openid).first()
                if not form_data:
                    data['from_data'] = '否'
                else:
                    data['from_data'] = '是'
                csv_list.append(data)

            today = datetime.datetime.now().strftime("%Y%m%d")
            csv_file = os.path.join(self.baseDir, 'user_export', '%s.csv' % today)
            with open(csv_file, 'w', encoding='utf-8') as f:
                writer = csv.DictWriter(f, headers)
                writer.writeheader()
                writer.writerows(csv_list)
            print('ok')

        except Exception as e:
            print(e)
            print(traceback.print_exc())


if __name__ == '__main__':
    a = Export()
    a.main()
