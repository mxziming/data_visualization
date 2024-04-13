# 设置分级显示策略
def style_function(feature):
    style = {}
    level = feature["properties"]["Vio_index"]
    if level < 100:
        style = {"radius": 2, 'fillColor': "green", 'fill_opacity': '0.6'}
    elif level < 500:
        style = {"radius": 3, 'fillColor': "yellow", 'fill_opacity': '0.6'}
    else:
        style = {"radius": 4, 'fillColor': "red", 'fill_opacity': '0.6'}

    return style