import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature

stations = pd.read_csv("data//stations.csv")[["code", "lat", "lon"]]

crs = ccrs.AlbersEqualArea(central_longitude=-155, standard_parallels=(51, 60))
ax = plt.axes(projection=crs)
ax.coastlines(resolution='10m')
ax.add_feature(cfeature.OCEAN.with_scale('50m'))
ax.add_feature(cfeature.LAND.with_scale('50m'), edgecolor='black')
ax.gridlines(linestyle='--', color='black')
x_list = stations["lon"].values.tolist()
y_list = stations["lat"].values.tolist()
code = stations["code"].values.tolist()
data_crs = ccrs.PlateCarree()
plt.plot(x_list, y_list, "^", color="seagreen", markersize=5, transform=data_crs)  # 绘制点
plt.legend(labels=['stations'])
# 添加点的标注
ax.set_extent((-164, -146, 51, 60), ccrs.PlateCarree())
plt.savefig('station_location.png')

tiled_labels = np.load("tiled_labels.npy")
results_ref = np.load("results_ref.npy")