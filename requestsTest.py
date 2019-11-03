# Author: AnakinJiang
# Email: jiangjinpeng319 AT gmail.com
# Time: 2019-09-26 10:02:37
# Description：模拟客户端向服务器发起请求
import requests
import json
import os
import base64

# root 表示原始数据的路径


def multi_test(arg, filename):
    files = {'file': [filename.split('/')[-1], open(filename, 'rb'), "text/plain"]}
    url = "http://116.62.246.133:10010/core" + str(arg['code'])
    resp = requests.post(url, data=arg, files=files)
    content = resp.content.decode('utf-8')
    print(json.loads(content))


# def judge_test(path, filename):
#     url = "http://59.78.194.95:10010/judge"
#     files = {'file': [filename, open(path + '/' + filename, 'rb'), "text/plain"]}
#     resp = requests.post(url, files=files)requestsTest.py:18
#     return resp.content


# def testCore(code, filename, fun, arg=None):
#     url = "http://59.78.194.95:10010/" + fun
#
#     data = {
#         'code': code,
#         'filename': filename,
#         'arg': arg
#     }
#     resp = requests.post(url, data=json.dumps(data))
#     if not os.path.exists('Output'):
#         print("创建目录成功")
#         os.makedirs('Output')
#     # if not resp.headers['filename']==None:
#     #     filename = resp.headers['filename']
#     #     print(filename)
#     file1 = json.loads(resp.content.decode('utf-8'))['fileurl']
#     file2 = json.loads(resp.content.decode('utf-8'))['pic_url1']
#     file3 = json.loads(resp.content.decode('utf-8'))['pic_url2']
#     file4 = json.loads(resp.content.decode('utf-8'))['pic_url3']
#     file5 = json.loads(resp.content.decode('utf-8'))['pic_url4']
#     file6 = json.loads(resp.content.decode('utf-8'))['pic_url5']
#     file7 = json.loads(resp.content.decode('utf-8'))['pic_url6']
#     print(file1)
#     print(file2)
#     print(file3)
#     print(file4)
#     print(file5)
#     print(file6)
#     print(file7)


if __name__ == "__main__":
    # 原始数据路径
    root = '/media/jinpengjiang/DataSet/Environment'
    # code:1
    CON_CMDEX = 'CON_CMDEX.dat'
    CON_CMDEX_USB = 'CON_CMDEX_USB.DAT'
    # code:2
    CON_CMD1 = 'CON_CMD1.dat'
    CON_CMD1_USB = 'CON_CMD1_USB.DAT'
    CON_CMD4 = 'CON_CMD4.dat'
    CON_CMD4_USB = 'CON_CMD4_USB.DAT'
    # code:3
    MAN_CMDEX = 'MAN_CMDEX.dat'
    # code:4
    MAN_CMD1 = 'MAN_CMD1.dat'
    MAN_CMD1_USB = 'MAN_CMD1_USB.DAT'
    MAN_CMD4 = 'MAN_CMD4.dat'
    MAN_CMD4_USB = 'MAN_CMD4_USB.DAT'
    # code:5
    GPSCON_CMDEX = 'GPSCON_CMDEX.dat'
    GPSCON_CMDEX_USB = 'GPSCON_CMDEX_USB.DAT'
    # code:6
    GPSCON_CMD1 = 'GPSCON_CMD1.dat'
    GPSCON_CMD1_USB = 'GPSCON_CMD1_USB.DAT'
    GPSCON_CMD4 = 'GPSCON_CMD4.dat'
    GPSCON_CMD4_USB = 'GPSCON_CMD4_USB.DAT'

    args = {
        'code': 3,
        'direction': 'x',
        'x_step': 2,
        'x_num': 8,
        'y_step': 3,
        'y_num': 8,
        'colorgrade': 16,
        'filename': MAN_CMDEX[:-4]
    }
    multi_test(args, root + '/' + MAN_CMDEX)
