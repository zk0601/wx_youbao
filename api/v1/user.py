from tornado.concurrent import run_on_executor
from ..base import BaseHandler
import datetime
import traceback

from models.user import UserBase, UserFrom, Spouse, Children
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
            self.logger.error(e)
            print(traceback.print_exc())
            self.session.rollback()
            return self.response(code=10000, msg='服务端异常')


class UserStoreInfoHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            openid = self.get_argument("openid", None)
            form_data = self.get_argument("form_data", None)
            self_people = form_data["self_people", None]

            if not openid or not form_data or not self_people:
                return self.response(code=10002, msg='参数错误')

            gender = self_people["gender"]
            family = int(self_people["family"])
            if family == 2 or family == 4:
                spouse = form_data["spouse"]
                spouse_birthday = spouse["birthday"]
                spouse_is_sick = int(spouse["is_sick"])
                if spouse_is_sick == 1:
                    spouse_disease = spouse["disease"]
                else:
                    spouse_disease = ''
                spouse_income = int(spouse["income"])
                spouse_profession = spouse["profession"]
                spouse_has_socialsecurity = int(spouse["has_socialsecurity"])
                spouse_offen_businesstravel = int(spouse["offen_businesstravel"])
                spouse_offen_car = int(spouse["offen_car"])
                s = Spouse(birthday=spouse_birthday, is_sick=spouse_is_sick, disease=spouse_disease, income=spouse_income,
                           profession=spouse_profession, has_socialsecurity=spouse_has_socialsecurity,
                           offen_businesstravel=spouse_offen_businesstravel, offen_car=spouse_offen_car)
                self.session.add(s)
                self.session.flush()
                spouse_id = s.id
            else:
                spouse_id = 0
            if family == 3 or family == 4:
                children = form_data["children"]
                child_list = []
                for child in children:
                    child_gender = child["gender"]
                    child_birthday = child["birthday"]
                    child_is_sick = int(child["is_sick"])
                    if child_is_sick == 1:
                        child_disease = child["disease"]
                    else:
                        child_disease = ''
                    c = Children(gender=child_gender, birthday=child_birthday, is_sick=child_is_sick, disease=child_disease)
                    self.session.add(c)
                    self.session.flush()
                    child_list.append(c.id)
                if len(child_list) == 3:
                    first_child_id, second_child_id, third_child_id = child_list[0], child_list[1], child_list[2]
                elif len(child_list) == 2:
                    first_child_id, second_child_id, third_child_id = child_list[0], child_list[1], 0
                elif len(child_list) == 1:
                    first_child_id, second_child_id, third_child_id = child_list[0], 0, 0
                else:
                    first_child_id, second_child_id, third_child_id = 0, 0, 0
            else:
                first_child_id, second_child_id, third_child_id = 0, 0, 0

            children_num = int(self_people["children_num"])
            is_supportparents = int(self_people["is_supportparents"])
            birthday = str(self_people["birthday"])
            is_sick = int(self_people["is_sick"])
            if is_sick == 1:
                disease = self_people["disease"]
            else:
                disease = ''
            income = int(self_people["income"])
            profession = self_people["profession"]
            has_socialsecurity = int(self_people["has_socialsecurity"])
            has_housloans = int(self_people["has_housloans"])
            if has_housloans == 1:
                houseloans_total = int(self_people["houseloans_total"])
                houseloans_permonth = int(self_people["houseloans_permonth"])
                houseloans_years = int(self_people["houseloans_years"])
            else:
                houseloans_total, houseloans_permonth, houseloans_years = 0, 0, 0
            has_carloans = int(self_people["has_carloans"])
            if has_carloans == 1:
                carloans_total = self_people["carloans_total"]
                carloans_permonth = self_people["carloans_permonth"]
                carloans_years = self_people["carloans_years"]
            else:
                carloans_total, carloans_permonth, carloans_years = 0, 0, 0
            offen_businesstravel = int(self_people["offen_businesstravel"])
            offen_car = int(self_people["offen_car"])
            city = self_people["city"]
            name = self_people["name"]
            phone = str(self_people["phone"])

            user = self.session.query(UserFrom).filter(UserFrom.openid == openid).first()
            if not user:
                user = UserFrom(openid=openid, gender=gender, family=family, children_num=children_num, spouse_id=spouse_id,
                                first_child_id=first_child_id, second_child_id=second_child_id, third_child_id=third_child_id,
                                is_supportparents=is_supportparents,
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
                user.children_num = children_num
                user.spouse_id = spouse_id
                user.first_child_id = first_child_id
                user.second_child_id = second_child_id
                user.third_child_id = third_child_id
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
            print(traceback.print_exc())
            self.session.rollback()
            return self.response(code=10000, msg='服务端异常')
