import csv

def read_steam_keys(file_path):
    """Read Steam keys and their claimed emails from a text file."""
    steam_keys = {}
    with open(file_path, 'r', encoding='utf-8-sig') as f:  # Use 'utf-8-sig' to handle BOM
        for line in f:
            line = line.strip()  # Remove any leading/trailing whitespace
            if line:  # Check if line is not empty
                key_email_pair = line.split(' ', 1)
                key = key_email_pair[0]
                email = key_email_pair[1] if len(key_email_pair) > 1 else None
                steam_keys[key] = email
    return steam_keys

def read_emails_from_csv(file_path):
    """Read emails from the specified column in a CSV file, skipping the header."""
    emails = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) > 1:  # Assuming Column B is index 1
                emails.append(row[1].strip())  # Collect emails from Column B
    return emails

def pair_emails_with_steam_keys(emails, steam_keys):
    """Pair each email with a unique Steam key, skipping already claimed emails."""
    paired_data = []
    claimed_emails = {email for email in steam_keys.values() if email is not None}

    for email in emails:
        if email not in claimed_emails:  # Skip if email already has a claimed key
            for key in steam_keys:
                if steam_keys[key] is None:  # Only pair with unclaimed keys
                    paired_data.append((email, key))
                    steam_keys[key] = email  # Mark the key as claimed
                    break  # Move to the next email after claiming a key
    return paired_data

def write_paired_data_to_csv(paired_data, output_file_path):
    """Write the paired email and Steam key data to a new CSV file."""
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Email', 'SteamKey'])  # Write header
        writer.writerows(paired_data)

def write_updated_steam_keys(steam_keys, file_path):
    """Write the updated Steam keys and claimed emails back to the TXT file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for key, email in steam_keys.items():
            if email:  # Only write keys that are claimed
                f.write(f"{key} {email}\n")
            else:
                f.write(f"{key}\n")  # Unclaimed key

def main():
    csv_file_path = 'patreon.csv'  # Input CSV file path
    txt_file_path = 'steam_keys.txt'  # Input TXT file path
    output_file_path = 'paired_data.csv'  # Output CSV file path

    # Read emails and Steam keys
    emails = read_emails_from_csv(csv_file_path)
    steam_keys = read_steam_keys(txt_file_path)

    # Pair emails with Steam keys
    paired_data = pair_emails_with_steam_keys(emails, steam_keys)

    # Write the paired data to a new CSV file
    if paired_data:
        write_paired_data_to_csv(paired_data, output_file_path)
    else:
        # If no new pairs, write existing claimed pairs to CSV
        existing_pairs = [(email, key) for key, email in steam_keys.items() if email]
        write_paired_data_to_csv(existing_pairs, output_file_path)

    print(f"Paired data written to {output_file_path}")

    # Update the TXT file with claimed emails
    write_updated_steam_keys(steam_keys, txt_file_path)
    print(f"Updated keys in {txt_file_path}")

if __name__ == "__main__":
    main()
