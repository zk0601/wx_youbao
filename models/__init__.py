from tornado.options import options
from sqlalchemy import create_engine
import config.setting

database_url = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(options.mysql_user, options.mysql_password,
                                                                    options.mysql_host, options.mysql_port,
                                                                    options.mysql_database)
Engine = create_engine(database_url, encoding='utf8', pool_size=options.pool_size,
                       pool_recycle=options.pool_recycle, echo=False, echo_pool=False)
