import xarray as xr
import numpy as np
import os
import glob

# 定义.nc文件所在的文件夹路径
nc_files_path = r"D:\Chaos;Butterfly\Data\input\Ocean"

# 读取地形数据
topography_data_path =  r'D:\Chaos;Butterfly\Data\default_data\topography.nc'
land_mask = xr.open_dataset(topography_data_path, decode_times=False)
land_hgt = land_mask['HGT']  # 地形高度数据

# 创建新的经纬度坐标以对齐SSH与地形数据的分辨率
lon_new = np.linspace(-180, 180, 1440)
lat_new = np.linspace(-90, 90, 721)

# 对地形数据进行插值，以匹配新的经纬度分辨率
land_hgt_aligned = land_hgt.interp(lon=lon_new, lat=lat_new)

# 获取所有.nc文件的路径
nc_files = glob.glob(os.path.join(nc_files_path, '*.nc'))

# 遍历每个.nc文件
for nc_file in nc_files:
    # 读取海洋SSH数据
    ssh_data = xr.open_dataset(nc_file, decode_times=False)
    surf_el = ssh_data['surf_el']  # SSH数据

    # 对SSH数据进行插值，以匹配新的经纬度分辨率
    surf_el_aligned = surf_el.interp(lon=lon_new, lat=lat_new)

    # 使用地形数据填补SSH数据中的缺省值
    surf_el_filled = np.where(np.isnan(surf_el_aligned.values), land_hgt_aligned.values, surf_el_aligned.values)

    # 构造输出文件名（将.nc替换为.npy）
    output_file_name = os.path.basename(nc_file).replace('.nc', '.npy')
    output_file_path = os.path.join("D:\Chaos;Butterfly\Data\output", output_file_name)

    # 保存处理并填补后的数据为.npy文件
    np.save(output_file_path, surf_el_filled)

    print(f"Processed and filled, then saved: {output_file_path}")

print("All files have been processed.")
