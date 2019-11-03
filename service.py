# Filename: Environmental_data_visual
# Author: AnakinJiang
# Email: jiangjinpeng319 AT gmail.com
# Time: 2019-09-26 10:02:37
# Description：启动服务、服务相关配置

import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from handler import IndexHandler, Core1Handler, Core2Handler, Core3Handler, Core4Handler, Core5Handler, \
    Core6Handler, PicHandler

define("port", default=10010, type=int, help="run server on the given port.")
HANDLERS = [
    (r"/", IndexHandler),
    (r"/core1", Core1Handler),
    (r"/core2", Core2Handler),
    (r"/core3", Core3Handler),
    (r"/core4", Core4Handler),
    (r"/core5", Core5Handler),
    (r"/core6", Core6Handler),
    (r"/pic", PicHandler),
    (r"/files/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "files")})
]

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=HANDLERS, static_path=os.path.join(os.path.dirname(__file__), "files"),
                                  debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
