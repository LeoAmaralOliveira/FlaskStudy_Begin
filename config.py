from pathlib import os
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = str(os.getenv("FLASK_SECRET_KEY"))
SQLALCHEMY_DATABASE_URI = (
    'mysql+mysqlconnector://'
    f'{str(os.getenv("MYSQL_USERNAME"))}:'
    f'{str(os.getenv("MYSQL_PW"))}@'
    f'{str(os.getenv("MYSQL_HOST"))}/gameteca'
)
