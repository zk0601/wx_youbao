from tornado.options import options
import config.setting
import requests
import datetime
import json
import os


def get_token():
    access_token_file = os.path.join(os.path.dirname(__file__), "access_token.txt")
    with open(access_token_file, "r") as f:
        content = f.read()
        data_dict = eval(content)
        time = datetime.datetime.strptime(data_dict["time"], '%Y-%m-%d %H:%M:%S')

    if (datetime.datetime.now()-time).seconds < 7000:
        return data_dict["access_token"]
    else:
        data = {
            'grant_type': 'client_credential',
            'appid': options.AppID,
            'secret': options.APPSecret
        }
        url = 'https://api.weixin.qq.com/cgi-bin/token'

        res = requests.get(url, params=data, timeout=10)
        access_token = res.json().get("access_token")
        content = "{'access_token':" + str(access_token) + ",'time':" + "'" + \
                  str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "'" + "}"
        with open(access_token_file, "w") as f:
            f.write(content)
        return access_token


def send_template_msg(openid):
    data = {
        "touser": openid,
        "template_id": options.event_notice,
        "url": options.detail_url,
        "data": {
            "first": {
                "value": "您好，如您已完成支付，请及时填写联系方式以便客服与您联系！",
                "color": "#FF0000"
            },
            "keyword1": {
                "value": "如有问题，您可选择自动联系客服，添加客服微信号",
                "color": "#173177"
            },
            "keyword2": {
                "value": "GaoYang-NPU",
                "color": "#173177"
            },
            "keyword3": {
                "value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "color": "#173177"
            },
            "remark": {
                "value": "请您及时处理！",
                "color": "#173177"
            }
        }
    }
    json_template = json.dumps(data)
    access_token = get_token()
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_token
    res = requests.post(url, data=json_template)
    return res.json()


if __name__ == '__main__':
    get_token()