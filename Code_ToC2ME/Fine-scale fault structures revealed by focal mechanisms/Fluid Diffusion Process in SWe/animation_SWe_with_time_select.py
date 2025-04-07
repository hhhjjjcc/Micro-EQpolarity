import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime
import numpy as np
from obspy.imaging.beachball import beach

# -------------------------------
# 解析时间戳，兼容有无小数点的情况
# -------------------------------
def parse_timestamp(ts):
    ts_str = str(ts).strip()  # 转换为字符串
    if '.' in ts_str:
        dt_obj = datetime.strptime(ts_str, '%Y%m%d%H%M%S.%f')
    else:
        dt_obj = datetime.strptime(ts_str, '%Y%m%d%H%M%S')
    return dt_obj.replace(microsecond=0)

# ==============================
# 读取 Excel 数据，并生成 datetime 列
# ==============================
excel_file = './ToC2ME_Extract.xlsx'
df = pd.read_excel(excel_file)

# 确保 Second 是整数，以避免时间匹配问题
df['Second'] = df['Second'].astype(int)
df['datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']])
df = df.sort_values(by='datetime')

# ==============================
# 读取文本数据，并处理震源机制信息
# ==============================
txt_file_path = './mt_solution_20250317_SKHASH_SWe_quality_A_B.txt'
df_txt = pd.read_csv(txt_file_path, sep='\t', header=None, 
                     names=['timestamp', 'lat_orig', 'lon_orig', 'depth', 'strike', 'dip', 'rake', 'flag'])

# 解析时间戳，并确保 datetime 仅保留到秒级
df_txt['timestamp'] = df_txt['timestamp'].astype(str)  # 确保为字符串
df_txt['datetime'] = df_txt['timestamp'].apply(parse_timestamp).dt.floor('S')

# 过滤 dip < 45° 的记录
df_txt_filtered = df_txt[df_txt['dip'] < 45].copy()

# ==============================
# 使用 merge_asof 进行时间匹配
# ==============================
df_match = df[['datetime', 'Latitude', 'Longitude']].sort_values('datetime')
df_merged = pd.merge_asof(df_txt_filtered.sort_values('datetime'), df_match, on='datetime', direction='nearest')

# **打印实际绘制的震源机制解记录**
print("### 实际绘制的震源机制解记录 ###")
print(df_merged)

# ==============================
# 设置输出目录和图形参数
# ==============================
output_dir = './'
blue_color = '#737FBF'

# 指定的故障时刻及对应标题
faults = [
    ('2016-11-20 19:58:31', 'Fault1 activation: 2016-11-20'),
    ('2016-11-21 22:26:46', 'Fault2 activation: 2016-11-21'),
    ('2016-11-22 05:21:40', 'Fault3 activation: 2016-11-22'),
    ('2016-11-22 19:45:47', 'Fault4 activation: 2016-11-22'),
    ('2016-11-23 06:45:35', 'Fault5 activation: 2016-11-23'),
    ('2016-11-24 04:42:07', 'Fault6 activation: 2016-11-24')
]

# ==============================
# 生成每个故障时间点的图像
# ==============================
for fault_time, title in faults:
    fault_datetime = pd.to_datetime(fault_time)
    
    # 只筛选出故障发生之前的 Excel 数据（用于绘制散点）
    current_data = df[df['datetime'] <= fault_datetime]
    
    # 震源机制球 **不按时间筛选，全部绘制**
    current_mech = df_merged  # 这里不做任何时间筛选，确保所有 dip < 45° 的机制球都显示

    # 创建 Matplotlib 图
    fig, ax = plt.subplots(figsize=(8.27, 7))
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    # 绘制背景散点（浅灰色）
    ax.scatter(df['Longitude'], df['Latitude'], s=15, c='lightgray', alpha=0.5)
    # 绘制当前故障时刻前的数据（蓝色）
    ax.scatter(current_data['Longitude'], current_data['Latitude'], s=15, c=blue_color)
    
    # --------------------------
    # 直接在 ax 中绘制 **所有** 震源机制球
    # --------------------------
    for idx, row in current_mech.iterrows():
        mech = [row['strike'], row['dip'], row['rake']]
        lon, lat = row['Longitude'], row['Latitude']
        
        # 计算震源机制球的大小（适当缩放）
        size = 0.00015  # 适当缩放到经纬度范围
        
        # 创建 beachball，并转换为 Matplotlib 的 Patch
        beachball_patch = beach(mech, xy=(lon, lat), width=size, linewidth=1, facecolor='#50AF71', edgecolor='k')
        
        # 直接将震源机制球添加到 ax 中
        ax.add_collection(beachball_patch)
    
    # 设置图标题和坐标轴
    ax.set_title(title, fontsize=20)
    ax.set_xlim(-117.230, -117.224)
    ax.set_xticks([-117.230, -117.228, -117.226, -117.224])
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    
    # 保存图片
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = f'{output_dir}{title.split(":")[0]}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
