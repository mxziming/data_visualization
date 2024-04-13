import math

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