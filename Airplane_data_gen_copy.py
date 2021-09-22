import csv
import time
from datetime import datetime
import pandas as pd

fieldnames = ["Time", "s1", "s2", "s3"]
df = pd.read_csv('PredictiveManteinanceEngineTraining.csv', usecols=[6, 7, 8])
df.columns = ['s1', 's2', 's3']
with open('airplane_data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
i = 1
sensor_1 = df.iloc[i].values[0]
sensor_2 = df.iloc[i].values[1] + 0.4
while True:
    with open('airplane_data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        now = datetime.now().strftime('%m/%d/%Y,%H:%M:%S')
        s1 = sensor_1
        if i // 11 == 0:
            print("hi")
            i = i + 1
            s2 = s1 + 1
        else:
            i = i + 1
            s2 = s1
        s3 = sensor_1
        info = {
            "Time": now,
            "s1": s1,
            "s2": s2,
            "s3": s3
        }

        csv_writer.writerow(info)
        sensor_1 = df.iloc[i].values[0]
        sensor_2 = df.iloc[i].values[1] + 0.4
        print(now, s1, s2, s3, i)
        time.sleep(1)
