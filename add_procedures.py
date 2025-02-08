from app import db, create_app  
from models.procedure import Procedure

app = create_app()

procedures_data = [
    {"name": "Aclaración del tatuaje", "category": "SW", "duration": "30 min"},
    {"name": "Aclaración del tatuaje/micropigmentación (cejas)", "category": "SW", "duration": "20 min"},
    {"name": "Aclaración del tatuaje/micropigmentación (labios)", "category": "SP", "duration": "20 min"},
    {"name": "Onicomicosis (hongos de las uñas)", "category": "SR", "duration": "60 min"},
    {"name": "Eliminacion de arañas vasculares (piernas)", "category": "SW", "duration": "30 min"},
    {"name": "Aclaramiento de la pigmentación (corporal)", "category": "SW", "duration": "20 min"},
    {"name": "Consulta", "category": "SW", "duration": "50 min"},
    {"name": "Rejuvenecimiento FracTat", "category": "SW", "duration": "30 min"},
    {"name": "Aclaramiento de la pigmentación (manos)", "category": "SW", "duration": "20 min"},
    {"name": "Tratamiento de acné activo (corporal)", "category": "SW", "duration": "30 min"},
    {"name": "Control", "category": "SW", "duration": "15 min"},
    {"name": "Aclaramiento de la pigmentación (ingles)", "category": "SW", "duration": "30 min"},
    {"name": "Beauty Pack", "category": "SW", "duration": "40 min"},
    {"name": "Limpieza facial (manual)", "category": "SW", "duration": "1 h"},
    {"name": "Rejuvenecimiento 4D de Fotona", "category": "SP", "duration": "90 min"},
    {"name": "Rejuvenecimiento 4D de Fotona (sin peeling)", "category": "SP", "duration": "80 min"},
    {"name": "Rejuvenecimiento de la zona periocular (Smooth Eye)", "category": "SP", "duration": "60 min"},
    {"name": "Tratamiento del ronquido (NightLase)", "category": "SP", "duration": "30 min"},
    {"name": "Consulta Tatuaje", "category": "SP", "duration": "20 min"},
    {"name": "Tratamiento de Rosacea/Cuperosis", "category": "SP", "duration": "30 min"},
    {"name": "Eliminación de Arañas vasculares (facial)", "category": "SP", "duration": "30 min"},
    {"name": "Reinición de puntos Rubí", "category": "SP", "duration": "20 min"},
    {"name": "Tratamiento de las secuelas de acné (láser StarWalker)", "category": "SP", "duration": "50 min"},
    {"name": "Peeling con láser (Fotona 2D)", "category": "SP", "duration": "30 min"},
    {"name": "Rejuvenecimiento de labios (Lip Lase)", "category": "SP", "duration": "30 min"},
    {"name": "BlackPeel (peeling de carbón con láser)", "category": "SP", "duration": "30 min"},
    {"name": "Rejuvenecimiento StarWalker", "category": "SW", "duration": "30 min"},
    {"name": "Tratamiento de cicatrices", "category": "SW", "duration": "60 min"},
    {"name": "Tratamiento de estrias", "category": "SW", "duration": "40 min"},
    {"name": "Aclaramiento de la pigmentación (manos+antebrazos)", "category": "SW", "duration": "40 min"},
    {"name": "Tratamiento de Melasma", "category": "SW", "duration": "40 min"},
    {"name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (abdomen)", "category": "SP", "duration": "180 min"},
    {"name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (gluteos)", "category": "SP", "duration": "180 min"},
    {"name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (brazos)", "category": "SP", "duration": "150 min"},
    {"name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (papada)", "category": "SP", "duration": "90 min"},
    {"name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (flancos)", "category": "SP", "duration": "180 min"},
    {"name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (muslos)", "category": "SP", "duration": "180 min"},
    {"name": "Tratamiento de grasa localizada y tensado cutaneo TightSculpting (rodillas)", "category": "SP", "duration": "120 min"},
    {"name": "Aclaración de acné activo", "category": "SW", "duration": "60 min"},
    {"name": "Aclaración de la pigmentación facial", "category": "SW", "duration": "40 min"},
    {"name": "Tratamiento de cicatrices hiperpigmentadas", "category": "SP", "duration": "30 min"},
    {"name": "Dermapen", "category": "SW", "duration": "30 min"},
]

with app.app_context():
    for procedure_data in procedures_data:
        procedure = Procedure(
            name=procedure_data["name"],
            category=procedure_data["category"],
            duration=procedure_data["duration"]
        )
        db.session.add(procedure)
    db.session.commit()

print("Procedures added successfully!")
