import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def read_paired_data(file_path):
    """Read paired email and SteamKey data from a CSV file."""
    paired_data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) == 2:  # Ensure we have both email and SteamKey
                paired_data.append((row[0].strip(), row[1].strip()))
    return paired_data

def read_completed_emails(file_path):
    """Read already sent emails from a text file."""
    if not os.path.exists(file_path):
        return set()  # Return an empty set if the file doesn't exist

    with open(file_path, 'r', encoding='utf-8') as f:
        return {line.strip() for line in f if line.strip()}

def send_email(to_email, steam_key, smtp_settings):
    """Send an email with the SteamKey."""
    msg = MIMEMultipart()
    msg['From'] = smtp_settings['from_email']
    msg['To'] = to_email
    msg['Subject'] = "Your Steam Key"

    body = f"Hello!\n\nYou are receiving this email because you met the requirements for a Retail GearGrit key on Patreon.\n\nHere is your Steam Key: {steam_key}\n\nThank you!\n\nLove, Pandan"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_settings['smtp_server'], smtp_settings['smtp_port']) as server:
            server.starttls()
            server.login(smtp_settings['from_email'], smtp_settings['email_password'])
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except smtplib.SMTPRecipientsRefused as e:
        print(f"Failed to send email to {to_email}: {e}")
    except Exception as e:
        print(f"An error occurred while sending email to {to_email}: {e}")

def read_password(file_path):
    """Read the email password from a secret text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()  # Remove any surrounding whitespace

def main():
    paired_data_file = 'paired_data.csv'  # Input CSV file path
    completed_emails_file = 'Completed Emails.txt'  # File to track sent emails
    secret_file = 'emailpassword_secret.txt'  # File containing the email password

    # Read the email password from the secret file
    email_password = read_password(secret_file)

    # SMTP configuration (update with your settings)
    smtp_settings = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'from_email': 'GearGritGame@gmail.com',  # Replace with your email
        'email_password': email_password  # Replace with your email password or app password
    }

    paired_data = read_paired_data(paired_data_file)
    completed_emails = read_completed_emails(completed_emails_file)

    for email, steam_key in paired_data:
        if email and email not in completed_emails:
            send_email(email, steam_key, smtp_settings)
            completed_emails.add(email)  # Add to the set of completed emails

    # Write completed emails back to the file, removing any empty lines
    with open(completed_emails_file, 'w', encoding='utf-8') as f:
        for email in sorted(completed_emails):  # Optional: Sort emails
            if email.strip():  # Ensure no empty lines
                f.write(email + '\n')  # Write valid emails

if __name__ == "__main__":
    main()
