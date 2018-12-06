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
            msg['From'] = _format_addr('锦鲤保好运<%s>' % '15927260404@139.com')
            msg['To'] = 'm15927260404@163.com,15927260404@139.com'
            msg['Subject'] = Header(header, 'utf-8').encode()
            msg.attach(MIMEText(text, 'plain', 'utf-8'))

            att = MIMEText(open(send_file, 'rb').read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = "attachment; filename='%s.csv'" % today
            msg.attach(att)
            server = smtplib.SMTP_SSL('smtp.139.com', 465)
            server.set_debuglevel(1)
            server.login('15927260404@139.com', '4608310zk')
            server.sendmail('15927260404@139.com', 'm15927260404@163.com,15927260404@139.com'.split(','), msg.as_string())
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
        \n    每列代表的中文含义从左至右为 “用户微信昵称, 用户微信头像, 是否填写姓名电话, 姓名, 电话, 是否填写详细信息”
        \n    可用excel筛选功能自主选择信息
        \n
        \n备注：附件文件为.csv格式，采用utf-8编码，若使用office的excel打开出现乱码，先将文件编码改为ANSI即可
    """
    send_email(text, '锦鲤保好运（购买用户名单）')
