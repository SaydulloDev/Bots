import csv


def write_dict_to_csv(data, file_path):
    with open(file_path, 'w', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(data.keys())
        writer.writerow(data.values())
