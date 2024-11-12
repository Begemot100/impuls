from datetime import datetime
import requests
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from config import Config
from models import db, migrate
from models.employee import Employee
from models.procedure import Procedure
from models.booking import Booking
import logging


API_KEY = '35fdd66e-7f4e-4281-81ae-2a0411344a9e'
BASE_URL = 'https://fotona.crmexpert.md'


def populate_procedures():
    procedures = [
        {"id": 1, "name": "Aclaración del tatuaje", "duration": "30 min", "category": "SW"},
        {"id": 2, "name": "Aclaración del tatuaje/micropigmentación (cejas)", "duration": "20 min", "category": "SW"},
        {"id": 3, "name": "Aclaración del tatuaje/micropigmentación (labios)", "duration": "20 min", "category": "SP"},
        {"id": 4, "name": "Onicomicosis (hongos de las uñas)", "duration": "60 min", "category": "SR"},
        {"id": 5, "name": "Eliminacion de arañas vasculares (piernas)", "duration": "30 min", "category": "SW"},
        {"id": 6, "name": "Aclaramiento de la pigmentación (corporal)", "duration": "20 min", "category": "SW"},
        {"id": 7, "name": "Consulta", "duration": "50 min", "category": "SW"},
        {"id": 8, "name": "Rejuvenecimiento FracTat", "duration": "30 min", "category": "SW"},
        {"id": 9, "name": "Aclaramiento de la pigmentación (manos)", "duration": "20 min", "category": "SW"},
        {"id": 10, "name": "Tratamiento de acné activo (corporal)", "duration": "30 min", "category": "SW"},
        {"id": 11, "name": "Control", "duration": "15 min", "category": "SW"},
        {"id": 12, "name": "Aclaramiento de la pigmentación (ingles)", "duration": "30 min", "category": "SW"},
        {"id": 13, "name": "Beauty Pack", "duration": "40 min", "category": "SW"},
        {"id": 14, "name": "Limpieza facial (manual)", "duration": "1 h", "category": "SW"},
        {"id": 15, "name": "Rejuvenecimiento 4D de Fotona", "duration": "90 min", "category": "SP"},
        {"id": 16, "name": "Rejuvenecimiento 4D de Fotona (sin peeling)", "duration": "80 min", "category": "SP"},
        {"id": 17, "name": "Rejuvenecimiento de la zona periocular (Smooth Eye)", "duration": "60 min", "category": "SP"},
        {"id": 18, "name": "Tratamiento del ronquido (NightLase)", "duration": "30 min", "category": "SP"},
        {"id": 19, "name": "Consulta Tatuaje", "duration": "20 min", "category": "SP"},
        {"id": 20, "name": "Tratamiento de Rosacea/Cuperosis", "duration": "30 min", "category": "SP"},
        {"id": 21, "name": "Eliminación de Arañas vasculares (facial)", "duration": "30 min", "category": "SP"},
        {"id": 22, "name": "Reinición de puntos Rubí", "duration": "20 min", "category": "SP"},
        {"id": 23, "name": "Tratamiento de las secuelas de acné (láser StarWalker)", "duration": "50 min", "category": "SP"},
        {"id": 24, "name": "Peeling con láser (Fotona 2D)", "duration": "30 min", "category": "SP"},
        {"id": 25, "name": "Rejuvenecimiento de labios (Lip Lase)", "duration": "30 min", "category": "SP"},
        {"id": 26, "name": "BlackPeel (peeling de carbón con láser)", "duration": "30 min", "category": "SP"},
        {"id": 27, "name": "Rejuvenecimiento StarWalker", "duration": "30 min", "category": "SW"},
        {"id": 28, "name": "Tratamiento de cicatrices", "duration": "60 min", "category": "SW"},
        {"id": 29, "name": "Tratamiento de estrias", "duration": "40 min", "category": "SW"},
        {"id": 30, "name": "Aclaramiento de la pigmentación (manos+antebrazos)", "duration": "40 min", "category": "SW"},
        {"id": 31, "name": "Tratamiento de Melasma", "duration": "40 min", "category": "SW"},
        {"id": 32, "name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (abdomen)", "duration": "180 min", "category": "SP"},
        {"id": 33, "name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (gluteos)", "duration": "180 min", "category": "SP"},
        {"id": 34, "name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (brazos)", "duration": "150 min", "category": "SP"},
        {"id": 35, "name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (papada)", "duration": "90 min", "category": "SP"},
        {"id": 36, "name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (flancos)", "duration": "180 min", "category": "SP"},
        {"id": 37, "name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (muslos)", "duration": "180 min", "category": "SP"},
        {"id": 38, "name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (rodillas)", "duration": "120 min", "category": "SP"},
        {"id": 39, "name": "Aclaración de acné activo", "duration": "60 min", "category": "SW"},
        {"id": 40, "name": "Aclaración de la pigmentación facial", "duration": "40 min", "category": "SW"},
        {"id": 41, "name": "Tratamiento de cicatrices hiperpigmentadas", "duration": "30 min", "category": "SP"},
        {"id": 42, "name": "Dermapen", "duration": "30 min", "category": "SW"},
    ]

    for procedure in procedures:
        existing_procedure = Procedure.query.get(procedure["id"])
        if not existing_procedure:
            new_procedure = Procedure(
                id=procedure["id"],
                name=procedure["name"],
                duration=procedure["duration"],
                category=procedure["category"]
            )
            db.session.add(new_procedure)
    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    @app.route("/employees")
    def employees():
        employees = Employee.query.all()
        return render_template("employees.html", employees=employees)

    @app.route("/procedures", methods=["GET"])
    def procedures():
        procedures = Procedure.query.all()
        return render_template("procedures.html", procedures=procedures)

    @app.route("/get_employee_procedures/<int:employee_id>", methods=["GET"])
    def get_employee_procedures(employee_id):
        employee = Employee.query.get(employee_id)
        if employee:
            procedure_ids = [procedure.id for procedure in employee.procedures]
            return jsonify({"procedures": procedure_ids})
        return jsonify({"error": "Сотрудник не найден"}), 404

    @app.route("/save_procedures/<int:employee_id>", methods=["POST"])
    def save_procedures(employee_id):
        data = request.get_json()
        procedure_ids = data.get("procedures", [])

        try:
            employee = Employee.query.get(employee_id)
            if employee:
                selected_procedures = Procedure.query.filter(Procedure.id.in_(procedure_ids)).all()
                employee.procedures = selected_procedures
                db.session.commit()
                return jsonify({"success": True, "message": "Процедуры успешно сохранены."})
            else:
                return jsonify({"success": False, "message": "Сотрудник не найден."}), 404
        except Exception as e:
            print(f"Ошибка при сохранении процедур: {e}")
            return jsonify({"success": False, "message": "Ошибка при сохранении процедур."}), 500

    @app.route("/")
    def home():
        return redirect(url_for("index"))

    @app.route('/index')
    def index():
        employees = Employee.query.all()
        procedures = Procedure.query.all()
        return render_template('index.html', employees=employees, procedures=procedures)

    def get_bookings_from_api(master_id, date):
        api_url = f"{BASE_URL}/order_calendar/master_orders"
        params = {
            "api_key": API_KEY,
            "master_id": master_id,
            "date": date
        }
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            return response.json() if response.text.strip() else []
        except requests.RequestException as e:
            print("Ошибка при запросе к API:", e)
            return []

    @app.route("/bookings")
    def bookings():
        date = request.args.get("date", "")
        master_id = request.args.get("master_id", "")
        masters = Employee.query.all()
        bookings = []

        if master_id:
            bookings = get_bookings_from_api(master_id, date)
        else:
            for master in masters:
                master_bookings = get_bookings_from_api(master.id, date)
                bookings.extend(master_bookings)

        formatted_bookings = []
        for booking in bookings:
            title = booking.get("title", "Не указано")
            start = booking.get("start")
            end = booking.get("end")
            start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            duration = end_time - start_time
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = remainder // 60
            duration_str = f"{hours} ч {minutes} мин" if hours > 0 else f"{minutes} мин"
            items = booking.get("items", "Нет данных")
            service = ", ".join(f"{key}: {value}" for key, value in items.items()) if isinstance(items, dict) else items

            formatted_bookings.append({
                "title": title,
                "service": service,
                "start": start,
                "end": end,
                "duration": duration_str
            })

        return render_template("bookings.html", bookings=formatted_bookings, date=date, masters=masters, master_id=master_id)

    AVAILABLE_SLOTS = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"]

    def get_busy_slots(master_id, date):
        api_url = f"{BASE_URL}/order_calendar/master_orders"
        params = {
            "api_key": API_KEY,
            "master_id": master_id,
            "date": date
        }
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            bookings = response.json()
            return [booking['start'][11:16] for booking in bookings]
        except requests.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []

    @app.route('/get_slots')
    def get_slots():
        master_id = request.args.get('master_id')
        date = request.args.get('date')
        busy_slots = get_busy_slots(master_id, date)
        free_slots = [slot for slot in AVAILABLE_SLOTS if slot not in busy_slots]
        return jsonify({"slots": free_slots})

    @app.route("/book", methods=["GET", "POST"])
    def book():
        procedures = Procedure.query.all()
        doctors = Employee.query.all()
        return render_template("book.html", procedures=procedures, doctors=doctors)

    @app.route("/create_booking", methods=["POST"])
    def create_booking():
        data = request.get_json()
        client_name = data.get("client_name")
        procedure_id = data.get("procedure_id")
        employee_id = data.get("doctor_id")
        datetime_str = data.get("datetime")

        try:
            booking_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            new_booking = Booking(
                client_name=client_name,
                procedure_id=procedure_id,
                employee_id=employee_id,
                booking_date=booking_datetime.date(),
                booking_time=booking_datetime.time()
            )
            db.session.add(new_booking)
            db.session.commit()
            return jsonify({"success": True, "message": "Запись успешно создана."})
        except Exception as e:
            print("Ошибка при создании записи:", e)
            return jsonify({"success": False, "message": "Ошибка при создании записи."}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(port=5005)