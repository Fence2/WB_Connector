import config
import api
from models import Postgres
import pandas as pd

# Подключаемся в API Wildberries
wb = api.WB(config.wb_token)

# Получаем список заказов
# orders_json = wb.get_orders(date_from='2023-12-20')

# Тестовые данные
orders_json = [
    {
        "date": "2022-03-04T18:08:31",
        "lastChangeDate": "2022-03-06T10:11:07",
        "warehouseName": "Подольск",
        "countryName": "Россия",
        "oblastOkrugName": "Центральный федеральный округ",
        "regionName": "Московская",
        "supplierArticle": "12345",
        "nmId": 1234567,
        "barcode": "123453559000",
        "category": "Бытовая техника",
        "subject": "Мультистайлеры",
        "brand": "Тест",
        "techSize": "0",
        "incomeID": 56735459,
        "isSupply": False,
        "isRealization": True,
        "totalPrice": 1887,
        "discountPercent": 18,
        "spp": 26,
        "finishedPrice": 1145,
        "priceWithDisc": 1547,
        "isCancel": True,
        "cancelDate": "2022-03-09T00:00:00",
        "orderType": "Клиентский",
        "sticker": "926912515",
        "gNumber": "34343462218572569531",
        "srid": "11.rf9ef11fce1684117b0nhj96222982382.3.0"
    },
    {
        "date": "2022-05-04T18:15:31",
        "lastChangeDate": "2022-04-10T10:11:07",
        "warehouseName": "Тюмень",
        "countryName": "Россия",
        "oblastOkrugName": "Тюменская область",
        "regionName": "Тюменский",
        "supplierArticle": "54352",
        "nmId": 9387123,
        "barcode": "4141242453",
        "category": "Цифровые товары",
        "subject": "Мультистайлеры",
        "brand": "Тест",
        "techSize": "0",
        "incomeID": 56735459,
        "isSupply": False,
        "isRealization": True,
        "totalPrice": 1887,
        "discountPercent": 5,
        "spp": 26,
        "finishedPrice": 1145,
        "priceWithDisc": 1547,
        "isCancel": False,
        "cancelDate": "2022-03-09T00:00:00",
        "orderType": "Клиентский",
        # "sticker": None,
        "gNumber": "34343462218572569531",
        "srid": "13.rf9ef11fcesfasvwe17b0nhj96222982382.3.0"
    }
]

# Подключаемся к СУБД PostgreSQL
psql = Postgres(
    db_name=config.db_name,
    db_host=config.db_host,
    db_port=config.db_port,
    db_user=config.db_user,
    db_password=config.db_password
)

# Инициализируем БД (Создаем основные таблицы)
x = psql.initialize_db()

# Формируем датафрейм с заказами
orders_df: pd.DataFrame = pd.DataFrame.from_dict(orders_json)

# Загружаем заказы в таблицу orders
result = psql.execute_values(orders_df, 'orders')

# Выводим результат загрузки заказов
if isinstance(result, int):
    print(f"Всего загружено {result} заказов")
else:
    print(result)  # Ошибка

