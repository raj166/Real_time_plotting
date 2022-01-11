import csv
import time
from datetime import datetime
import pandas as pd

fieldnames = ["Time", "s1", "s2", "s3"]
df = pd.read_csv('combined_csv.csv')
df.columns = ['s1', 's2', 's3']

with open('Data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
i = 0
sensor_1 = df.iloc[i].values[0]
sensor_2 = df.iloc[i].values[1]
sensor_3 = df.iloc[i].values[2]
while True:
    with open('Data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        now = datetime.now().strftime('%m/%d/%Y,%H:%M:%S')
        s1 = sensor_1
        s2 = sensor_2
        s3 = sensor_3
        info = {
            "Time": now,
            "s1": s1,
            "s2": s2,
            "s3": s3
        }

        csv_writer.writerow(info)
        i = i + 1
        sensor_1 = df.iloc[i].values[0]
        sensor_2 = df.iloc[i].values[1]
        sensor_3 = df.iloc[i].values[2]
        print(now, s1, s2, s3, i)
        time.sleep(1)
