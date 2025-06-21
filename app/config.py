import os
import requests

basedir = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(basedir, '..', 'src', 'assets', 'data', 'data.db')

try:
    checker = requests.get('https://google.com')
    if checker.status_code == 200:
        SQLALCHEMY_DATABASE_URI = "postgresql://dynax_towi_user:lcOA6Tz5CYo5YKdtT1eCAU5y9px0H4yE@dpg-d1biebmuk2gs739qhrng-a.oregon-postgres.render.com/dynax_towi"
except Exception as E:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.abspath(db_path)}"

DEVELOPER = "A.I Instaraj"
API_TOKEN = "7808377808:AAGkatfsVibkW1MAP9eVaON1K9Z8SMbJrhI"
SECRET_KEY = "Abbr..8080:4025x%3054.{}@index.dyn.las"
STATIC_FOLDER = 'src/assets'
START_MSG = "Hey!. This is Dynax ✨"
ABOUT_MSG = "Dynax!. A bot for scraping metadata about research publications. Built with Love by A.I Instaraj🏅🌹."
URL = "https://scholar.google.com"
DRIVER = "C:\\Users\\USER\\OneDrive\\Documents\\Advanced Projects\\Dynax\src\\chromedriver.exe"
NAME = "Dynax!"
DEPLOY_OPTIONS = "RENDER"
INTERFACE = "TELEGRAM"
LANGUAGE = "PYTHON"
LIBRARY = "BEAUTIFULSOUP"
SITE = "GOOGLE SCHOLAR"
FRAMEWORK = "FLASK"
GATEWAY = "WSGI"
ENGINE = "JINJA"
CATEGORIES = "RESEARCH"
DOCS = "readme"
PDF_FOLDER = "PDF"