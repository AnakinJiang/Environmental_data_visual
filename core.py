# Filename: Environmental_data_visual
# Author: AnakinJiang
# Email: jiangjinpeng319 AT gmail.com
# Description：核心文件，处理六种不同类型文件

import numpy as np
from dataprocess import data_process, cal_statistic, data_read, headname_tran, cal_xy, cal_j, cal_w
from fileprocess import excel_write, deleteFolder, txt_write, save_new_file, save_file, getPic
from visual import run_gps
from urllib.request import quote

ROOT = 'files/'
IP = 'http://116.62.246.133:10010/files/'


def process_12(filename, data, fun):
    save_file(ROOT, filename, data)
    path = ROOT + filename
    iflose, ifminus = fun(path, filename)
    filename = quote(filename)
    res = {'sourcefile': IP + filename + '/' + filename, 'calfile': IP + filename + '/' + filename + '.csv',
           'newfile': None, 'pic1': None, 'pic2': None, 'pic3': None, 'iflose': iflose, 'ifminus': ifminus}
    return res


def process_34(filename, data, direction, x_step, x_num, y_step, y_num, fun):
    save_file(ROOT, filename, data)

    path = ROOT + filename
    inputval, iflose, ifminus = fun(path, filename, direction, x_step, x_num, y_step, y_num)
    filename2 = getPic(filename, path)
    print(filename2)
    filename = quote(filename)
    res = {'sourcefile': IP + filename + '/' + filename, 'calfile': IP + filename + '/' + filename + '.csv',
           'newfile': IP + filename + '/' + filename + '_new.csv', 'pic1': IP + filename + '/' + quote(filename2[0]),
           'pic2': None, 'pic3': None, 'iflose': iflose, 'ifminus': ifminus, 'inputval': inputval}

    if fun == data_visual_3:
        res['pic2'] = IP + filename + '/' + quote(filename2[1])
        res['pic3'] = IP + filename + '/' + quote(filename2[2])
    return res


def process_56(filename, data, fun):
    save_file(ROOT, filename, data)
    path = ROOT + filename
    iflose, ifminus, southwest, northeast = fun(path, filename)

    filename2 = getPic(filename, path)
    filename = quote(filename)
    res = {'sourcefile': IP + filename + '/' + filename, 'calfile': IP + filename + '/' + filename + '.csv',
           'newfile': IP + filename + '/' + filename + '_new.csv', 'pic1': IP + filename + '/' + quote(filename2[0]),
           'picc1': IP + filename + '/' + quote(filename2[1]), 'pic2': None, 'picc2': None, 'pic3': None, 'picc3': None,
           'iflos': iflose, 'ifminus': ifminus, 'southwest': southwest, 'northeast': northeast}
    if fun == data_visual_5:
        res['pic2'] = IP + filename + '/' + quote(filename2[2])
        res['picc2'] = IP + filename + '/' + quote(filename2[3])
        res['pic3'] = IP + filename + '/' + quote(filename2[4])
        res['picc3'] = IP + filename + '/' + quote(filename2[5])
    return res


def data_visual_1(path, filename):
    """
        读取continual+Explorer数据，如10sxblnexh
        选取关键属性，并计算统计数据
        输入：文件
        输出：在本地保存一份文件
    """
    print("------读取并解析类型1数据------")

    header_name, file_data, iflose = data_read(path + '/' + filename)
    file_data = file_data[:, [2, 4, 6]].astype(float)
    file_data, ifminus = data_process(file_data, [0, 1, 2])
    output_name = filename + '.xlsx'
    data = cal_statistic(file_data)
    # , filename.split('/')[1].split('.')[0]
    txt_write(data, headname_tran(header_name[[2, 4, 6]]), path + '/' + output_name)
    return iflose, ifminus


def data_visual_2(path, filename):
    """
        读取continual+1_4数据，如50201905
        选取关键属性，并计算统计数据
        输入：文件
        输出：在本地保存一份文件
    """
    print("------读取并解析类型2数据------")
    header_name, fileData, iflose = data_read(path + '/' + filename)
    fileData = np.array(fileData)[:, [2]].astype(float)
    fileData, ifminus = data_process(fileData, [0])
    output_name = filename + '.xlsx'
    data = cal_statistic(fileData)
    txt_write(data, headname_tran(header_name[[2]]), path + '/' + output_name)
    return iflose, ifminus


def data_visual_3(path, filename, direction='x', x_step=2, x_num=8, y_step=3, y_num=8, colorgrade=16):
    """
        读取Manual+Explorer数据，如10cqexlo
        给定direction、x_step、x_num、y_step、y_num四个属性，构造矩阵
        选取关键属性，并计算统计数据，并插值作图
        输入：文件
        输出：在本地保存一份文件，加图片
        根据需求，若生成的点数小于实际点数，则输入点数错误，重新输入
    """

    print("------读取并解析类型3数据------")
    header_name, file_data, iflose = data_read(path + '/' + filename)
    header_names1 = headname_tran(header_name[[2, 5, 8]])
    header_names = range(len(header_name))
    if not (direction == 'x' or direction == 'y'):
        print("输入非法字符")
        return False, True, True

    index = cal_xy(direction, x_step, x_num, y_step, y_num)
    if_gps = 0  # 0表示不在地图上展示
    print("输入XY的乘积：", len(index))
    if len(index) < len(file_data):
        print("用户输入数据有误")
        return False, True, True
    else:

        file_data = file_data[:, [2, 5, 8]].astype(float)
        file_data, ifminus = data_process(file_data, [0, 1, 2])

        index = index[:len(file_data)]
        index = list(zip(*index))
        x = list(index[0])
        y = list(index[1])
        output_name = filename + '.xlsx'
        data = cal_statistic(file_data)
        txt_write(data, header_names1, path + '/' + output_name)
        x, y, z, _, _ = run_gps(x, y, file_data.T, filename, header_names, if_gps, colorgrade)
        save_new_file(x, y, z, header_names1, path + '/' + filename)
    return True, iflose, ifminus


