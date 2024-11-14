import csv
from collections import defaultdict

# Function to load protocol mapping from a CSV file
def load_protocol_mapping(protocol_file):
    protocol_mapping = {}
    with open(protocol_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            decimal = int(row['Decimal'])
            keyword = row['Keyword'].lower()
            protocol_mapping[decimal] = keyword
    return protocol_mapping

# Function to load the lookup table from an Excel-like CSV file into a dictionary
def load_lookup_table(lookup_file):
    lookup_table = {}
    with open(lookup_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            dstport = int(row['dstport'])
            protocol = row['protocol'].lower()
            tag = row['tag']
            lookup_table[(dstport, protocol)] = tag
    return lookup_table

# Function to parse flow logs and count matches
def parse_flow_logs(log_file, lookup_table, protocol_mapping):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0

    with open(log_file, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) < 10:
                continue  # Skip malformed lines

            dstport = int(parts[5])
            protocol_num = int(parts[6])
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
    protocol_file = 'protocol-numbers-1.csv'  # Path to protocol mapping CSV file
    lookup_file = 'lookup_table.csv'          # Path to lookup table CSV file
    log_file = 'lookup_logs.txt'              # Path to flow log file

    protocol_mapping = load_protocol_mapping(protocol_file)  # Load protocol mappings
    lookup_table = load_lookup_table(lookup_file)            # Load lookup table

    tag_counts, port_protocol_counts = parse_flow_logs(log_file, lookup_table, protocol_mapping)
    write_output(tag_counts, port_protocol_counts)

if __name__ == "__main__":
    main()