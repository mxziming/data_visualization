import pandas as pd
import requests
import json

from utils.gcj02_to_wgs84 import gcj02_to_wgs84

pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

# 批量地理编码函数，得到高德坐标
def geocode_adresses(address_list):
    pos_list = []
    for i in range(len(address_list)):
        # 获取单个电子眼的地址
        address = address_list[i]
        # 需要大家自行替换申请到的高德APIkey，申请方法参考https://lbs.amap.com/api/webservice/guide/api/georegeo
        key = 'cdaa43b30fa82f3230eff2b3684c9b57'
        # API调用的url
        url = 'https://restapi.amap.com/v3/geocode/geo?address={}&output=location&key={}'.format(address, key)
        # 获取该API的请求结果
        res = requests.get(url)
        # 将返回的文本信息转换为python字典
        json_data = json.loads(res.text)
        status = json_data['status']
        # 对请求结果的状态进行判断，如果status为1则为请求成功
        if (status == '1'):
            # 从字典中获取位置信息
            geo = json_data['geocodes'][0]['location']
            # 分割经纬度信息，加入输出坐标列表中
            longitude = geo.split(',')[0]
            latitude = geo.split(',')[1]
        else: # 如果请求失败，则返回异常值
            longitude = -999
            latitude = -999
        pos_list.append([longitude, latitude])
    print('地理编码已完成')
    return pos_list

data = pd.read_csv('../data/video_surveillance.csv', index_col=0)

# 构建地址列表
address_list = ["上海市"+i for i in data['位置']]
# 对地址列表中的所有地址调用高德API进行批量地理编码
data['coordinate'] = geocode_adresses(address_list)

# 地理纠偏

# 提取经纬度列表
data['lon'] = data['coordinate'].map(lambda x: float(x[0]))
data['lat'] = data['coordinate'].map(lambda x: float(x[1]))
data['WGS_coordinate'] = data.apply(lambda poi: gcj02_to_wgs84(poi['lon'], poi['lat']), axis=1)

# 保存编码且校正后结果
data.to_csv('data/video_surveillance_with_geo_data.csv')

