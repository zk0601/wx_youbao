from tornado.options import define

#port
define("port", default=8888, help="run on the given port", type=int)

#mysql test
# define("mysql_host", default="47.91.252.155:3306", help="database host")
# define("mysql_database", default="youbao", help="database name")
# define("mysql_user", default="root", help="database user")
# define("mysql_password", default="123456", help="database password")
define("mysql_host", default="47.75.49.133:3306", help="database host")
define("mysql_database", default="youbao", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="4608310zk", help="database password")

define("pool_size", default=20, help="pool size")
define("pool_recycle", default=3600, help="pool recycle")

#tornado execute threads num
define("max_workers", default=25, type=int, help="max threads")

#token
define("secret", default='Youbao~348#fgMFHz24$9deHPfL', help="token secret")

#wechat config
# define("AppID", default='wxdd1aae652aa93507', help='wechat develop id')
# define('APPSecret', default='cd2cd98d1c3c34f4093a1ade46fe342d', help='wechat secret')
define("AppID", default='wx39e54711a30945e2', help='wechat develop id')
define('APPSecret', default='950cefbcc48d62ebfdbae6639f4486b4', help='wechat secret')

# define("wx_token", default='Youbao123456', help='wechat token')
# define("EncodingAESKey", default='ysV2I4oa7s9hC60TMA5TTm0Na4hk8fhLZ7krvrlXZ5d', help='wechat EncodingAESKey')
define("wx_token", default='Jinlibao230943', help='wechat token')
define("EncodingAESKey", default='URIkgXtyJ1oNJL2aSYfn7L16n0HoWDE8P37wou69O2Z', help='wechat EncodingAESKey')

# payment
define('merchant_id', default='1520796591', help='wechat merchant number')
define("pay_key", default='wJAGIl0jiSxJQEm2bU5OpmKoc5XJHQSW', help='wechat payment key')

define("wx_access_url", default='https://api.weixin.qq.com/sns/oauth2/access_token', help='wechat access token request url')
define("wx_refresh_url", default='https://api.weixin.qq.com/sns/oauth2/refresh_token', help='wechat refresh access token')
define("wx_userinfo_url", default='https://api.weixin.qq.com/sns/userinfo', help='wechat get userinfo')
define("wx_payment_url", default="https://api.mch.weixin.qq.com/pay/unifiedorder", help='wechat order')
define("wx_orderquery_url", default="https://api.mch.weixin.qq.com/pay/orderquery", help='wechat order query')

define('server_ip', default='47.110.67.202', help='wechat payment require a server ip')
define('notify_url', default='https://temp.mibaoxian.com/youbao/v1/order/paycallback', help='wechat payment callback url')

# sms
define("send_sms_url", default="http://zhibo.dejikeji.com/api/zhibo/v1/user/mobile/send", help="sms code url")
define("verify_sms_url", default="http://zhibo.dejikeji.com/api/zhibo/v1/user/mobile/verify", help="verify smscode url")
define("sms_type_code", default=311, type=int, help="verify smscode url")

# template_massage
# define('event_notice', default="TYWpdC1PcQMkEs6j4T6w6dLxUevNv2C4TQmLMw-L-Fw", help="wechat events notice id")
define('event_notice', default="QGm4AXK5GSBmx_R1hA6Rt5i8L0TSaydp1Ky8Ty6gKqs", help="wechat events notice id")
define('detail_url', default='https://temp.mibaoxian.com/phonename', help='click detail direct url')