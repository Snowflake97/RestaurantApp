import datetime

def str_to_time_conversion(time):
    parts = time.split(":")
    converted_time = datetime.time(int(parts[0]), int(parts[1]))
    return converted_time

def create_date():
    year = input("Wprowadz rok: ")
    month = input("Wprowadz miesiac(1-12): ")
    day = input("Wprowadz dzien: ")

    return f"{year}-{month}-{day}"

def create_hour():
    hour = input("Wprowadz godzine: ")
    time = datetime.time(int(hour), 0)
    return time
