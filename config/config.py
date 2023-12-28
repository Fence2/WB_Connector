from dotenv import load_dotenv
import os

load_dotenv()

wb_token: str = os.getenv('WB_TOKEN')

if wb_token is None or len(wb_token) == 0:
    raise ValueError("Токен для API авторизации к Wildberries не найден в файле .env")

db_name: str = os.getenv('DB_NAME')
db_host: str = os.getenv('DB_HOST')
db_port: str = os.getenv('DB_PORT')
db_user: str = os.getenv('DB_USER')
db_password: str = os.getenv('DB_PASSWORD')

if not all((db_name, db_host, db_port, db_user, db_password)):
    raise ValueError("Для доступа к СУБД введены не все данные в файле .env")


__all__ = ['wb_token', 'db_name', 'db_host', 'db_port', 'db_user', 'db_password']
