from datetime import datetime


def ask_date() -> str:
    """Return current date response

    Returns:
        str: _description_
    """
    today = datetime.today().strftime("%d/%m/%Y")
    return f"Hôm nay là ngày {today}"

def ask_hour() -> str:
    """Return current time response

    Returns:
        str: _description_
    """
    current = datetime.now()

    return f"Hiện tại là {current.hour}:{current.minute}:{current.second}"

INTENT_HANDLER = {'ask_date': ask_date, 'ask_hour': ask_hour}
