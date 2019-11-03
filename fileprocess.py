# Author: AnakinJiang
# Email: jiangjinpeng319 AT gmail.com
# Time:2019-08-26 14:57:03
# Description：文件相关函数，包含文件类型判断、文件保存、文件删除

import datetime
import pandas as pd
import os
import numpy as np
import xlrd


def judge(filename):
    """
        读取文件判断文件类型
        输入：文件名
        返回：1到6表示文件类型
    """
    with open(filename) as file_obj:
        header_name = file_obj.readline().split('\t')
        header_len = len(header_name)
        if header_len == 13:
            return 1
        if header_len == 5:
            return 2
        if header_len == 16:
            return 3
        if header_len == 6:
            return 4
        if header_len == 15:
            return 5
        if header_len == 7:
            return 6


def excel_write(data, header_name, filename):
    attribute_names = ['统计量', '最大值', '最小值', '均值', '方差', '变异系数']
    data = pd.DataFrame(data)
    writer = pd.ExcelWriter(filename)  # 写入Excel文件
    data.index = attribute_names
    data.to_excel(writer, header=header_name, float_format='%.5f')
    writer.save()
    writer.close()


def txt_write(data, header_name, filename):
    attribute_names = [['最大值'], ['最小值'], ['均值'], ['方差'], ['变异系数']]
    print(header_name)
    print(data)
    data = np.hstack((attribute_names, data))
    tmp = ['统计量']
    tmp.extend(header_name)
    data = np.vstack((tmp, data))
    data = pd.DataFrame(data)
    writer = pd.ExcelWriter(filename)
    data.to_excel(writer, sheet_name='Sheet1', index=False, header=False, float_format='%.5f')
    writer.save()
    writer.close()
    excel_file = pd.read_excel(filename)
    excel_file.to_csv(filename[:-5] + '.csv', sep=',', index=False, encoding="utf-8", na_rep='NA')


def deleteFolder(folderPath):
    # 反向查找传入的文件夹路径最后一个字符是否为斜杠
    pos = folderPath.rfind("/")
    if pos > 0:
        # 如果文件夹路径最后一个字符不是斜杠，则在末尾添加斜杠
        folderPath = folderPath + '/'

    try:
        # 获取当前文件夹下文件列表，包括文件和文件夹
        childList = os.listdir(folderPath)
    except Exception as e:
        return e, -1
    # 如果文件夹列表为空，返回异常
    if childList is None:
        print("文件夹不合法")
        return "error", -2

    # 便利当前文件夹下文件名称列表
    for child in childList:
        # 根据判断文件有没有*.*的后缀，区分是文件还是文件夹
        isFile = child.rfind('.')
        if isFile > 0:
            # 如果是文件，对文件进行删除
            os.remove(folderPath + '/' + child)
        else:
            # 如果是目录进行递归便利
            deleteFolder(folderPath + '/' + child)
    # os.rmdir(folderPath)


def getPic(filename, path):
    picfile = []
    # filename = filename.split('/')[-1]
    for root, dirs, files in os.walk(path):
        print(files)
        root = root.split('/')[-1]
        print(root)
        print(filename)
        files = sorted(files)
        print(files)
        for i in files:
            if root + '_' in i and root + '_new' not in i:
                picfile.append(i)
    return picfile


def save_file(root, filename, data):
    if not os.path.exists(root):
        print("创建目录" + root + "成功")
        os.makedirs(root)
    path = root + filename + '/'
    if not os.path.exists(path):
        print("创建目录" + path + "成功")
        os.makedirs(path)
    relative_path = path + filename
    print("文件保存路径：", relative_path)
    with open(relative_path, 'w') as file_object:  # relative_path: files/10sxblnexh/10sxblnexh.dat
        file_object.write(data)


def save_new_file(X, Y, fileData, header_names, filename):
    data = np.hstack((X, Y))
    data = np.hstack((data, fileData))
    data = pd.DataFrame(data)
    data = pd.DataFrame(data)
    myheader = ['X', 'Y']
    myheader.extend(header_names)
    # myheader = np.array(myheader)
    # myheader = myheader.reshape((1,myheader.shape[0]))
    # myheader=np.array(myheader).reshape((1,np.array(myheader).shape[1]))
    writer = pd.ExcelWriter(filename + '_new.xlsx')
    data.to_excel(writer, sheet_name='Sheet1', header=myheader, index=False)
    writer.save()
    writer.close()
    excel_file = pd.read_excel(filename + '_new.xlsx')
    excel_file.to_csv(filename + '_new.csv', sep=',', index=False)


if __name__ == "__main__":
    filename1 = 'Data/10sxblnexh.dat'
    filename2 = 'Data/50201905.DAT'
    filename3 = 'Data/10cqexlo.dat'
    filename4 = 'Data/10sxc1.dat'
    filename5 = 'Data/10sxex02.dat'
    filename6 = 'Data/42042633.DAT'

    filename = filename5
    filetype = judge(filename)
    print(filetype)
