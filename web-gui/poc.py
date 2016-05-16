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
import socket
import os


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

static = os.getcwd()+"/static"

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 
                                    os.path.join(os.getcwd(), 'static')}),
    (r'/ws', WebSocketHandler)
    ])


kplex = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kplex.connect(('',10110))
nmea_port = kplex.makefile()

def post_new_data():
    while True:
        try:
            msg = nmea_port.readline()
            if msg.startswith('$WIMDA'):
                (_,_,_,P,_,T,_,_,_,RH,_,DP,_,WD,_,_,_,_,_,WS,_)=msg.split(',')
                P = str(1000*float(P)) # bar -> mbar
                data = {'tstamp': time.time(), # time, unix epoch
                        'T': T,    # air temp., *C
                        'RH': RH,  # rel. humidity, %
                        'P': P,    # air press., mb
                        'DP': DP,  # dewpoint, *C
                        'WS': WS,  # wind speed, m/s
                        'WD': WD } # wind direction, *TN
                WebSocketHandler.send_updates(json.dumps(data))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            continue

threading.Thread(target=post_new_data).start()

srv = tornado.httpserver.HTTPServer(app)
srv.listen(80)
try:
    tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt, SystemExit:
    tornado.ioloop.IOLoop.instance().stop()



