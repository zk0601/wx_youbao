import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import traceback
import csv
import os
import datetime

from scripts.crontab_to_notify_event import TemplateNotify
from models.user import Phone_Name, User_Base, User_From, Spouse, Children
from models.order import Order


class Export(TemplateNotify):
    def __init__(self):
        super(Export, self).__init__()
        self.family_str = {
            '1': '单身',
            '2': '已婚无娃',
            '3': '离婚有娃',
            '4': '已婚有娃'
        }
        self.other_str = {
            '0': '否',
            '1': '是'
        }

    def main(self):
        try:
            # headers = ['用户微信昵称', '用户微信头像', '姓名', '电话', '微信', '订单支付时间', '性别', '家庭情况',
            #            '孩子数量', '是否赡养父母', '出生日期', '疾病', '年收入（万元）', '职业', '是否有社保',
            #            '房贷总额（万元）', '房贷月供（元）', '还需还款年数', '车贷总额（万元）', '车贷月供（元）',
            #            '还需还款年数', '是否经常出差', '日常出行是否驾车', '所在城市',
            #            '配偶生日', '配偶疾病', '配偶收入（万元）', '配偶职业', '配偶是否有社保', '配合是否经常出差',
            #            '配偶日常出行是否驾车', '第一个孩子性别', '第一个孩子生日', '第一个孩子疾病',
            #            '第二个孩子性别', '第二个孩子生日', '第二个孩子疾病',  '第三个孩子性别', '第三个孩子生日', '第三个孩子疾病',
            #            ]
            headers = ['nick_name', 'image', 'name', 'phone', 'wechat', 'order_time', 'gender', 'family',
                       'children_num', 'is_supportparents', 'birthday', 'disease', 'income', 'profession',
                       'has_socialsecurity', 'houseloans_total', 'houseloans_permonth', 'houseloans_years',
                       'carloans_total', 'carloans_permonth', 'carloans_years', 'offen_businesstravel', 'offen_car',
                       'city', 'spouse_birthday', 'spouse_disease', 'spouse_income', 'spouse_profession', 'spouse_security',
                       'spouse_businesstravel', 'spouse_car', 'first_child_gender', 'first_child_birthday',
                       'first_child_disease', 'second_child_gender', 'second_child_birthday', 'second_child_disease',
                       'third_child_gender', 'third_child_birthday', 'third_child_disease']
            csv_list = []
            data_template = dict()
            for item in headers:
                data_template[item] = ''
            users = self.session.query(Order).filter(Order.pay_status == 2).all()
            for user in users:
                data = data_template.copy()
                openid = user.user_openid
                base = self.session.query(User_Base).filter(User_Base.openid == openid).all()
                base = base[-1]
                data['nick_name'] = base.nickname
                data['image'] = base.image_url
                phone = self.session.query(Phone_Name).filter(Phone_Name.openid == openid).first()
                if phone:
                    data['name'], data['phone'], data['wechat'] = phone.name, str(phone.phone), phone.wx_number
                form_data = self.session.query(User_From).filter(User_From.openid == openid).first()
                data['order_time'] = user.complete_time.strftime("%Y-%m-%d %H:%M:%S")
                if form_data:
                    data['gender'] = form_data.gender
                    data['family'] = self.family_str[str(form_data.family)]
                    data['children_num'] = form_data.children_num
                    data['is_supportparents'] = self.other_str[str(form_data.is_supportparents)]
                    data['birthday'] = form_data.birthday
                    data['disease'] = form_data.disease
                    data['income'] = form_data.income
                    data['profession'] = form_data.profession
                    data['has_socialsecurity'] = self.other_str[str(form_data.has_socialsecurity)]
                    data['houseloans_total'] = form_data.houseloans_total
                    data['houseloans_permonth'] = form_data.houseloans_permonth
                    data['houseloans_years'] = form_data.houseloans_years
                    data['carloans_total'] = form_data.carloans_total
                    data['carloans_permonth'] = form_data.carloans_permonth
                    data['carloans_years'] = form_data.carloans_years
                    data['offen_businesstravel'] = self.other_str[str(form_data.offen_businesstravel)]
                    data['offen_car'] = self.other_str[str(form_data.offen_car)]
                    data['city'] = form_data.city

                    spouse = self.session.query(Spouse).filter(Spouse.id == form_data.spouse_id).first()
                    if spouse.id != 0:
                        data['spouse_birthday'] = spouse.birthday
                        data['spouse_disease'] = spouse.disease
                        data['spouse_income'] = spouse.income
                        data['spouse_profession'] = spouse.profession
                        data['spouse_security'] = self.other_str[str(spouse.has_socialsecurity)]
                        data['spouse_businesstravel'] = self.other_str[str(spouse.offen_businesstravel)]
                        data['spouse_car'] = self.other_str[str(spouse.offen_car)]

                    first_child = self.session.query(Children).filter(Children.id == form_data.first_child_id).first()
                    if first_child.id != 0:
                        data['first_child_gender'] = first_child.gender
                        data['first_child_birthday'] = first_child.birthday
                        data['first_child_disease'] = first_child.disease
                    second_child = self.session.query(Children).filter(Children.id == form_data.second_child_id).first()
                    if second_child.id != 0:
                        data['second_child_gender'] = second_child.gender
                        data['second_child_birthday'] = second_child.birthday
                        data['second_child_gender'] = second_child.disease
                    third_child = self.session.query(Children).filter(Children.id == form_data.third_child_id).first()
                    if third_child.id != 0:
                        data['third_child_gender'] = third_child.gender
                        data['third_child_birthday'] = third_child.birthday
                        data['third_child_gender'] = third_child.disease

                csv_list.append(data)

            today = datetime.datetime.now().strftime("%Y%m%d")
            csv_file = os.path.join(self.baseDir, 'user_export', '%s.csv' % today)
            with open(csv_file, 'w', newline='') as f:
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
