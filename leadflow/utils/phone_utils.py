import re
import phonenumbers
from phonenumbers import PhoneNumberFormat

def clean_phone_number(phone, default_region=None):
    """
    Normalize phone numbers to E.164 format: +<countrycode><number>
    default_region examples: 'IN', 'AE', 'US', 'GB'
    """

    if not phone:
        return None

    try:
        # Remove obvious noise
        phone = re.sub(r"[^\d+]", "", phone)

        parsed = phonenumbers.parse(phone, default_region)

        if not phonenumbers.is_valid_number(parsed):
            return None

        return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)

    except:
        return None