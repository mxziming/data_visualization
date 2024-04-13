import pandas as pd
import geopandas as gpd

data = pd.read_csv('../data/video_surveillance_with_geo_data.csv', index_col=0)

# 提取WGS84坐标
data['WGS_coordinate'] = data['WGS_coordinate'].\
    replace("'", '', regex=True).\
    replace('\[', '', regex=True).\
    replace('\]', '', regex=True).\
    replace('\(', '', regex=True).\
    replace('\)', '', regex=True).\
    replace(' ', '', regex=True).\
    str.split(",")

data['WGS_lon'] = [i[0] for i in data['WGS_coordinate']]
data['WGS_lat'] = [i[1] for i in data['WGS_coordinate']]

# 仅保留有用信息，生成dataframe
df = data[['位置', '违章指数', '超链接', 'WGS_lon', 'WGS_lat']]

# 根据经纬度生成点的几何对象，并指定坐标系
geometry = gpd.points_from_xy(data['WGS_lon'], data['WGS_lat'], crs=4326)

# 初始化geodataframe
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# 导出为shp
gdf.to_file('data/video_surveillance.shp', encoding='gbk', crs=4326)