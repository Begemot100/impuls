from models import db
from models.procedure import Procedure

# Таблица для связи многие ко многим
employee_procedures = db.Table('employee_procedures',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.id'), primary_key=True),
    db.Column('procedure_id', db.Integer, db.ForeignKey('procedures.id'), primary_key=True)
)

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)

    # Добавляем связь с процедурами
    procedures = db.relationship('Procedure', secondary=employee_procedures, backref='employees')
