#coding:utf-8
import smtplib
import traceback
import datetime
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr, parseaddr


def send_email(text, header):
    while True:
        try:
            today = datetime.datetime.now().strftime("%Y%m%d")
            send_file = os.path.join(os.path.dirname(__file__), "user_export", "%s.csv" % today)
            msg = MIMEMultipart()
            msg['From'] = _format_addr('锦鲤好运保<%s>' % '15927260404@139.com')
            msg['To'] = '934170914@qq.com'
            # msg['To'] = '15927260404@139.com'
            msg['Subject'] = Header(header, 'utf-8').encode()
            msg.attach(MIMEText(text, 'plain', 'utf-8'))

            att = MIMEText(open(send_file, 'rb').read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = "attachment; filename='%s.csv'" % today
            msg.attach(att)
            server = smtplib.SMTP_SSL('smtp.139.com', 465)
            server.set_debuglevel(1)
            server.login('15927260404@139.com', '4608310zk')
            server.sendmail('15927260404@139.com', '934170914@qq.com'.split(','), msg.as_string())
            # server.sendmail('15927260404@139.com', '15927260404@139.com'.split(','), msg.as_string())
            break

        except Exception as e:
            print(traceback.print_exc())
            continue


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


if __name__ == '__main__':
    text = """
        此名单为所有用户购买名单，不区分日期。
        \n    可用excel筛选功能自主选择信息
        \n    列名解释：
        \n              nick_name : 用户微信昵称\t
                        image : 用户微信头像\t
                        name : 姓名\t
                        phone : 电话\t
                        wechat : 微信\t
                        order_time : 订单支付时间\t
                        gender : 性别\t
                        family : 家庭情况\t
                        children_num : 孩子数量\t
                        is_supportparents : 是否赡养父母\t
                        birthday : 出生日期\t
                        disease : 疾病\t
                        income : 年收入（万元）\t
                        profession : 职业\t
                        has_socialsecurity : 是否有社保\t
                        houseloans_total : 房贷总额（万元）\t
                        houseloans_permonth : 房贷月供（元）\t
                        houseloans_years : 还需还款年数\t
                        carloans_total : 车贷总额（万元）\t
                        carloans_permonth : 车贷月供（元）\t
                        carloans_years : 还需还款年数\t
                        offen_businesstravel : 是否经常出差\t
                        offen_car : 日常出行是否驾车\t
                        city : 所在城市\t
                        spouse_birthday : 配偶生日\t
                        spouse_disease : 配偶疾病\t
                        spouse_income : 配偶收入（万元）\t
                        spouse_profession : 配偶职业\t
                        spouse_security : 配偶是否有社保\t
                        spouse_businesstravel : 配合是否经常出差\t
                        spouse_car : 配偶日常出行是否驾车\t
                        first_child_gender : 第一个孩子性别\t
                        first_child_birthday : 第一个孩子生日\t
                        first_child_disease : 第一个孩子疾病\t
                        second_child_gender : 第二个孩子性别\t
                        second_child_birthday : 第二个孩子生日\t
                        second_child_disease : 第二个孩子疾病\t
                        third_child_gender : 第三个孩子性别\t
                        third_child_birthday : 第三个孩子生日\t
                        third_child_disease : 第三个孩子疾病\t
        \n
        \n备注：附件文件为.csv格式，采用utf-8编码，若使用office的excel打开出现乱码，先将文件编码改为ANSI即可
    """
    send_email(text, '锦鲤保好运（购买用户名单）')
