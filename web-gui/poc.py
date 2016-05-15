#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Patrick

references
----------
- https://alansellers.net/projects/the-button-websocket-raspberry-pi/


This temporary script file is located here:
/home/patrick/.spyder2/.temp.py
"""



import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import threading
import time

import json
import random ####


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.htm")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        self.set_nodelay(True)
        print('Socket Connected: ' + str(self.request.remote_ip))
        WebSocketHandler.waiters.add(self)

    def on_close(self):
        print('Socket disconnected: ' + str(self.request.remote_ip))
        WebSocketHandler.waiters.remove(self)

    @classmethod
    def send_updates(cls, index):
        for waiter in cls.waiters:
            try:
                waiter.write_message(index)
            except:
                print("Error sending message")

import os
static = os.getcwd()+"/static"

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static}),
    (r'/ws', WebSocketHandler)
    ])


def injectdata():
    while True:
        data = {'timestamp': time.time(),
                'Tair': random.randrange(13, 22),
                'RH': random.randrange(65,85),
                'Pbaro': random.randrange(1004, 1113),
                'dewpoint': random.randrange(-4, 9),
                'WS': random.randrange(0, 10),
                'WD': random.randrange(0,359)
                }
        WebSocketHandler.send_updates(json.dumps(data))
        time.sleep(1)


threading.Thread(target=injectdata).start()
srv = tornado.httpserver.HTTPServer(app)
srv.listen(80)
try:
    tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt, SystemExit:
    tornado.ioloop.IOLoop.instance().stop()



