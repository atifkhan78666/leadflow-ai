import requests
import re
from bs4 import BeautifulSoup


EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

def find_emails(text):
    return re.findall(EMAIL_REGEX, text)

def extract_email(base_url):
    pages_to_check = [
        base_url,
        base_url + "/contact",
        base_url + "/contact-us",
        base_url + "/about",
        base_url + "/about-us"
    ]

    emails_found = set()

    for url in pages_to_check:

        try:
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                continue
            html = response.text
            emails = find_emails(html)
            for email in emails:
                emails_found.add(email)

        except:
            continue

    if emails_found:
        return list(emails_found)[0]

    return None