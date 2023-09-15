import os
import time

def get_last_modified_timestamp(file_path):
    try:
        return os.path.getmtime(file_path)
    except FileNotFoundError:
        return None

def display_new_content(file_path, last_timestamp):
    current_timestamp = get_last_modified_timestamp(file_path)
    if current_timestamp and current_timestamp != last_timestamp:
        with open(file_path, 'r') as file:
            new_content = file.readlines()
            for line in new_content:
                print(line.strip())
        return current_timestamp
    return last_timestamp

if __name__ == "__main__":
    file_path = "/home/pi/sim900/report.txt"
    last_timestamp = None

    try:
        while True:
            last_timestamp = display_new_content(file_path, last_timestamp)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

