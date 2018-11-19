from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, DATETIME
from datetime import datetime

Base = declarative_base()


#user_base_model
class UserBase(Base):
    __tablename__ = 'user_base'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    openid = Column(VARCHAR(255), unique=True)
    nickname = Column(VARCHAR(255), nullable=False)
    image_url = Column(VARCHAR(255), nullable=False)
    gender = Column(VARCHAR(12))
    province = Column(VARCHAR(255))
    city = Column(VARCHAR(255))
    create_time = Column(DATETIME, default=datetime.now(), nullable=False)

    def keys(self):
        return [c.name for c in self.__table__.columns]


#user_form_model
class UserFrom(Base):
    __tablename__ = 'user_form'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    openid = Column(VARCHAR(255), unique=True)
    gender = Column(VARCHAR(12), nullable=False)
    family = Column(INTEGER, nullable=False)
    is_supportparents = Column(INTEGER, nullable=False)
    birthday = Column(VARCHAR(255), nullable=False)
    is_sick = Column(INTEGER, nullable=False)
    disease = Column(VARCHAR(255), default="")
    income = Column(INTEGER, nullable=False)
    profession = Column(VARCHAR(255), nullable=False)
    has_socialsecurity = Column(INTEGER, nullable=False)
    has_housloans = Column(INTEGER, nullable=False)
    houseloans_total = Column(INTEGER, default=None)
    houseloans_permonth = Column(INTEGER, default=None)
    houseloans_years = Column(INTEGER, default=None)
    has_carloans = Column(INTEGER, nullable=False)
    carloans_total = Column(INTEGER, default=None)
    carloans_permonth = Column(INTEGER, default=None)
    carloans_years = Column(INTEGER, default=None)
    offen_businesstravel = Column(INTEGER, nullable=False)
    offen_car = Column(INTEGER, nullable=False)
    city = Column(VARCHAR(255), nullable=False)
    create_time = Column(DATETIME, default=datetime.now(), nullable=False)

    def keys(self):
        return [c.name for c in self.__table__.columns]
