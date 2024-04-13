import math
from utils._transformlat import _transformlat
from utils._transformlng import _transformlng
from utils.out_of_china import out_of_china
from utils.wgs84_to_gcj02 import wgs84_to_gcj02

# 坐标纠偏
x_pi = 3.14159265358979324 * 3000.0 / 180.0
# 圆周率π
pi = 3.1415926535897932384626
# 长半轴长度
a = 6378245.0
# 地球的角离心率
ee = 0.00669342162296594323
# 矫正参数
interval = 0.000001

def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:列表返回
    """
    # 判断是否在国内
    if out_of_china(lng, lat):
        return lng, lat

    dlng = _transformlng(lng - 105.0, lat - 35.0)
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    wgslng = lng + dlng
    wgslat = lat + dlat

    # 新加误差矫正部分
    corrent_list = wgs84_to_gcj02(wgslng, wgslat)
    clng = corrent_list[0]-lng
    clat = corrent_list[1]-lat
    dis = math.sqrt(clng*clng + clat*clat)

    while dis > interval:
        clng = clng/2
        clat = clat/2
        wgslng = wgslng - clng
        wgslat = wgslat - clat
        corrent_list = wgs84_to_gcj02(wgslng, wgslat)
        cclng = corrent_list[0] - lng
        cclat = corrent_list[1] - lat
        dis = math.sqrt(cclng*cclng + cclat*cclat)
        clng = clng if math.fabs(clng) > math.fabs(cclng) else cclng
        clat = clat if math.fabs(clat) > math.fabs(cclat) else cclat

    return [wgslng, wgslat]
