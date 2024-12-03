import os
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from transformers import pipeline

# Directory and file paths
DATA_DIR = "data"
TICKETS_FILE = os.path.join(DATA_DIR, "issue_tickets.csv")

# Ensure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Load and Save Functions
def load_issue_tickets():
    valid_tickets = []
    if os.path.exists(TICKETS_FILE) and os.path.getsize(TICKETS_FILE) > 0:
        all_tickets = pd.read_csv(TICKETS_FILE).to_dict(orient="records")
        for ticket in all_tickets:
            try:
                if isinstance(ticket["date"], str):
                    # Check if the date is ISO 8601 formatted
                    datetime.datetime.fromisoformat(ticket["date"])
                else:
                    continue  # Skip invalid rows

                if isinstance(ticket["name"], str):
                    valid_tickets.append(ticket)
            except (ValueError, KeyError):
                continue  # Skip invalid rows
    return valid_tickets

def save_issue_ticket(issue_data):
    if isinstance(issue_data, list):
        pd.DataFrame(issue_data).to_csv(TICKETS_FILE, index=False)
    elif isinstance(issue_data, dict):
        issue_data["geo_location"] = str(issue_data.get("geo_location", {}))  # Serialize geo_location
        df = pd.DataFrame([issue_data])
        df.to_csv(TICKETS_FILE, mode="a", header=not os.path.exists(TICKETS_FILE), index=False)
    else:
        raise ValueError("Invalid issue_data format. Expected dict or list.")

# AI Models
def classify_waste(image):
    if image is None:
        return "Unknown"
    try:
        classifier = pipeline("image-classification", model="microsoft/resnet-50")
        predictions = classifier(image)
        return predictions[0]["label"]
    except Exception as e:
        print(f"Error in waste classification: {e}")
        return "Error in Classification"

def classify_issue(description):
    try:
        nlp_classifier = pipeline("text-classification", model="distilbert-base-uncased")
        prediction = nlp_classifier(description)
        return prediction[0]["label"]
    except Exception as e:
        print(f"Error in issue classification: {e}")
        return "Error in Classification"

# Email Function
def send_email_to_citizen(citizen_email, subject, body):
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = citizen_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, citizen_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
