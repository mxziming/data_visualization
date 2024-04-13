import math
from utils._transformlat import _transformlat
from utils._transformlng import _transformlng
from utils.out_of_china import out_of_china

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

def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
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
    gclng = lng + dlng
    gclat = lat + dlat

    return [gclng, gclat]