from models.employee import Employee  
from models import db  
from app import create_app

employees_data = [
    {"id": 3079, "name": "Martsyniak Daria"},
    {"id": 2963, "name": "Viacheslav BCN"},
    {"id": 3067, "name": "Ekaterina Kuznetsova TRG"},
    {"id": 1532, "name": "Katerina (médico) BCN"},
    {"id": 2702, "name": "Katerina Tarragona"},
    {"id": 2962, "name": "Ushakov Viacheslav TRG"},
    {"id": 3084, "name": "Yulia Estetica"}
]

app = create_app()

with app.app_context():
    for employee_data in employees_data:
        employee = Employee(id=employee_data["id"], name=employee_data["name"])
        db.session.add(employee)
    db.session.commit()
    print("Сотрудники успешно добавлены!")
