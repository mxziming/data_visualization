import warnings
warnings.filterwarnings("ignore")

# 数据分析库
import geopandas as gpd

gdf = gpd.read_file("../data/video_surveillance.shp", crs=4326)

# 读入上海市范围的json文件
sh_districts = gpd.read_file('../data/shanghai.json')
sh_districts.rename(columns={'name': 'district'}, inplace=True)

# 对电子眼的点gdf和上海市区划的面gdf进行空间join，how=left代表以左侧的gdf作为主表，合并区划的信息到主表中
gdf_joined = gpd.sjoin(gdf, sh_districts, how='left', op='within', lsuffix='_pt', rsuffix='_py')

gdf_joined.to_file('data/video_surveillance_with_district.shp', encoding='gbk', crs=4326)