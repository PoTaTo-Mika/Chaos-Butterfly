from datetime import datetime, timedelta
import re  # ����������ʽģ��

file_path = "D://filelist.txt"

def generate_date_list(start_date, end_date):
    # ���ɴ� start_date �� end_date ֮��������б�
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

def extract_date_from_filename(filename):
    # ʹ��������ʽ���ļ�������ȡ����ʱ���ַ���
    match = re.search(r'hycom_GLBv0.08_539_[^\d]*(\d{8})', filename)
    if match:
        # ��ʹ�����ڲ��ֽ���ת��
        try:
            return datetime.strptime(match.group(1), '%Y%m%d')
        except ValueError as e:
            print(f"Error parsing date from {filename}: {e}")
    return None

def check_files(file_paths, start_date, end_date):
    # ���������������б�
    dates_needed = set(generate_date_list(start_date, end_date))
    # ��ʼ��һ������������ҵ�������
    dates_found = set()
    # ��ʼ��һ���б������������ȡ��������
    all_extracted_dates = []

    for file_path in file_paths:
        date = extract_date_from_filename(file_path)
        if date:
            dates_found.add(date.date())
            all_extracted_dates.append(date.date())  # ��ӵ��б���

    # ��ӡ������ȡ��������
    if all_extracted_dates:
        print("All extracted dates:")
        for extracted_date in sorted(all_extracted_dates):
            print(extracted_date.strftime("%Y%m%d"))

# ��ȡ�ļ����б�
with open(file_path, 'r') as file:
    file_paths = [path.strip() for path in file.readlines()]

# ���������ռ�����ʼ�ͽ�������
start_date = datetime(2015, 1, 1)
end_date = datetime(2015, 12, 31)

# ִ�м��
check_files(file_paths, start_date, end_date)