def data_visual_4(path, filename, direction='x', x_step=2, x_num=16, y_step=3, y_num=16, colorgrade=16):
    """
        读取Manual+1_4数据，如10sxc1
        给定direction、x_step、x_num、y_step、y_num四个属性，构造矩阵
        选取关键属性，并计算统计数据，并插值作图
        输入：文件
        输出：在本地保存一份文件，加图片
        根据需求，若生成的点数小于实际点数，则输入点数错误，重新输入
    """

    print("------读取并解析类型4数据------")
    header_name, file_data, iflose = data_read(path + '/' + filename)
    header_names1 = headname_tran(header_name[[2]])
    header_names = range(len(header_name))
    if not (direction == 'x' or direction == 'y'):
        print("输入非法字符")
        return False, True, True
    index = cal_xy(direction, x_step, x_num, y_step, y_num)
    if_gps = 0  # 0表示不在地图上展示
    print("输入XY的乘积：", len(index))
    print("实际点数：", len(file_data))
    if len(index) < len(file_data):
        print("用户输入数据有误")
        return False, True, True
    else:

        file_data = file_data[:, [2]].astype(float)
        print(file_data.shape)
        file_data, ifminus = data_process(file_data, [0])
        index = index[:len(file_data)]
        index = list(zip(*index))
        X = list(index[0])
        Y = list(index[1])
        output_name = filename + '.xlsx'
        data = cal_statistic(file_data)
        txt_write(data, header_names1, path + '/' + output_name)
        X, Y, Z, _, _ = run_gps(X, Y, file_data.T, filename,
                                header_names, if_gps, colorgrade)
        save_new_file(X, Y, Z, header_names1, path + '/' + filename)
    return True, iflose, ifminus


def data_visual_5(path, filename, colorgrade=16):
    """
        读取GPS+Explorer数据，如10sxex02
        给定direction、x_step、x_num、y_step、y_num四个属性，构造矩阵
        选取关键属性，并计算统计数据，并插值作图
        输入：文件
        输出：在本地保存一份文件，加图片
    """

    print("------读取并解析类型5数据------")
    header_name, fileData, iflose = data_read(path + '/' + filename)
    header_names1 = headname_tran(header_name[[4, 6, 8]])
    header_names = range(len(header_name))
    if_gps = 1  # 1表示在地图上展示
    fileData = fileData[:, [0, 1, 4, 6, 8]]
    fileData, ifminus = data_process(fileData, [2, 3, 4])
    X = cal_w(fileData[:, [0]])
    Y = cal_w(fileData[:, [1]])
    fileData = fileData[:, [2, 3, 4]].astype(float)
    # print(fileData)
    output_name = filename + '.xlsx'
    data = cal_statistic(fileData)
    txt_write(data, header_names1, path + '/' + output_name)

    # file_save(X,Y,fileData)
    X, Y, Z, southwest, northeast = run_gps(np.array(X), np.array(Y), fileData.T,
                                            filename, header_names, if_gps, colorgrade)
    save_new_file(X, Y, Z, header_names1, path + '/' + filename)

    return iflose, ifminus, southwest, northeast


def data_visual_6(path, filename, colorgrade=16):
    """
        读取GPS+1_4数据，如42042633
        给定direction、x_step、x_num、y_step、y_num四个属性，构造矩阵
        选取关键属性，并计算统计数据，并插值作图
        输入：文件
        输出：在本地保存一份文件，加图片
    """

    print("------读取并解析类型6数据------")
    header_name, file_data, iflose = data_read(path + '/' + filename)
    header_names1 = headname_tran(header_name[[4]])
    header_names = range(len(header_name))
    if_gps = 1  # 1表示在地图上展示
    file_data = file_data[:, [0, 1, 4]]
    file_data, ifminus = data_process(file_data, [2])
    Y = cal_w(file_data[:, [1]])  # 计算维度
    X = cal_w(file_data[:, [0]])  # 计算经度
    file_data = file_data[:, [2]].astype(float)
    output_name = filename + '.xlsx'
    data = cal_statistic(file_data)
    # excel_write(data, str(header_names), path+'/'+output_name)
    txt_write(data, header_names1, path + '/' + output_name)

    # file_save(X,Y,fileData)
    X, Y, Z, southwest, northeast = run_gps(np.array(X), np.array(Y), file_data.T,
                                            filename, header_names, if_gps, colorgrade)
    save_new_file(X, Y, Z, header_names1, path + '/' + filename)
    return iflose, ifminus, southwest, northeast
