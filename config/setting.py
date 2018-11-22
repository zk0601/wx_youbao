from tornado.options import define

#port
define("port", default=8888, help="run on the given port", type=int)

#mysql test
define("mysql_host", default="47.91.252.155:3306", help="database host")
define("mysql_database", default="youbao", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="123456", help="database password")

define("pool_size", default=20, help="pool size")
define("pool_recycle", default=3600, help="pool recycle")

#tornado execute threads num
define("max_workers", default=25, type=int, help="max threads")

#token
define("secret", default='Youbao~348#fgMFHz24$9deHPfL', help="token secret")

#wechat config
define("AppID", default='', help='wechat develop id')
define('APPSecret', default='', help='wechat secret')
define('merchant_id', default='', help='wechat merchant number')

define("wx_token", default='', help='wechat token')
define("EncodingAESKey", default='', help='wechat EncodingAESKey')

define("pay_key", default='', help='wechat payment key')

define("wx_access_url", default='https://api.weixin.qq.com/sns/oauth2/access_token', help='wechat access token request url')
define("wx_refresh_url", default='https://api.weixin.qq.com/sns/oauth2/refresh_token', help='wechat refresh access token')
define("wx_userinfo_url", default='https://api.weixin.qq.com/sns/userinfo', help='wechat get userinfo')
define("wx_payment_url", default="https://api.mch.weixin.qq.com/pay/unifiedorder", help='wechat order')
define("wx_orderquery_url", default="https://api.mch.weixin.qq.com/pay/orderquery", help='wechat order query')

define('server_ip', default='', help='wechat payment require a server ip')
define('notify_url', default='', help='wechat payment callback url')
