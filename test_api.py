from datetime import datetime
from services.crm_sync import get_master_orders

# Список исполнителей с ID
executors = {
    3079: "Martsyniak Daria",
    2963: "Viacheslav BCN",
    3067: "Ekaterina Kuznetsova TRG",
    1532: "Katerina (médico) BCN",
    2702: "Katerina Tarragona",
    2962: "Ushakov Viacheslav TRG",
    3084: "Yulia Estetica"
}

# Текущая дата
date = "2024-11-04"  # Установите желаемую дату

# Получение заказов для каждого исполнителя
for master_id, name in executors.items():
    try:
        orders = get_master_orders(master_id, date)
        if orders:
            print(f"Заказы для {name} на {date}: {orders}")
        else:
            print(f"Заказов для {name} на {date} нет или доступ к ним ограничен.")
    except Exception as e:
        print(f"Ошибка при получении заказов для {name}: {e}")
