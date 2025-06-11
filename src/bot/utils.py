import re


def is_valid_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    """
    return re.fullmatch(r"\+?[1-9]\d{9,14}$", phone) is not None
