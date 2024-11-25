import requests
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import stripe
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import json
from dotenv import load_dotenv
import os




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Загрузка переменных из .env
load_dotenv()

API_URL = "https://fotona.crmexpert.md/order_calendar/master_orders"
CRM_API_KEY = os.getenv("CRM_API_KEY")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

stripe.api_key = STRIPE_SECRET_KEY
API_KEY = CRM_API_KEY

# Модель Master
class Master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Модель Procedure
class Procedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # Duration in minutes
    price = db.Column(db.Float, nullable=True)
    master_id = db.Column(db.Integer, db.ForeignKey('master.id'), nullable=True)

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    master_id = db.Column(db.String(50), nullable=False)
    procedure_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    client_name = db.Column(db.String(255), nullable=False, default="Unknown")
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


@app.route('/')
def index():
    masters = Master.query.all()
    procedures = Procedure.query.all()
    return render_template('index.html', masters=masters, procedures=procedures)

# Route для получения доступных слотов
from sqlalchemy.orm import Session

@app.route('/api/get_slots', methods=['GET'])
def get_slots():
    master_id = request.args.get('master_id')
    date = request.args.get('date')
    procedure_id = request.args.get('procedure_id')  # Получаем ID процедуры

    if not master_id or not date or not procedure_id:
        return jsonify({"error": "Master ID, date, and procedure ID are required"}), 400

    # Используем Session для получения процедуры
    session = db.session  # SQLAlchemy session
    procedure = session.get(Procedure, procedure_id)
    if not procedure:
        return jsonify({"error": "Procedure not found"}), 404

    procedure_duration = procedure.duration  # Длительность в минутах

    # Запрос к CRM
    API_URL = "https://fotona.crmexpert.md/order_calendar/master_orders"
    API_KEY = "35fdd66e-7f4e-4281-81ae-2a0411344a9e"
    url = f"{API_URL}?api_key={API_KEY}&master_id={master_id}&date={date}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            crm_data = response.json()

            # Фильтруем слоты по длительности процедуры
            available_slots = []
            for slot in crm_data:
                if "Doctor ausente" in slot.get("items", ""):
                    continue

                slot_start = datetime.strptime(slot["start"], "%Y-%m-%d %H:%M:%S")
                slot_end = datetime.strptime(slot["end"], "%Y-%m-%d %H:%M:%S")
                slot_duration = (slot_end - slot_start).total_seconds() / 60  # Длительность в минутах

                # Если длительность слота >= длительности процедуры, добавляем
                if slot_duration >= procedure_duration:
                    # Ограничиваем слот по длительности процедуры
                    adjusted_end = slot_start + timedelta(minutes=procedure_duration)
                    available_slots.append({
                        "start": slot_start.strftime("%Y-%m-%d %H:%M:%S"),
                        "end": adjusted_end.strftime("%Y-%m-%d %H:%M:%S")
                    })

            if not available_slots:
                return jsonify({"error": f"No suitable slots for Master ID {master_id} on {date}"}), 404

            return jsonify({"slots": available_slots})
        else:
            return jsonify({"error": "Failed to fetch data from CRM", "status_code": response.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_master', methods=['POST'])
def add_master():
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    master = Master(name=name)
    db.session.add(master)
    db.session.commit()
    return jsonify({"message": "Master added successfully!"})

@app.route('/add_procedure', methods=['POST'])
def add_procedure():
    data = request.json
    name = data.get('name')
    duration = data.get('duration')
    price = data.get('price')
    master_id = data.get('master_id')

    if not all([name, duration, price, master_id]):
        return jsonify({"error": "All fields are required"}), 400

    procedure = Procedure(name=name, duration=duration, price=price, master_id=master_id)
    db.session.add(procedure)
    db.session.commit()
    return jsonify({"message": "Procedure added successfully!"})

def preload_masters():
    """Добавление мастеров в базу данных при инициализации"""
    preloaded_masters = [
        {"id": 3079, "name": "Martsyniak Daria"},
        {"id": 2963, "name": "Viacheslav BCN"},
        {"id": 3067, "name": "Ekaterina Kuznetsova TRG"},
        {"id": 1532, "name": "Katerina (médico) BCN"},
        {"id": 2702, "name": "Katerina Tarragona"},
        {"id": 2962, "name": "Ushakov Viacheslav TRG"},
        {"id": 3084, "name": "Yulia Estetica"},
    ]

    for master_data in preloaded_masters:
        # Проверяем, существует ли мастер с таким ID
        if not db.session.get(Master, master_data["id"]):
            master = Master(id=master_data["id"], name=master_data["name"])
            db.session.add(master)
    db.session.commit()

# Редактировать мастера
@app.route('/edit_master/<int:master_id>', methods=['POST'])
def edit_master(master_id):
    data = request.json
    master = Master.query.get(master_id)
    if not master:
        return jsonify({"error": "Master not found"}), 404

    master.name = data.get('name', master.name)
    db.session.commit()
    return jsonify({"message": "Master updated successfully!"})

# Удалить мастера
@app.route('/delete_master/<int:master_id>', methods=['DELETE'])
def delete_master(master_id):
    master = Master.query.get(master_id)
    if not master:
        return jsonify({"error": "Master not found"}), 404

    db.session.delete(master)
    db.session.commit()
    return jsonify({"message": "Master deleted successfully!"})

# Редактировать процедуру
@app.route('/edit_procedure/<int:procedure_id>', methods=['POST'])
def edit_procedure(procedure_id):
    data = request.json
    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return jsonify({"error": "Procedure not found"}), 404

    procedure.name = data.get('name', procedure.name)
    procedure.duration = data.get('duration', procedure.duration)
    procedure.price = data.get('price', procedure.price)
    procedure.master_id = data.get('master_id', procedure.master_id)
    db.session.commit()
    return jsonify({"message": "Procedure updated successfully!"})

# Удалить процедуру
@app.route('/delete_procedure/<int:procedure_id>', methods=['DELETE'])
def delete_procedure(procedure_id):
    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return jsonify({"error": "Procedure not found"}), 404

    db.session.delete(procedure)
    db.session.commit()
    return jsonify({"message": "Procedure deleted successfully!"})


# API для создания платежной сессии
@app.route('/api/create_checkout', methods=['POST'])
def create_checkout():
    data = request.json
    master_id = data.get('master_id')
    date = data.get('date')
    time = data.get('time')

    if not all([master_id, date, time]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        # Создание Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f"Booking with Master {master_id} on {date} at {time}",
                    },
                    'unit_amount': 1000,  # 10 евро в центах
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:5000/success',
            cancel_url='http://127.0.0.1:5000/cancel',
        )

        return jsonify({"sessionId": session.id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Маршрут для успешной оплаты
@app.route('/success')
def success():
    return render_template('success.html')

# Маршрут для отменённой оплаты
@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

# Основной маршрут для отображения виджета
@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/api/get_procedures', methods=['GET'])
def get_procedures():
    # Получаем все процедуры из базы данных
    procedures = Procedure.query.all()

    if not procedures:
        return jsonify({"procedures": []})

    # Формируем список процедур
    procedures_data = [
        {"id": proc.id, "name": proc.name, "type": proc.type, "duration": proc.duration}
        for proc in procedures
    ]
    return jsonify({"procedures": procedures_data})





@app.route('/api/create_payment', methods=['POST'])
def create_payment():
    try:
        # Parse incoming JSON data
        data = request.get_json()
        print("Received data:", data)  # Debugging information

        # Required fields for validation
        required_fields = ['date', 'start_time', 'end_time', 'master_id', 'procedure_id', 'email', 'client_name']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "All fields are required, including name and email."}), 400

        # Extract and validate data
        email = data["email"]
        client_name = data["client_name"]
        date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        start_time = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S").time()
        end_time = datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S").time()
        master_id = data["master_id"]
        procedure_id = data["procedure_id"]

        print(f"Email: {email}, Client Name: {client_name}, Date: {date}")  # Debugging information

        # Create the PaymentIntent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=1000,  # Amount in cents (e.g., €10.00)
            currency="eur",
            receipt_email=email,
            metadata={
                "start_time": data["start_time"],
                "end_time": data["end_time"],
                "master_id": master_id,
                "date": data["date"],
                "procedure_id": procedure_id,
                "client_name": client_name
            }
        )
        print("PaymentIntent created successfully:", intent)

        # Save booking to the database
        new_booking = Booking(
            master_id=master_id,
            procedure_id=procedure_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            client_name=client_name,
            email=email
        )
        db.session.add(new_booking)
        db.session.commit()
        print("Booking saved successfully in the database.")

        # Save Stripe response to a text file for reference
        filename = f"stripe_payment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = f"/Users/germany/Desktop/impuls/pythonProject {filename}"  # Replace with a valid directory path
        with open(filepath, "w") as file:
            file.write(str(intent))  # Save the intent as text
        print(f"Stripe response saved to {filepath}")

        # Return the client secret to the front end
        return jsonify({"client_secret": intent.client_secret})
    except stripe.error.CardError as e:
        print(f"Card error: {e.error.message}")
        return jsonify({"error": e.error.message}), 402
    except stripe.error.RateLimitError as e:
        print("Too many requests to Stripe API")
        return jsonify({"error": "Rate limit error"}), 429
    except stripe.error.InvalidRequestError as e:
        print(f"Invalid parameters: {e.error.message}")
        return jsonify({"error": e.error.message}), 400
    except stripe.error.AuthenticationError as e:
        print("Authentication error, check API keys")
        return jsonify({"error": "Authentication error"}), 401
    except stripe.error.APIConnectionError as e:
        print("Network communication error with Stripe")
        return jsonify({"error": "Network error"}), 503
    except stripe.error.StripeError as e:
        print("Generic Stripe error:", str(e))
        return jsonify({"error": "Something went wrong with Stripe"}), 500
    except Exception as e:
        print("General error occurred:", str(e))  # Log unexpected errors
        return jsonify({"error": str(e)}), 500


@app.route('/api/get_procedure_duration', methods=['GET'])
def get_procedure_duration():
    procedure_id = request.args.get('procedure_id')
    if not procedure_id:
        return jsonify({"error": "Procedure ID is required"}), 400

    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return jsonify({"error": "Procedure not found"}), 404

    return jsonify({"duration": procedure.duration})



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создает все таблицы, если их еще нет
        preload_masters()
    app.run(debug=True)
