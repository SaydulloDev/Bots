import csv
import os


def write_to_csv(file_path, header, row):
    with open(file_path, 'w', newline='\n') as f:
        csv_write = csv.DictWriter(f, header)
        if os.path.getsize(file_path) == 0:
            csv_write.writeheader()
        csv_write.writerow(row)
    print('Good Job!')
