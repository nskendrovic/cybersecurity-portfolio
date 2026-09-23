# Import necessary modules for email parsing, DNS queries, HTTP requests, regex, WHOIS lookup, and date handling
import email
from email import policy
from email.parser import BytesParser
import dns.resolver
import requests
import re
import whois
from datetime import datetime
import spf
from dateutil.relativedelta import relativedelta

# 📬 Parse the raw email and extract sender and routing headers
def parse_email(raw_email):
    # Parse the email using default policy (handles headers and encoding cleanly)
    msg = BytesParser(policy=policy.default).parsebytes(raw_email)
    # Extract the 'From' header (sender's email address)
    sender = msg['From']
    # Extract all 'Received' headers (used to trace sender IP)
    received_headers = msg.get_all('Received', [])
    return sender, received_headers

# 🔍 Check if the domain has a valid SPF record
def check_spf(domain):
    try:
        # Query DNS TXT records for the domain
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            # Look for an SPF record starting with 'v=spf1'
            if 'v=spf1' in rdata.to_text():
                return True
    except Exception:
        # If DNS query fails or no SPF found
        return False
    return False

# 🌐 Extract the sender IP address from the Received headers
def extract_ip(headers):
    # Regex pattern to match IPv4 addresses in square brackets
    ip_pattern = r'\[(\d{1,3}(?:\.\d{1,3}){3})\]'
    for h in headers:
        match = re.search(ip_pattern, h)
        if match:
            return match.group(1)
    return None

# 📅 Use WHOIS to determine domain age in days
def get_domain_age_local(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = next((d for d in creation_date if isinstance(d, datetime)), None)
        if isinstance(creation_date, str):
            try:
                creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
            except ValueError:
                creation_date = None
        if not isinstance(creation_date, datetime):
            print(f"WHOIS failed for {domain}: no valid creation date")
            return -1, "Unknown"

        creation_date = creation_date.replace(tzinfo=None)
        now = datetime.now().replace(tzinfo=None)

        delta = relativedelta(now, creation_date)
        age_days = (now - creation_date).days
        age_str = f"{delta.years} years, {delta.months} months, {delta.days} days"
        return age_days, age_str
    except Exception as e:
        print(f"Local WHOIS error for {domain}: {e}")
        return -1, "Unknown"



# 📡 Check if the domain has MX records (mail server configuration)
def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except Exception:
        return False

# 🚨 Query AbuseIPDB for sender IP reputation
def abuseipdb_check(ip):
    try:
        response = requests.get(
            f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}",
            headers={
                "Key": "YOUR_API_KEY",  # Replace with your actual AbuseIPDB API key
                "Accept": "application/json"
            }
        )
        data = response.json()
        # Extract abuse confidence score (0–100)
        return data.get('data', {}).get('abuseConfidenceScore', 0)
    except Exception:
        # Return 0 if API call fails
        return 0

# 📊 Calculate a trust score based on multiple factors
def score_sender(spf_valid, abuse_score, domain_age, mx_valid, sender, domain):
    score = 100  # Start with full trust

    # Technical signals
    if not spf_valid:
        score -= 30
    if abuse_score > 50:
        score -= 50
    elif abuse_score > 20:
        score -= 20
    if domain_age != -1:
        if domain_age < 30:
            score -= 25
        elif domain_age < 180:
            score -= 10
    if not mx_valid:
        score -= 25

    # Behavioral signals
    if is_suspicious_name(sender):
        score -= 20
    if is_suspicious_domain(domain):
        score -= 15

    # Cap score between 0 and 100
    score = max(0, min(score, 100))
    return score


# 📂 Load and analyze a local .eml email file
with open(r'C:\01. Python TEST\test3.eml', 'rb') as f:
    raw_email = f.read()

# 🧠 Detect suspicious sender display names
def is_suspicious_name(sender):
    return bool(re.search(r"(access log|#[A-Z0-9]{6,}|system alert|invoice|payment)", sender, re.IGNORECASE))

# 🌐 Detect suspicious domains or TLDs
def is_suspicious_domain(domain):
    return domain.endswith('.ru') or domain.endswith('.cn') or len(domain) > 30

# 🧪 Run analysis pipeline
sender, headers = parse_email(raw_email)
domain = sender.split('@')[-1]  # Extract domain from sender email
domain = re.sub(r"[^\w\.-]", "", domain.strip().lower())
domain_age_days, domain_age_str = get_domain_age_local(domain)
mx_valid = has_mx_record(domain)
spf_valid = check_spf(domain)
ip = extract_ip(headers)
abuse_score = abuseipdb_check(ip)
trust_score = score_sender(spf_valid, abuse_score, domain_age_days, mx_valid, sender, domain)

# 📋 Print full sender reputation report
print("📧 Email Sender Analysis Report")
print(f"Sender: {sender}")
print(f"Sender IP: {ip}")
print(f"Domain Age: {domain_age_str} ({domain_age_days} days)")
print(f"SPF Valid: {spf_valid}")
print(f"AbuseIPDB abuse confidence score: {abuse_score}")
print(f"MX Record Present: {mx_valid}")
print(f"Trust Score: {trust_score}")
print("Risk Level:", "Low" if trust_score > 80 else "Medium" if trust_score > 50 else "High")

