from pathlib import os as path_os
import os
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = str(path_os.getenv("FLASK_SECRET_KEY"))
SQLALCHEMY_DATABASE_URI = (
    'mysql+mysqlconnector://'
    f'{str(path_os.getenv("MYSQL_USERNAME"))}:'
    f'{str(path_os.getenv("MYSQL_PW"))}@'
    f'{str(path_os.getenv("MYSQL_HOST"))}/gameteca'
)
UPLOAD_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/uploads"
