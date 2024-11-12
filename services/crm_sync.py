import requests

API_URL = "https://fotona.crmexpert.md/order_calendar/master_orders"

def get_master_orders(api_key, master_id, date):
    params = {
        "api_key": api_key,
        "master_id": master_id,
        "date": date
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Ошибка при получении данных из CRM:", response.status_code)
        return None
