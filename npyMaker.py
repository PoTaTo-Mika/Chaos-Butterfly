import xarray as xr
import numpy as np
import os
import glob

# ����.nc�ļ����ڵ��ļ���·��
nc_files_path = r"D:\Chaos;Butterfly\Data\input\Ocean"

# ��ȡ��������
topography_data_path =  r'D:\Chaos;Butterfly\Data\default_data\topography.nc'
land_mask = xr.open_dataset(topography_data_path, decode_times=False)
land_hgt = land_mask['HGT']  # ���θ߶�����

# �����µľ�γ�������Զ���SSH��������ݵķֱ���
lon_new = np.linspace(-180, 180, 1440)
lat_new = np.linspace(-90, 90, 721)

# �Ե������ݽ��в�ֵ����ƥ���µľ�γ�ȷֱ���
land_hgt_aligned = land_hgt.interp(lon=lon_new, lat=lat_new)

# ��ȡ����.nc�ļ���·��
nc_files = glob.glob(os.path.join(nc_files_path, '*.nc'))

# ����ÿ��.nc�ļ�
for nc_file in nc_files:
    # ��ȡ����SSH����
    ssh_data = xr.open_dataset(nc_file, decode_times=False)
    surf_el = ssh_data['surf_el']  # SSH����

    # ��SSH���ݽ��в�ֵ����ƥ���µľ�γ�ȷֱ���
    surf_el_aligned = surf_el.interp(lon=lon_new, lat=lat_new)

    # ʹ�õ��������SSH�����е�ȱʡֵ
    surf_el_filled = np.where(np.isnan(surf_el_aligned.values), land_hgt_aligned.values, surf_el_aligned.values)

    # ��������ļ�������.nc�滻Ϊ.npy��
    output_file_name = os.path.basename(nc_file).replace('.nc', '.npy')
    output_file_path = os.path.join("D:\Chaos;Butterfly\Data\output", output_file_name)

    # ���洦����������Ϊ.npy�ļ�
    np.save(output_file_path, surf_el_filled)

    print(f"Processed and filled, then saved: {output_file_path}")

print("All files have been processed.")
