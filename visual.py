# Author: AnakinJiang
# Email: jiangjinpeng319 AT gmail.com
# Time: 2019-09-26 10:02:37
# Description：数据可视化实现
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.spatial import ConvexHull
import pykrige.kriging_tools as kt
from pykrige.uk import UniversalKriging
from pykrige.ok import OrdinaryKriging
import cv2


def kriging_interpolation(x, y, z):
    """
        克里金插值
    """

    grid_x = np.linspace(min(x), max(x), len(x) / 2)
    grid_y = np.linspace(min(y), max(y), len(y) / 2)
    ok = OrdinaryKriging(x, y, z, variogram_model='gaussian', verbose=False, enable_plotting=False)
    z, ss = ok.execute('grid', grid_x, grid_y)

    return grid_x, grid_y, z, None


def draw_sandian(x, y):
    print(x)
    print(y)
    plt.scatter(x, y, s=4)
    plt.xticks(np.linspace(min(x), max(x), 10))  # 带旋转
    plt.yticks(np.linspace(min(y), max(y), 10))
    plt.show()


def draw_by_object(x_new, y_new, z_new, if_gps, colorgrade, x, y, filename, headername):

    # plt.clabel(c, inline=True, fontsize=10)


    if if_gps:
        fig = plt.figure(figsize=(12.0, 8.0), facecolor="None")
        cmap = matplotlib.cm.jet
        z_min = np.min(z_new)
        z_max = np.max(z_new)
        norm = matplotlib.colors.Normalize(vmin=z_min, vmax=z_max)
        bounds = [round(elem, 2) for elem in np.linspace(z_min, z_max, colorgrade)]
        ax1 = fig.add_axes([0, 0, 0.9, 1])
        ax2 = fig.add_axes([0.9, 0.1, 0.04, 0.8])

        cs = ax1.contourf(x_new, y_new, z_new, colorgrade, cmap=plt.cm.jet)
        c = ax1.contour(x_new, y_new, z_new, colorgrade, colors='gray')
        points = np.array([x, y]).T
        hull = ConvexHull(points)
        # ax1.plot(points[:, 0], points[:, 1], 'o')
        # hull.vertices 得到凸轮廓坐标的索引值，逆时针画
        hull1 = hull.vertices.tolist()  # 要闭合必须再回到起点[0]
        hull1.append(hull1[0])
        # plt.plot(points[hull1, 0], points[hull1, 1], 'r--^', lw=2) # 连接凸包
        X = points[hull1, 0].tolist()
        Y = points[hull1, 1].tolist()

        xmax = X.index(max(X))
        xmin = X.index(min(X))
        ymax = Y.index(max(Y))
        ymin = Y.index(min(Y))
        length = len(X)

        if ymax < xmax:
            tmpX = X[xmax:length + 1] + X[0:ymax + 1]
            tmpY = Y[xmax:length + 1] + Y[0:ymax + 1]
        else:
            tmpX = X[ymax:xmax + 1]
            tmpY = Y[ymax:xmax + 1]
        tmpX.reverse()
        tmpX.append(X[xmax])
        tmpY.reverse()
        tmpY.append(Y[ymax])
        ax1.fill(tmpX, tmpY, color="w")

        if xmin < ymax:
            tmpX = X[ymax:length + 1] + X[0:xmin + 1]
            tmpY = Y[ymax:length + 1] + Y[0:xmin + 1]
        else:
            tmpX = X[ymax:xmin + 1]
            tmpY = Y[ymax:xmin + 1]
        tmpX.reverse()
        tmpX.append(X[xmin])
        tmpY.reverse()
        tmpY.append(Y[ymax])
        ax1.fill(tmpX, tmpY, color="w")

        if ymin < xmin:
            tmpX = X[xmin:length + 1] + X[0:ymin + 1]
            tmpY = Y[xmin:length + 1] + Y[0:ymin + 1]
        else:
            tmpX = X[xmin:ymin + 1]
            tmpY = Y[xmin:ymin + 1]
        tmpX.reverse()
        tmpX.append(X[xmin])
        tmpY.reverse()
        tmpY.append(Y[ymin])
        ax1.fill(tmpX, tmpY, color="w")

        if xmax < ymin:
            tmpX = X[ymin:length + 1] + X[0:xmax + 1]
            tmpY = Y[ymin:length + 1] + Y[0:xmax + 1]
        else:
            tmpX = X[ymin:xmax + 1]
            tmpY = Y[ymin:xmax + 1]
        tmpX.reverse()
        tmpX.append(X[xmax])
        tmpY.reverse()
        tmpY.append(Y[ymin])
        ax1.fill(tmpX, tmpY, color="w")

        # cb = plt.colorbar(cs)  # 增加颜色条
        cb4 = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap, boundaries=bounds, norm=norm, spacing='proportional',
                                        orientation='vertical')
        cb4.set_label('mS/m')
        path = 'files/' + filename + '/' + filename + '_' + str(headername)
        plt.savefig(path + '.png')
        plt.clf()
        img = cv2.imread(path + '.png', flags=cv2.IMREAD_COLOR)
        cut1 = img[1:800, 1:1080]
        cut2 = img[:, 1081:]
        print("123")
        cv2.imwrite(path + '.png', cut1)
        cv2.imwrite(path + '_clcbar.png', cut2)

    else:
        matplotlib.rcParams['figure.figsize'] = (12.0, 8.0)

        cs = plt.contourf(x_new, y_new, z_new, colorgrade, cmap=plt.cm.jet)
        c = plt.contour(x_new, y_new, z_new, colorgrade, colors='gray')
        cb = plt.colorbar(cs)  # 增加颜色条
        cb.set_label('mS/m')
        plt.xticks(np.linspace(min(x_new), max(x_new), 10))  # 带旋转
        plt.yticks(np.linspace(min(y_new), max(y_new), 10))
        plt.gca().xaxis.get_major_formatter().set_useOffset(False)
        plt.gca().yaxis.get_major_formatter().set_useOffset(False)
        plt.savefig('files/' + filename + '/' + filename + '_' + str(headername) + '.png')
        plt.clf()


