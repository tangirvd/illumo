import pandas as pd
import csv
from collections import defaultdict

# Function to load protocol mapping from an Excel file
def load_protocol_mapping(protocol_file):
    protocol_mapping = {}
    df = pd.read_csv(protocol_file)
    for _, row in df.iterrows():
        decimal = int(row['Decimal'])
        keyword = row['Keyword'].lower()
        protocol_mapping[decimal] = keyword
    return protocol_mapping

# Function to load the lookup table from an Excel file into a dictionary
def load_lookup_table(lookup_file):
    lookup_table = {}
    df = pd.read_excel(lookup_file, sheet_name='Sheet1')
    for _, row in df.iterrows():
        dstport, protocol, tag = int(row['dstport']), row['protocol'].lower(), row['tag']
        lookup_table[(dstport, protocol)] = tag
    return lookup_table

# Function to parse flow logs and count matches
def parse_flow_logs(log_file, lookup_table, protocol_mapping):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0
    print(log_file)
    with open(log_file, 'r') as file:
        print("Success")
        for line in file:
            parts = line.split()
            if len(parts) < 10:
                continue  # Skip malformed lines

            dstport = int(parts[6])
            protocol_num = int(parts[7])
            print(dstport, protocol_num)
            protocol = protocol_mapping.get(protocol_num, "unknown")
            key = (dstport, protocol)

            # Retrieve the tag for the given port/protocol combination from the lookup table
            tag = lookup_table.get(key)

            if tag:
                tag_counts[tag] += 1
            else:
                untagged_count += 1

            # Increment port/protocol combination count
            port_protocol_counts[key] += 1

    # Convert tag counts to include 'Untagged'
    tag_counts['Untagged'] = untagged_count

    return tag_counts, port_protocol_counts

# Function to write the output files
def write_output(tag_counts, port_protocol_counts):
    # Write tag counts
    with open('tag_counts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tag", "Count"])
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])

    # Write port/protocol combination counts
    with open('port_protocol_counts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol), count in port_protocol_counts.items():
            writer.writerow([port, protocol, count])

# Main function to execute the program
def main():
    protocol_file = 'protocol-numbers-1.csv'  # Path to protocol mapping Excel file
    lookup_file = 'lookup_table.xlsx'        # Path to lookup table Excel file
    log_file = 'lookup_logs.txt'               # Path to flow log file

    protocol_mapping = load_protocol_mapping(protocol_file)  # Load protocol mappings
    lookup_table = load_lookup_table(lookup_file)            # Load lookup table

    tag_counts, port_protocol_counts = parse_flow_logs(log_file, lookup_table, protocol_mapping)
    write_output(tag_counts, port_protocol_counts)

if __name__ == "__main__":
    main()
