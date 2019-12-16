from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, DATETIME, DECIMAL

Base = declarative_base()


#product_model
class Product(Base):
    __tablename__ = 'product'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    price = Column(DECIMAL(8, 2), nullable=False)
    description = Column(TEXT, nullable=False)
    sell_amount = Column(INTEGER, nullable=False, default=0)
    is_available = Column(INTEGER, nullable=False, default=1)

    def keys(self):
        return [c.name for c in self.__table__.columns]


if __name__ == '__main__':
    from models import Engine
    Base.metadata.create_all(Engine)
