from tornado.concurrent import run_on_executor
from ..base import BaseHandler
import datetime

from models.user import UserBase, UserFrom
from utils.wx_requests import wx_get_userinfo, wx_get_access_token, wx_refresh_access_token


class UserLoginHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            code = self.get_argument("code", None)
            if not code:
                return self.response(code=10002, msg='缺失code')

            res_data = wx_get_access_token(code)
            if "errcode" in res_data:
                return self.response(code=10002, msg="%s:%s" % (res_data['errcode'], res_data['errmsg']))
            else:
                access_token = res_data["access_token"]
                refresh_token = res_data["refresh_token"]
                openid = res_data["openid"]

                user_info = wx_get_userinfo(access_token, openid)
                if "errcode" in user_info:
                    if int(user_info["errcode"]) == 40014:
                        access_token_res = wx_refresh_access_token(refresh_token)
                        if "errcode" in access_token_res:
                            return self.response(code=10002, msg="%s:%s" % (access_token_res['errcode'], access_token_res['errmsg']))
                        else:
                            user_info = wx_get_userinfo(access_token_res["access_token"], openid)
                    else:
                        return self.response(code=10002, msg="%s:%s" % (user_info['errcode'], user_info['errmsg']))
                if "errcode" in user_info:
                    return self.response(code=10002, msg="%s:%s" % (user_info['errcode'], user_info['errmsg']))
                else:
                    openid = user_info["openid"]
                    nickname = user_info["nickname"]
                    sex = user_info["sex"]
                    province = user_info["province"]
                    city = user_info["city"]
                    country = user_info["country"]
                    headimgurl = user_info["headimgurl"]

                    user = UserBase(openid=openid, nickname=nickname, image_url=headimgurl, gender=sex, province=province,
                                    city=city, country=country, create_time=datetime.datetime.now())
                    self.session.add(user)
                    self.session.commit()

                    userid = user.id
                    token = self.encode(userid, openid)
                    data = {'openid': openid, 'token': token}

                    return self.response(data=data, code=10001, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            self.session.rollback()
            return self.response(code=10000, msg='服务端异常')


class UserStoreInfoHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            openid = self.get_argument("openid", None)
            form_data = self.get_argument("form_data", None)

            if not openid or not form_data:
                return self.response(code=10002, msg='参数错误')

            gender = form_data["gender"]
            family = int(form_data["family"])
            is_supportparents = int(form_data["is_supportparents"])
            birthday = str(form_data["birthday"])
            is_sick = int(form_data["is_sick"])
            if is_sick == 1:
                disease = form_data["disease"]
            else:
                disease = ''
            income = int(form_data["income"])
            profession = form_data["profession"]
            has_socialsecurity = int(form_data["has_socialsecurity"])
            has_housloans = int(form_data["has_housloans"])
            if has_housloans == 1:
                houseloans_total = int(form_data["houseloans_total"])
                houseloans_permonth = int(form_data["houseloans_permonth"])
                houseloans_years = int(form_data["houseloans_years"])
            else:
                houseloans_total, houseloans_permonth, houseloans_years = '', '', ''
            has_carloans = int(form_data["has_carloans"])
            if has_carloans == 1:
                carloans_total = form_data["carloans_total"]
                carloans_permonth = form_data["carloans_permonth"]
                carloans_years = form_data["carloans_years"]
            else:
                carloans_total, carloans_permonth, carloans_years = '', '', ''
            offen_businesstravel = int(form_data["offen_businesstravel"])
            offen_car = int(form_data["offen_car"])
            city = form_data["city"]
            name = form_data["name"]
            phone = str(form_data["phone"])

            user = self.session.query(UserFrom).filter(UserFrom.openid == openid).first()
            if not user:
                user = UserFrom(openid=openid, gender=gender, family=family, is_supportparents=is_supportparents,
                                birthday=birthday, is_sick=is_sick, disease=disease, income=income, profession=profession,
                                has_socialsecurity=has_socialsecurity, has_housloans=has_housloans, houseloans_total=houseloans_total,
                                houseloans_permonth=houseloans_permonth, houseloans_years=houseloans_years, has_carloans=has_carloans,
                                carloans_total=carloans_total, carloans_permonth=carloans_permonth, carloans_years=carloans_years,
                                offen_businesstravel=offen_businesstravel, offen_car=offen_car, city=city, name=name,
                                phone=phone, create_time=datetime.datetime.now())
                self.session.add(user)
            else:
                user.gender = gender
                user.family = family
                user.is_supportparents = is_supportparents
                user.birthday = birthday
                user.is_sick = is_sick
                user.disease = disease
                user.income = income
                user.profession = profession
                user.has_socialsecurity = has_socialsecurity
                user.has_housloans = has_housloans
                user.houseloans_total = houseloans_total
                user.houseloans_permonth = houseloans_permonth
                user.houseloans_years = houseloans_years
                user.has_carloans = has_carloans
                user.carloans_total = carloans_total
                user.carloans_permonth = carloans_permonth
                user.carloans_years = carloans_years
                user.offen_businesstravel = offen_businesstravel
                user.offen_car = offen_car
                user.city = city
                user.name = name
                user.phone = phone
            self.session.commit()

            return self.response(code=10000, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            self.session.rollback()
            return self.response(code=10000, msg='服务端异常')
