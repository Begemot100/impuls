import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_hard_to_guess_string'
    CRM_API_KEY = '35fdd66e-7f4e-4281-81ae-2a0411344a9e'
    CRM_BASE_URL = 'https://fotona.crmexpert.md'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crmimpuls.db'  # Укажите путь к базе данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False
