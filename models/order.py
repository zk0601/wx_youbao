from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, DATETIME, DECIMAL, ForeignKey
from datetime import datetime

Base = declarative_base()


#order_model
class Order(Base):
    __tablename__ = 'order'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    product_id = Column(INTEGER, ForeignKey('product.id'), nullable=False)
    product_name = Column(VARCHAR(255), nullable=False)
    product_description = Column(VARCHAR(255), nullable=False)
    total_fee = Column(DECIMAL(8, 2), nullable=False)
    create_ts = Column(DATETIME, default=datetime.now(), nullable=False)
    pay_status = Column(INTEGER, default=None)
    openid = Column(VARCHAR(255), ForeignKey('user_base.openid'), nullable=False)
    complete_time = Column(DATETIME)

    def keys(self):
        return [c.name for c in self.__table__.columns]
