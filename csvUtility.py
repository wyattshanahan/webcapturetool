import csv

def process_csv(input_file, output_file):
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        with open(output_file, 'w') as output:
            for row in csv_reader:
                ip_address, dns_name = row[0].split(" ")
                dns_name = dns_name.strip("()")
                if dns_name:
                    output.write(f"{dns_name}\n")
                else:
                    output.write(f"{ip_address}\n")

# Replace 'input.csv' and 'output.csv' with your file names
# or name file as input.csv

process_csv('input.csv', 'output.csv')
