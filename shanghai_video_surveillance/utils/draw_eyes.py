import warnings
warnings.filterwarnings("ignore")

# 可视化库
import folium
from folium.features import GeoJson,GeoJsonPopup,GeoJsonTooltip
from folium.plugins import MiniMap
from folium.plugins import Geocoder

from utils.style_function import style_function

def draw_eyes(m, gdf):
    circleMarker = folium.CircleMarker(radius=5,
                                       fill_color="orange",
                                       fill_opacity=1,
                                       color="black",
                                       weight=1)
    gjson = GeoJson(data=gdf,
                    style_function=style_function,
                    marker=circleMarker,
                    name="electronic_eyes",
                    ).add_to(m)
    Geocoder(collapsed=True).add_to(m)

    # 添加单击显示
    GeoJsonPopup(fields=['position', 'Vio_index', 'district', 'WGS_lon', 'WGS_lat', 'href'], labels=True).add_to(gjson)

    # 添加鼠标移动显示
    GeoJsonTooltip(fields=['position', 'Vio_index', 'district', 'WGS_lon', 'WGS_lat', 'href'], labels=True).add_to(
        gjson)

    # 添加索引图
    minimap = MiniMap(toggle_display=True)
    m.add_child(minimap)

    # 添加图层切换控件
    folium.LayerControl().add_to(m)