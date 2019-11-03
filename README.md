<!--
 * @Author: AnakinJiang
 * @Email: jiangjinpeng319 AT gmail.com
 * @Descripttion: 
 * @Date: 2019-11-01 10:57:04
 * @LastEditors: AnakinJiang
 * @LastEditTime: 2019-11-01 10:57:05
 -->
# Environmental_data_visual
## 项目概述

场地数据可视化，使用tornado搭建服务，克里金插值法进行差值，同时白化凸包。

## 环境安装

操作系统：Ubuntu 18.04
### Anaconda安装
下载Anaconda，去[官网](https://www.anaconda.com/distribution/#linux)下载对应版本
进入下载目录，输入以下指令下载
```angular2
$ sudo bash Anaconda3-5.3.0-Linux-x86_64.sh
```
一直按回车或yes完成安装，完成安装，接下来配置环境变量，在终端输入
```
$ sudo gedit ~/.bashrc
```
然后加入
```angular2
export PATH=~/anaconda3/bin:$PATH
```
更新配置：
```angular2
$ source ~/.bashrc
```
输入python，若显示Anaconda 则表示安装成功
### 虚拟环境安装
创建虚拟环境，并进入环境

```bash
$ conda create -n environment python=3.6
$ source activate environment
$ pip install --upgrade pip
$ pip install autopep8
```

安装相关配置

```bash
$ pip install -r requirements.txt
```

在云服务上配置环境，需要提前配置以下环境：

```bash
$ apt-get update
$ apt-get install apt-file
$ apt-file update
$ apt-file search libSM.so.6
$ apt-get install libsm6
$ apt-get install libxrender1
```
## 工程说明

- file：测试数据
- core.py：核心文件，处理六种不同类型文件
- visual.py：数据可视化实现
- dataprocess.py：数据预处理、统计量计算
- handler.py：请求处理，逻辑层
- fileprocess.py：文件相关函数，包含文件类型判断、文件保存、文件删除
- service.py：启动服务、服务相关配置
- requirements.txt：环境依赖
- requestsTest.py：请求测试

## 运行
若要运行requestsTest.py，则需要设定数据集路径
```python
$ python service.py
```

