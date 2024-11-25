import requests

# Константы API
API_URL = "https://fotona.crmexpert.md/order_calendar/master_orders"
API_KEY = "35fdd66e-7f4e-4281-81ae-2a0411344a9e"

# Параметры для тестирования
master_id = "3079"  # ID мастера
date = "2024-11-25"  # Тестовая дата

# Формирование URL
url = f"{API_URL}?api_key={API_KEY}&master_id={master_id}&date={date}"

# Отправка запроса
try:
    response = requests.get(url)

    # Проверка статуса ответа
    if response.status_code == 200:
        print("Успешный ответ от CRM:")
        print(response.json())  # Вывод данных слотов
    else:
        print(f"Ошибка: Код статуса {response.status_code}")
        print("Ответ:", response.text)
except Exception as e:
    print("Ошибка при выполнении запроса:", str(e))
