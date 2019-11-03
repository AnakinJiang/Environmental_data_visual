# Author: AnakinJiang
# Email: jiangjinpeng319 AT gmail.com
# Time: 2019-09-26 10:02:37
# Description：数据预处理、统计量计算
import numpy as np


def data_process(datas, index):
    """数据预处理，删除负数"""
    delete_list = []
    ifminus = 0
    for i, data in enumerate(datas):
        for j in data[index]:
            # print(j)
            if float(j) < 0:
                delete_list.append(i)
                ifminus = 1
                break
                # print('OK')
    datas = np.delete(datas, delete_list, axis=0)
    # print("删除缺失数据和负值后数据的维度：", datas.shape)
    return datas, ifminus


def cal_statistic(X):
    """计算数据统计量
        包括：最值、均值、方差、变异系数、百分位数
    """
    # X = np.array([X]).T
    max_value = np.max(X, axis=0)
    out = np.array([max_value])
    min_value = np.min(X, axis=0).reshape(1, X.shape[1])
    out = np.concatenate((out, min_value), axis=0)
    mean_value = np.mean(X, axis=0).reshape(1, X.shape[1])
    out = np.concatenate((out, mean_value), axis=0)
    var_value = np.var(X, axis=0).reshape(1, X.shape[1])
    out = np.concatenate((out, var_value), axis=0)
    std_value = np.std(X, axis=0).reshape(1, X.shape[1])
    variation_value = std_value / mean_value
    out = np.concatenate((out, variation_value), axis=0)
    out = np.around(out, decimals=2)
    print(out)
    return out


def data_read(filename):
    """
        读取原始文件内容，并删除缺失属性的数据
        输入：文件名
        输出：原始数据（样例数*属性）
    """

    file_data = []
    if_lose = 0  # 0表示未缺失、1表示缺失
    with open(filename) as file_obj:
        header_name = file_obj.readline().split('\t')
        header_len = len(header_name)
        # print("头文件长度：", header_len)
        height = 0
        for line in file_obj.readlines():
            data = line.strip().split('\t')
            height = height + 1
            if len(data) == header_len - 1:  # 删除缺失数据
                file_data.append(data)
            else:
                if_lose = 1
    # print("原始样本数：", height)
    # print("(样本数，横纵坐标+指标数)", np.array(file_data).shape)
    return np.array(header_name), np.array(file_data), if_lose


def headname_tran(header_names):

    for i, val in enumerate(header_names):
        if val == "Cond. [mS/m]":
            header_names[i] = "视电导率"
        if val == "Cond.[mS/m]":
            header_names[i] = "视电导率"
        elif val == "Cond.1[mS/m]":
            header_names[i] = "视电导率1"
        elif val == "Cond.1 [mS/m]":
            header_names[i] = "视电导率1"
        elif val == "Cond.2[mS/m]":
            header_names[i] = "视电导率2"
        elif val == "Cond.2 [mS/m]":
            header_names[i] = "视电导率2"
        elif val == "Cond.3[mS/m]":
            header_names[i] = "视电导率3"
        elif val == "Cond.3 [mS/m]":
            header_names[i] = "视电导率3"
        elif val == "Inphase [ppt]":
            header_names[i] = "同相位值"
        elif val == "Inphase[ppt]":
            header_names[i] = "同相位值"
        elif val == "Inph.1[ppt]":
            header_names[i] = "同相位值1"
        elif val == "Inph.1 [ppt]":
            header_names[i] = "同相位值1"
        elif val == "Inph.2[ppt]":
            header_names[i] = "同相位值2"
        elif val == "Inph.2 [ppt]":
            header_names[i] = "同相位值2"
        elif val == "Inph.3[ppt]":
            header_names[i] = "同相位值3"
        elif val == "Inph.3 [ppt]":
            header_names[i] = "同相位值3"

    return header_names


def cal_j(num):
    """
        处理经纬度数据
    """
    # print(num)
    out = []
    for x in num:
        out.append(120 + float(x[0][:-1]) / 6000)
    # print(out)
    return out


def cal_w(num):
    """
        处理经纬度数据
    """
    out = []
    for x in num:
        tmp = x[0].split('.')
        A = float(tmp[0][:-2])
        B = float(tmp[0][-2:]) + float(tmp[1][:-1]) / 10000
        # print(tmp[0][-2:])
        # print(tmp[1][:-1])

        out.append(A + B / 60)
    # print(out)
    return out


def cal_xy(direction, x_step, x_num, y_step, y_num):
    out = []
    if direction == 'x':
        for i in range(y_num):
            if i % 2 == 0:
                for j in range(x_num):
                    out.append([j * x_step, i * y_step])
            if i % 2 == 1:
                for j in range(x_num - 1, -1, -1):
                    out.append([j * x_step, i * y_step])
    if direction == 'y':
        for i in range(x_num):
            if i % 2 == 0:
                for j in range(y_num):
                    out.append([i * x_step, j * y_step])
            if i % 2 == 1:
                for j in range(y_num - 1, -1, -1):
                    out.append([i * x_step, j * y_step])
    return out
