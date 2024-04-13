import warnings
warnings.filterwarnings("ignore")

# 可视化库
import folium
from folium import Choropleth

# 数据分析库
import geopandas as gpd
import pandas as pd
import re

from utils.draw_eyes import draw_eyes
from utils.draw_cluster import draw_cluster

# 读入电子眼矢量
gdf_joined = gpd.read_file("../data/video_surveillance_with_district.shp", crs=4326)
gdf_joined.rename(columns={'位置': 'position', '违章指数': 'Vio_index', "超链接": "href"}, inplace=True)

# 指定坐标系
gdf_joined.crs = 4326

# 正则化匹配获取违章指数
gdf_joined['Vio_index'] = gdf_joined['Vio_index'].astype(str)
pattern = re.compile(r'\d+\.?\d*')
gdf_joined['Vio_index'] = [int(pattern.findall(i)[0]) for i in gdf_joined['Vio_index']]
gdf_joined.to_file('data/video_surveillance_model.shp', encoding='gbk', crs=4326)

# 指定地图瓦片，这里使用的是ArcGIS的街道底图
tiles = 'https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}.png'

# 初始化地图，指定地图中心位置为上海市
m1 = folium.Map(location=[31.23, 121.46], width =1000, height =750, zoom_start=9,
               control_scale=True, tiles=tiles, attr='ArcGIS街道', name='test')

# 在该地图上绘制电子眼分布散点
draw_eyes(m1, gdf_joined)

# 保存为html，通过打开html即可实现地图交互
m1.save('html/eyes.html')

# 初始化地图，指定地图中心位置为上海市
m2 = folium.Map(location=[31.23,121.46], width =1000, height =750,
               zoom_start=9, control_scale=True, tiles=tiles, attr='ArcGIS街道',
               name='test')

draw_cluster(m2, gdf_joined)

# 存储可视化地图为网页
m2.save('html/cluster.html')

# 合并分区电子眼统计结果
eys_counts = pd.DataFrame()
eys_counts['district'] = gdf_joined.district.value_counts().index
eys_counts['eys_counts'] = gdf_joined.district.value_counts().values
sh_districts = gpd.read_file('../data/shanghai.json')
sh_districts.rename(columns={'name': 'district'}, inplace=True)
eyes_districts_gdf = pd.merge(sh_districts, eys_counts)

# 初始化地图，指定地图中心位置为上海市
m3 = folium.Map(location=[31.23,121.46], width =1000, height =750,
                zoom_start=9, control_scale=True, tiles=tiles, attr='ArcGIS街道',
                name='test')

# 创建分级统计图
sh_choropleth = Choropleth(geo_data=eyes_districts_gdf,# 指定地理对象
        data=eys_counts,# 计数数据
        columns=['district','eys_counts'],# 指定颜色列表
        key_on='feature.properties.district',# geojson区域id
        bins=6,
        fill_color='YlOrRd',
        legend_name="Number of electronic monitoring",
        highlight=True).add_to(m3)

sh_choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['district', 'eys_counts'], labels=False))

# 存储可视化结果
m3.save('html/choropleth.html')