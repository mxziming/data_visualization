import warnings
warnings.filterwarnings("ignore")

# 可视化库
import folium

from folium.plugins import MiniMap
from folium.plugins import MarkerCluster

def draw_cluster(m, gdf):
    # 创建map，添加比例尺控件

    marker_cluster = MarkerCluster().add_to(m)
    # 添加聚类点
    for i in range(len(gdf)):
        temp = gdf.loc[i]
        label = '位置：' + temp['position'] + '\n' + "违章指数：" + str(temp['Vio_index']) + '\n' + "超链接" + temp['href']
        folium.Marker(
            location=[temp['WGS_lat'], temp['WGS_lon']],
            icon=folium.Icon(color='blue', icon='glyphicon-eye-open'),
            popup=label,
        ).add_to(marker_cluster)

    # 将聚类对象添加到地图
    m.add_child(marker_cluster)
    # 添加索引图
    minimap = MiniMap(toggle_display=True)
    m.add_child(minimap)