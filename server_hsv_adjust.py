import numpy as np
from flask import Flask, render_template, Response, request, abort
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask_sockets import Sockets
import message
from camera import VideoCamera
import time, threading
from flask import jsonify
from point import Point
from line import LinePara
from rectangle import Rectangle

msgsrv = message.MessageServer()
monkey.patch_all()

app = Flask(__name__)
sockets = Sockets(app)
app.config.update(
    DEBUG=True
)

camera = None
line = LinePara(Point(1, 1), Point(640, 480))
rect = Rectangle(Point(1, 1), Point(640, 480))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_info')
def video_info():
    if camera is None:
        video_size = (0, 0)
    else:
        video_size = camera.video_size()
    if video_size is None:
        video_size = (0, 0)
    return jsonify(video_size=video_size)


@app.route("/rect", methods=["get"])
def get_rect():
    global rect
    if rect is None:
        return jsonify(None)
    else:
        return jsonify(rect.to_json())


@app.route("/line", methods=["get"])
def get_line():
    global line
    if line is None:
        return jsonify(None)
    else:
        return jsonify(line.to_json())


@app.route('/draw_line', methods=["POST"])
def draw_line():
    j = request.get_json(True)
    if j["start"] is None or len(j["start"]) != 2:
        return "Format ERR"
    if j["end"] is None or len(j["end"]) != 2:
        return "Format ERR"
    print(j)
    global line
    start = j["start"]
    end = j["end"]
    line = LinePara(Point(start[0], start[1]), Point(end[0], end[1]))
    return "OK"


@app.route('/draw_rect', methods=["POST"])
def draw_rect():
    j = request.get_json(True)
    if j["start"] is None or len(j["start"]) != 2:
        return "Format ERR"
    if j["end"] is None or len(j["end"]) != 2:
        return "Format ERR"
    print(j)
    global rect
    start = j["start"]
    end = j["end"]
    rect = Rectangle(Point(start[0], start[1]), Point(end[0], end[1]))
    return "OK"


@app.route('/set_point_position/<int:x>/<int:y>', methods=["get"])
def set_point_position(x, y):
    global point_position
    if x == -1 or y == -1:
        point_position = None
    else:
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
    global camera
    camera = VideoCamera()
    print("start camera ...")
    while True:
        time.sleep(1)
        # cp = CirclePara(point_position, 10, (0, 0, 255))
        frame = camera.get_frame(line=line, rect=rect)
        msgsrv.add_message(frame)


def start_camero_background():
    t = threading.Thread(target=start_frame_flow, name='frame_flow')
    t.setDaemon(True)
    t.start()


if __name__ == '__main__':
    # app.run(port=5001, debug=True)
    start_camero_background()
    print("start http server ...")
    http_server = WSGIServer(('', 5001), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
