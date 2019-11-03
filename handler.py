# Author: AnakinJiang
# Email: jiangjinpeng319 AT gmail.com
# Time: 2019-09-26 10:02:37
# Description：请求处理，逻辑层

from abc import ABC
from urllib.request import quote
import json
from tornado.web import RequestHandler
from fileprocess import judge, deleteFolder, getPic, save_file
from core import process_12, process_34, process_56, data_visual_1, \
    data_visual_2, data_visual_3, data_visual_4, \
    data_visual_5, \
    data_visual_6
import numpy as np
import base64

root = 'files/'
IP = 'http://116.62.246.133:10010/files/'


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class IndexHandler(RequestHandler, ABC):
    def get(self):
        self.write('hello world!!!')
        self.finish()


class Core1Handler(RequestHandler, ABC):

    def post(self):
        files = self.request.files
        data = files['file'][0]["body"].decode('utf-8')
        filename = self.get_body_arguments('filename')[0]
        res = process_12(filename, data, data_visual_1)
        jsons = json.dumps(res, cls=NumpyEncoder)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(jsons)
        self.finish()


class Core2Handler(RequestHandler, ABC):

    def post(self):
        files = self.request.files
        data = files['file'][0]["body"].decode('utf-8')
        filename = self.get_body_arguments('filename')[0]
        res = process_12(filename, data, data_visual_2)
        jsons = json.dumps(res, cls=NumpyEncoder)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(jsons)
        self.finish()


class Core3Handler(RequestHandler):

    def post(self):
        files = self.request.files
        data = files['file'][0]["body"].decode('utf-8')
        filename = self.get_body_arguments('filename')[0]
        direction = self.get_body_argument('direction')
        x_step = int(self.get_body_argument('x_step'))
        x_num = int(self.get_body_argument('x_num'))
        y_step = int(self.get_body_argument('y_step'))
        y_num = int(self.get_body_argument('y_num'))
        res = process_34(filename, data, direction, x_step, x_num, y_step,
                         y_num, data_visual_3)
        jsons = json.dumps(res, cls=NumpyEncoder)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(jsons)
        self.finish()


class Core4Handler(RequestHandler):

    def post(self):
        files = self.request.files
        data = files['file'][0]["body"].decode('utf-8')
        filename = self.get_body_arguments('filename')[0]
        direction = self.get_body_argument('direction')
        x_step = int(self.get_body_argument('x_step'))
        x_num = int(self.get_body_argument('x_num'))
        y_step = int(self.get_body_argument('y_step'))
        y_num = int(self.get_body_argument('y_num'))
        res = process_34(filename, data, direction, x_step, x_num, y_step,
                         y_num, data_visual_4)
        jsons = json.dumps(res, cls=NumpyEncoder)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(jsons)
        self.finish()


class Core5Handler(RequestHandler):

    def post(self):
        files = self.request.files
        data = files['file'][0]["body"].decode('utf-8')
        filename = self.get_body_arguments('filename')[0]
        res = process_56(filename, data, data_visual_5)
        jsons = json.dumps(res, cls=NumpyEncoder)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(jsons)
        self.finish()


class Core6Handler(RequestHandler):

    def post(self):
        files = self.request.files
        data = files['file'][0]["body"].decode('utf-8')
        filename = self.get_body_arguments('filename')[0]
        res = process_56(filename, data, data_visual_6)
        jsons = json.dumps(res, cls=NumpyEncoder)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(jsons)
        self.finish()


class PicHandler(RequestHandler):

    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)
        print(json_args['filename'])
        filename = getPic(json_args['filename'], 'tmp')
        print(filename)

        retans = {}
        # 读取的模式需要根据实际情况进行修改
        for i in filename:
            with open('tmp/' + i, 'rb') as f:
                # while True:
                data = base64.b64encode(f.read())
                retans[i] = data.decode()
        jsons = json.dumps(retans, cls=NumpyEncoder)
        self.write(jsons)
        self.set_header('filenames', json_args['filename'])
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        # deleteFolder('tmp')
        self.finish()
