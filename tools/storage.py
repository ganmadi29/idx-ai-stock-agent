import csv
import os

FILE = "signals_log.csv"

def save_signal(data):
    exists = os.path.isfile(FILE)
    with open(FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(data)
