from impulsapp import db, Procedure, app

# Список процедур для добавления
procedures = [
    {"name": "Aclaración del tatuaje", "type": "SW", "duration": 30},
    {"name": "Rejuvenecimiento FracTat", "type": "SW", "duration": 50},
    {"name": "Tratamiento de acné activo (corporal)", "type": "SP", "duration": 30},
    {"name": "Control", "type": None, "duration": 15},
    {"name": "Consulta", "type": None, "duration": 20},
    {"name": "Peeling con láser (Fotona 2D)", "type": "SP", "duration": 40},
    {"name": "Rejuvenecimiento 4D de Fotona", "type": "SP", "duration": 90},
    {"name": "Limpieza facial (manual)", "type": None, "duration": 60},
    {"name": "Rejuvenecimiento de labios (Lip Lase)", "type": "SP", "duration": 30},
    {"name": "BlackPeel (peeling de carbono con láser)", "type": "SW", "duration": 40},
    {"name": "Tratamiento de cicatrices", "type": "SP", "duration": 50},
    {"name": "Tratamiento de estrías", "type": "SP", "duration": 60},
    {"name": "Aclaración de ojeras", "type": "SW", "duration": 40},
    {"name": "Tratamiento de la caída del cabello (HaiRestart)", "type": "SP", "duration": 60},
    {"name": "Limpieza Hydrafacial + peeling", "type": None, "duration": 90},
    {"name": "Control Inyecciones", "type": None, "duration": 15},
    {"name": "SmasLifting (Lifting facial tercio inferior + tercio medio)", "type": "SP", "duration": 40},
    {"name": "SmasLifting (Lifting facial de toda la cara)", "type": "SP", "duration": 50},
    # Добавьте остальные процедуры, если нужно
]

# Добавление процедур в базу данных
with app.app_context():
    for proc in procedures:
        # Проверяем, существует ли уже процедура с таким именем
        existing_proc = Procedure.query.filter_by(name=proc["name"]).first()
        if not existing_proc:
            new_proc = Procedure(
                name=proc["name"],
                type=proc.get("type"),
                duration=proc.get("duration")
            )
            db.session.add(new_proc)
    db.session.commit()

print("Procedures added successfully!")
