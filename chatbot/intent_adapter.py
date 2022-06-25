from datetime import datetime

from . import service


def ask_date(statement=None) -> str:
    """Return current date response

    Returns:
        str: _description_
    """
    today = datetime.today().strftime("%d/%m/%Y")
    return f"Hôm nay là ngày {today}"

def ask_hour(statement=None) -> str:
    """Return current time response

    Returns:
        str: _description_
    """
    current = datetime.now()

    return f"Hiện tại là {current.hour}:{current.minute}:{current.second}"

def ask_weather(statement=None) -> str:
    weather_data =  service.get_current_weather("Ho Chi Minh weather")
    return f"Thời tiết hiện tại vào {weather_data[0]}, có nhiệt độ {weather_data[1]}°C, trời {weather_data[2]}"

def search_google(statement=None) -> str:
    search_text = statement.in_response_to.replace("Tìm google giúp", "")
    pass


INTENT_HANDLER = {'ask_date': ask_date, 'ask_hour': ask_hour, 'ask_weather': ask_weather}
