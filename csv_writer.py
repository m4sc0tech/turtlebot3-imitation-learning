import csv


def open_csv_file(path):
    """Open a CSV file for writing and return (file, writer)."""
    csv_file = open(path, 'w', newline='')
    writer = csv.writer(csv_file)

    header = ['sec', 'nanosec'] + \
        [f'range_{i}' for i in range(360)] + \
        ['linear_x', 'angular_z']
    writer.writerow(header)

    return csv_file, writer