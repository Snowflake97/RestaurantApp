import datetime

def str_to_time_conversion(time):
    parts = time.split(":")
    converted_time = datetime.time(int(parts[0]), int(parts[1]))
    return converted_time