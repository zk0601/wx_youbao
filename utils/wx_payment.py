import requests
import hashlib
import datetime
from random import Random
from bs4 import BeautifulSoup
from tornado.options import options
import config.setting


def request_prepayment(openid, total_fee, out_trade_no, orderid):
    post_data = {
        "appid": options.AppID,
        "mch_id": options.merchant_id,
        "nonce_str": random_str(16),
        "sign_type": "MD5",
        "body": "wrapspeed",
        "out_trade_no": out_trade_no,
        "total_fee": total_fee,
        "spbill_create_ip": options.server_ip,
        "notify_url": options.notify_url,
        "trade_type": "JSAPI",
        "openid": openid,
        "attach": orderid
    }
    sign = get_sign(post_data)
    post_data['sign'] = sign
    res = requests.post(options.wx_payment_url, data=trans_dict_to_xml(post_data))
    res_data = trans_xml_to_dict(res.content)
    return res_data


def random_str(randomlength):
    """
    生成随机字符串
    :param randomlength: 字符串长度
     :return:
    """
    ret_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        ret_str += chars[random.randint(0, length)]
    return ret_str


def order_num(phone):
    """
    生成内部订单号,
    :param phone:
    :return:
    """
    local_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    result = phone + 'T' + local_time + random_str(5)
    return result


def get_sign(data_dict):
    # 签名函数，参数为签名的数据和密钥
    params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)
    params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + options.pay_key
    md5 = hashlib.md5()
    md5.update(params_str.encode('utf-8'))
    sign = md5.hexdigest().upper()
    return sign


def trans_dict_to_xml(data_dict):
    data_xml = []
    for key in sorted(data_dict.keys()):
        value = data_dict.get(key)
        if key == 'detail' and not value.startswith('<![CDATA['):  # 添加XML标记
            value = '<![CDATA[{}]]>'.format(value)
        data_xml.append('<{key}>{value}</{key}>'.format(key=key, value=value))
    return '<xml>{}</xml>'.format(''.join(data_xml)).encode('utf-8')


def trans_xml_to_dict(data_xml):
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict


def request_query_order(out_trade_no):
    data = {
        "appid": options.AppID,
        "mch_id": options.merchant_id,
        "out_trade_no": out_trade_no,
        "nonce_str": random_str(16),
        "sign_type": "MD5"
    }
    sign = get_sign(data)
    data["sign"] = sign
    res = requests.post(options.wx_orderquery_url, data=trans_dict_to_xml(data))
    res_data = trans_xml_to_dict(res.content)
    return res_data
