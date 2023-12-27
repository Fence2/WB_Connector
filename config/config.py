from dotenv import load_dotenv
import os

load_dotenv()

wb_token: str = os.getenv('WB_TOKEN')

if wb_token is None or len(wb_token) == 0:
    raise ValueError("Токен для API авторизации к Wildberries не найден в файле .env")

__all__ = ['wb_token']
