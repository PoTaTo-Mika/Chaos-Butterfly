from datetime import datetime, timedelta
import re  # 导入正则表达式模块

file_path = "D://filelist.txt"

def generate_date_list(start_date, end_date):
    # 生成从 start_date 到 end_date 之间的日期列表
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

def extract_date_from_filename(filename):
    # 使用正则表达式从文件名中提取日期时间字符串
    match = re.search(r'hycom_GLBv0.08_539_[^\d]*(\d{8})', filename)
    if match:
        # 仅使用日期部分进行转换
        try:
            return datetime.strptime(match.group(1), '%Y%m%d')
        except ValueError as e:
            print(f"Error parsing date from {filename}: {e}")
    return None

def check_files(file_paths, start_date, end_date):
    # 生成完整的日期列表
    dates_needed = set(generate_date_list(start_date, end_date))
    # 初始化一个集合来存放找到的日期
    dates_found = set()
    # 初始化一个列表来存放所有提取到的日期
    all_extracted_dates = []

    for file_path in file_paths:
        date = extract_date_from_filename(file_path)
        if date:
            dates_found.add(date.date())
            all_extracted_dates.append(date.date())  # 添加到列表中

    # 打印所有提取到的日期
    if all_extracted_dates:
        print("All extracted dates:")
        for extracted_date in sorted(all_extracted_dates):
            print(extracted_date.strftime("%Y%m%d"))

# 读取文件名列表
with open(file_path, 'r') as file:
    file_paths = [path.strip() for path in file.readlines()]

# 设置数据收集的起始和结束日期
start_date = datetime(2015, 1, 1)
end_date = datetime(2015, 12, 31)

# 执行检查
check_files(file_paths, start_date, end_date)
