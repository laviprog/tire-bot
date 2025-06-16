from datetime import datetime


def validate_datetime(date_str: str) -> datetime | None:
    """
    Validates a date string and returns a datetime object.
    :param date_str: The date string to validate.
    :return: datetime object if valid, None otherwise.
    :raises ValueError: If the date string is not in the expected format.
    """
    try:
        return datetime.strptime(date_str, "%d.%m.%Y %H:%M")
    except ValueError:
        return datetime.strptime(date_str, "%d.%m.%Y")
