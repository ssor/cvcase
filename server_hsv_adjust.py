import cv2
import numpy as np
from flask import Flask, render_template, Response, request, abort
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask_sockets import Sockets
import message
from camera import VideoCamera
from circle import CirclePara
import time, threading

msgsrv = message.MessageServer()
monkey.patch_all()

app = Flask(__name__)
sockets = Sockets(app)
app.config.update(
    DEBUG=True
)
point_position = (0, 0)


@app.route('/')
def index():
    return render_template('index.html', point_position_x=point_position[0], point_position_y=point_position[1])


@app.route('/set_point_position/<int:x>/<int:y>', methods=["get"])
def set_point_position(x, y):
    global point_position
    point_position = (x, y)
    print("new point -> (%d,%d)" % (x, y))
    return "OK"


@sockets.route('/ws')
def message(ws):
    print("new ws ...")
    while not ws.closed:
        msgsrv.observers.append(ws)
        message = ws.receive()
        if message:
            print("client msg <- ", message)
            # msgsrv.add_message("echo: %s" % message)
    return "Connected!"


def start_frame_flow():
    camera = VideoCamera()
    print("start camera ...")
    while True:
        time.sleep(0.1)
        cp = CirclePara(point_position, 10, (0, 0, 255))
        frame = camera.get_frame(cp)
        # print("frame out ...")
        msgsrv.add_message(frame)


if __name__ == '__main__':
    t = threading.Thread(target=start_frame_flow, name='frame_flow')
    t.setDaemon(True)
    t.start()
    print("start http server ...")
    http_server = WSGIServer(('', 5001), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
