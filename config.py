import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_hard_to_guess_string'
    CRM_API_KEY = ''
    CRM_BASE_URL = 'https://fotona.crmexpert.md'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crmimpuls.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