def draw_contour(x_new, y_new, z_new, if_gps, colorgrade, x, y, filename, headername):
    """
        等高线绘制：
    """
    matplotlib.rcParams['figure.figsize'] = (24.0, 16.0)

    cs = plt.contourf(x_new, y_new, z_new, colorgrade, cmap=plt.cm.jet)
    c = plt.contour(x_new, y_new, z_new, colorgrade, colors='gray')
    # plt.clabel(c, inline=True, fontsize=10)
    # plt.scatter(x, y, s=4)

    if if_gps:
        points = np.array([x, y]).T
        hull = ConvexHull(points)
        # plt.plot(points[:, 0], points[:, 1], 'o')
        # hull.vertices 得到凸轮廓坐标的索引值，逆时针画
        hull1 = hull.vertices.tolist()  # 要闭合必须再回到起点[0]
        hull1.append(hull1[0])
        # plt.plot(points[hull1, 0], points[hull1, 1], 'r--^', lw=2) # 连接凸包
        X = points[hull1, 0].tolist()
        Y = points[hull1, 1].tolist()

        xmax = X.index(max(X))
        xmin = X.index(min(X))
        ymax = Y.index(max(Y))
        ymin = Y.index(min(Y))
        length = len(X)

        if ymax < xmax:
            tmpX = X[xmax:length + 1] + X[0:ymax + 1]
            tmpY = Y[xmax:length + 1] + Y[0:ymax + 1]
        else:
            tmpX = X[ymax:xmax + 1]
            tmpY = Y[ymax:xmax + 1]
        tmpX.reverse()
        tmpX.append(X[xmax])
        tmpY.reverse()
        tmpY.append(Y[ymax])
        plt.fill(tmpX, tmpY, color="w")

        if xmin < ymax:
            tmpX = X[ymax:length + 1] + X[0:xmin + 1]
            tmpY = Y[ymax:length + 1] + Y[0:xmin + 1]
        else:
            tmpX = X[ymax:xmin + 1]
            tmpY = Y[ymax:xmin + 1]
        tmpX.reverse()
        tmpX.append(X[xmin])
        tmpY.reverse()
        tmpY.append(Y[ymax])
        plt.fill(tmpX, tmpY, color="w")

        if ymin < xmin:
            tmpX = X[xmin:length + 1] + X[0:ymin + 1]
            tmpY = Y[xmin:length + 1] + Y[0:ymin + 1]
        else:
            tmpX = X[xmin:ymin + 1]
            tmpY = Y[xmin:ymin + 1]
        tmpX.reverse()
        tmpX.append(X[xmin])
        tmpY.reverse()
        tmpY.append(Y[ymin])
        plt.fill(tmpX, tmpY, color="w")

        if xmax < ymin:
            tmpX = X[ymin:length + 1] + X[0:xmax + 1]
            tmpY = Y[ymin:length + 1] + Y[0:xmax + 1]
        else:
            tmpX = X[ymin:xmax + 1]
            tmpY = Y[ymin:xmax + 1]
        tmpX.reverse()
        tmpX.append(X[xmax])
        tmpY.reverse()
        tmpY.append(Y[ymin])
        plt.fill(tmpX, tmpY, color="w")

        plt.gcf().set_size_inches(2400 / 100.0 / 3.0, 1600 / 100.0 / 3.0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
        plt.margins(0, 0)
        cb = plt.colorbar(cs)  # 增加颜色条
        cb.set_label('mS/m')
        path = 'files/' + filename + '/' + filename + '_' + str(headername)
        plt.savefig(path + '.png')
        plt.clf()
        img = cv2.imread(path + '.png', flags=cv2.IMREAD_COLOR)
        cut1 = img[:, 0:641]
        cut2 = img[:, 642:]
        cv2.imwrite(path + '.png', cut1)
        cv2.imwrite(path + '_clcbar.png', cut2)

    else:
        cb = plt.colorbar(cs)  # 增加颜色条
        cb.set_label('mS/m')
        plt.xticks(np.linspace(min(x_new), max(x_new), 10))  # 带旋转
        plt.yticks(np.linspace(min(y_new), max(y_new), 10))
        plt.gca().xaxis.get_major_formatter().set_useOffset(False)
        plt.gca().yaxis.get_major_formatter().set_useOffset(False)
        plt.savefig('files/' + filename + '/' + filename + '_' + str(headername) + '.png')
        plt.clf()


def run_gps(X, Y, Z, filename, header_names, if_gps, colorgrade):
    """
        对{gps+explorer}或{gps+1_4}数据进行插值并可视化
    """
    outZ = []
    outX = []
    outY = []
    print(len(X))
    print(len(Y))
    for i, z in enumerate(Z):
        print(z.shape)
        x_new, y_new, z_new, grid_shape = kriging_interpolation(X, Y, z)
        outZ.append(z_new.flatten())
        draw_by_object(x_new, y_new, z_new, if_gps, colorgrade, X, Y, filename, header_names[i])
    for j in range(len(y_new)):
        outX.append(x_new)
    for j in range(len(x_new)):
        outY.append(y_new)
    # print(outX)
    outX = np.array(outX).flatten()
    outY = np.array(outY).flatten()
    outZ = np.array(outZ)
    southwest = [min(outX), min(outY)]
    northeast = [max(outX), max(outY)]
    return outX.reshape((outX.shape[0], -1)), outY.reshape((outY.shape[0], -1)), outZ.reshape(
        (outZ.shape[1], -1)), southwest, northeast
