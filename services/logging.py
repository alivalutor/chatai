import os
from datetime import datetime


def write_log(message, log_file="no_sort.log", flag="w"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, log_file)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, flag) as file:
        # with open(log_path, "a") as file:
        file.write(f"[{timestamp}]\n {message}\n")
