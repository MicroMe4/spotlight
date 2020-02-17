# -*- coding: utf-8 -*-
import math
import os
import sys


x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
one_deg = pi / 180.0
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方

def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

def getcoordfromfile(varfile):
    """
    :param varfile: the file you are going to read
    :return: the result of the coordinates from the file.
    """
    coord = []
    with open(varfile, "r") as Files:
        for line in Files:
            line = line.strip('\n')
            tmp = line.split(',')
            coord.append([float(tmp[0]), float(tmp[1])])
    return coord

def WriteToFile(varfile, coord):
    """
    :param varfile: the file you are going to write
    :param coord:  the coordinate you are going to write
    """
    with open(varfile, "w") as NewFiles:
        for r in range(0, len(coord)):
            NewFiles.write(str(coord[r][0]) + ',' + str(coord[r][1]) + '\n')

def distanceWGS(lat1,lon1,lat2,lon2):
    """
    :param lat1: WGS Coordinate A with latitude
    :param lon1: WGS Coordinate A with longtitude
    :param lat2: WGS Coordinate B with latitude
    :param lon2: WGS Coordinate B with longtitude
    :return: linear distance between A and B.
    """
    midval = 0.5 - math.cos((lat2-lat1)*one_deg) /2 + math.cos(lat1 * one_deg) * math.cos(lat2 * one_deg) * (1 - math.cos((lon2 - lon1) * one_deg)) / 2
    return 12742 * math.asin(math.sqrt(midval))

def getRidofSame(oldarray):
    """
    :param oldarray: the old arrays
    :return: newarray with no continous same point
    """
    newArray=[]
    newArray.append(oldarray[0])
    for i in range(1, len(oldarray)-1):
        if not (oldarray[i - 1] == oldarray[i]):
            newArray.append(oldarray[i])
    return newArray

def getRidofFloatingPoint(wgscoord,speedmeterperseoond):
    """
    :param wgscoord: It is required to be a coordinate set with (longtitude.latitude) variables
    :return: a new set with no 30m faraway set. (this is direct caculation. so maybe a litter mistake)
    """
    newArray=[]
    newArray.append(wgscoord[0])
    newArraysize=1
    for i in range(1, len(wgscoord)):
        if distanceWGS(newArray[newArraysize-1][1], newArray[newArraysize-1][0], wgscoord[i][1], wgscoord[i][0]) < speedmeterperseoond:
            newArray.append(wgscoord[i])
            newArraysize=newArraysize+1
    return newArray

def main():
    coordresr = getcoordfromfile("co.txt")
    coordresr = getRidofSame(coordresr)
    newcoordres = []
    if len(sys.argv) <= 2:
        if sys.argv[1] == "help" or len(sys.argv) == 1:
            print(sys.argv[0] + " [Data Type A] [Data Type B] (limited requirement)")
            print(" Each Data Type is one of following : WGS84, GCJ02, BD09")
            print(" (Limited requirement) is the number of 2 point's max distance")
        else:
            print("You Input Same Stuff, You know that don't u?")
    if len(sys.argv) == 3:
        coordresr = getRidofFloatingPoint(coordresr, 100)
        numberofco = len(coordresr)
        if sys.argv[1] == sys.argv[2]:
            return
        elif sys.argv[1] == "WGS84":
            if sys.argv[2] == "GCJ02":
                for i in range(0, numberofco):
                    newcoordres.append(wgs84_to_gcj02(float(coordresr[i][0]), float(coordresr[i][1])))
            elif sys.argv[2] == "BD09":
                for i in range(0, numberofco):
                    newcoordres.append(wgs84_to_bd09(float(coordresr[i][0]), float(coordresr[i][1])))
            else:
                print("No such Coordinate System")
        elif sys.argv[1] == "GCJ02":
            if sys.argv[2] == "WGS84":
                for i in range(0, numberofco):
                    newcoordres.append(gcj02_to_wgs84(float(coordresr[i][0]), float(coordresr[i][1])))
            elif sys.argv[2] == "BD09":
                for i in range(0, numberofco):
                    newcoordres.append(gcj02_to_bd09(float(coordresr[i][0]), float(coordresr[i][1])))
            else:
                print("No such Coordinate System")
        elif sys.argv[1] == "BD09":
            if sys.argv[2] == "WGS84":
                for i in range(0, numberofco):
                    newcoordres.append(bd09_to_wgs84(float(coordresr[i][0]), float(coordresr[i][1])))
            elif sys.argv[3] == "GCJ02":
                for i in range(0, numberofco):
                    newcoordres.append(bd09_to_gcj02(float(coordresr[i][0]), float(coordresr[i][1])))
            else:
                print("No such Coordinate System")
        else:
            print("Both of them are not in my caculation system!")
    elif len(sys.argv) == 4:
        coordresr = getRidofFloatingPoint(coordresr, float(sys.argv[3]))
        numberofco = len(coordresr)
        if sys.argv[1] == sys.argv[2]:
            return
        elif sys.argv[1] == "WGS84":
            if sys.argv[2] == "GCJ02":
                for i in range(0, numberofco):
                    newcoordres.append(wgs84_to_gcj02(float(coordresr[i][0]), float(coordresr[i][1])))
            elif sys.argv[2] == "BD09":
                for i in range(0, numberofco):
                    newcoordres.append(wgs84_to_bd09(float(coordresr[i][0]), float(coordresr[i][1])))
            else:
                print("No such Coordinate System")
        elif sys.argv[1] == "GCJ02":
            if sys.argv[2] == "WGS84":
                for i in range(0, numberofco):
                    newcoordres.append(gcj02_to_wgs84(float(coordresr[i][0]), float(coordresr[i][1])))
            elif sys.argv[2] == "BD09":
                for i in range(0, numberofco):
                    newcoordres.append(gcj02_to_bd09(float(coordresr[i][0]), float(coordresr[i][1])))
            else:
                print("No such Coordinate System")
        elif sys.argv[1] == "BD09":
            if sys.argv[2] == "WGS84":
                for i in range(0, numberofco):
                    newcoordres.append(bd09_to_wgs84(float(coordresr[i][0]), float(coordresr[i][1])))
            elif sys.argv[3] == "GCJ02":
                for i in range(0, numberofco):
                    newcoordres.append(bd09_to_gcj02(float(coordresr[i][0]), float(coordresr[i][1])))
            else:
                print("No such Coordinate System")
        else:
            print("Both of them are not in my caculation system!")
    if len(newcoordres) != 0:
        WriteToFile("cp.txt", newcoordres)
        os.rename("co.txt", "co_beforeProcess.txt")
        os.rename("cp.txt", "co.txt")
    return

if __name__ == '__main__':
   main()