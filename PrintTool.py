import datetime

file_path = 'D://date.txt'

def read_dates_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        dates = file.readlines()
    return [date.strip() for date in dates]

def find_missing_dates(dates):
    date_objects = [datetime.datetime.strptime(date, '%Y%m%d').date() for date in dates]
    min_date = min(date_objects)
    max_date = max(date_objects)
    
    year_start = datetime.date(min_date.year, 1, 1)
    year_end = datetime.date(max_date.year, 12, 31)
    all_dates = {year_start + datetime.timedelta(days=x) for x in range((year_end - year_start).days + 1)}
    
    read_dates = set(date_objects)
    missing_dates = all_dates - read_dates
    
    return sorted(list(missing_dates))

def main():
    dates = read_dates_from_file(file_path)
    missing_dates = find_missing_dates(dates)
    print("Missing dates:")
    for date in missing_dates:
        print(date.strftime('%Y%m%d'))

if __name__ == "__main__":
    main()
