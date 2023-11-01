import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

USERNAME = str(os.getenv('USERNAME'))

PASSWORD = str(os.getenv('PASSWORD'))

API_TOKEN = str(os.getenv('API_TOKEN'))

EMAIL = str(os.getenv('EMAIL'))

API_KEY = str(os.getenv('API_KEY'))

MYSQL_USER = str(os.getenv('MYSQL_USER'))

MYSQL_PASSWORD = str(os.getenv('MYSQL_PASSWORD'))

MYSQL_HOST = str(os.getenv('MYSQL_HOST'))

MYSQL_PORT = str(os.getenv('MYSQL_PORT'))

PAY_TOKEN = str(os.getenv('PAY_TOKEN'))
