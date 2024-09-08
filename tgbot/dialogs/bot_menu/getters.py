from smsactivate.api import SMSActivateAPI
from tgbot.config import Config
from aiogram_dialog import DialogManager

async def get_services(dialog_manager: DialogManager, **kwargs):
    """
    Retrieves the list of available services from SMSActivate API.
    """
    config: Config = dialog_manager.middleware_data["config"]
    sms_activate_api_key = config.sms_activate.api_key

    # Initialize SMSActivate API client
    sa = SMSActivateAPI(sms_activate_api_key)

    # Fetch available services (default to country 0)
    country = dialog_manager.dialog_data.get("country", 0)
    status = sa.getNumbersStatus(country=country)

    # Extract services
    try:
        services = [service for service in status.keys()]
        return {"services": services}
    except Exception as e:
        print(f"Error fetching services: {e}")
        return {"services": []}

async def get_countries(dialog_manager: DialogManager, **kwargs):
    """
    Retrieves the list of available countries from SMSActivate API.
    """
    config: Config = dialog_manager.middleware_data["config"]
    sms_activate_api_key = config.sms_activate.api_key

    # Initialize SMSActivate API client
    sa = SMSActivateAPI(sms_activate_api_key)

    # Fetch available countries
    countries = sa.getCountries()

    # Extract country names
    try:
        country_list = [countries[country]["eng"] for country in countries]
        return {"countries": country_list}
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return {"countries": []}
