import requests
from tornado.options import options
import config.setting


def wx_get_access_token(code):
    data = {
        "appid": options.AppID,
        "secret": options.APPSecret,
        "code": code,
        "grant_type": "authorization_code"
    }
    res = requests.get(options.wx_access_url, params=data)
    return res.json()


def wx_refresh_access_token(refresh_token):
    data = {
        "appid": options.AppID,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    res = requests.get(options.wx_refresh_url, params=data)
    return res.json()


def wx_get_userinfo(access_token, openid):
    data = {
        "access_token": access_token,
        "openid": openid,
        "lang": "zh_CN"
    }
    res = requests.get(options.wx_userinfo_url, params=data)
    return res.json()
