from pathlib import os as path_os
import os
import socket
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = str(path_os.getenv("FLASK_SECRET_KEY"))
SQLALCHEMY_DATABASE_URI = (
    'mysql+mysqlconnector://'
    f'{str(path_os.getenv("MYSQL_USERNAME"))}:'
    f'{str(path_os.getenv("MYSQL_PW"))}@'
    f'{".".join(socket.gethostbyname(socket.gethostname()).split(".")[:-1] + ["1"])}/gameteca' # NoQa
)
UPLOAD_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/uploads"
