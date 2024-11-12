from datetime import datetime
from models import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedures.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    procedure = db.relationship('Procedure', backref='bookings')
    employee = db.relationship('Employee', backref='bookings')

    def __init__(self, client_name, procedure_id, employee_id, booking_date, booking_time):
        self.client_name = client_name
        self.procedure_id = procedure_id
        self.employee_id = employee_id
        self.booking_date = booking_date
        self.booking_time = booking_time
