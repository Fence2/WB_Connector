import psycopg2
import psycopg2.extras as extras
import pandas as pd
import numpy as np


class Postgres:
    WB_ORDERS_SCHEMA = """
    CREATE TABLE IF NOT EXISTS orders (
        srid TEXT PRIMARY KEY,
        gNumber VARCHAR(50),
        date TIMESTAMP,
        lastChangeDate TIMESTAMP,
        orderType VARCHAR(50),
        warehouseName VARCHAR(50),
        countryName VARCHAR(200),
        oblastOkrugName VARCHAR(200),
        regionName VARCHAR(200),
        supplierArticle VARCHAR(75),
        nmId INT,
        barcode VARCHAR(30),
        category VARCHAR(50),
        subject VARCHAR(50),
        brand VARCHAR(50),
        techSize VARCHAR(30),
        incomeID INT,
        isSupply BOOL,
        isRealization BOOL,
        totalPrice DECIMAL(15,2),
        discountPercent SMALLINT,
        spp DECIMAL(15,2),
        finishedPrice DECIMAL(15,2),
        priceWithDisc DECIMAL(15,2),
        isCancel BOOL,
        cancelDate TIMESTAMP,
        sticker TEXT
    )
    """

    def __init__(self, *, db_name: str, db_host: str, db_port: str, db_user: str, db_password: str):
        self.database = db_name
        self.user = db_user

        self.conn = psycopg2.connect(
            database=db_name,
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password
        )

    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            pass

    def initialize_db(self):
        with self.conn.cursor() as cur:
            try:
                cur.execute(Postgres.WB_ORDERS_SCHEMA)
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s" % error)
                return str(error)

    def execute_values(self, df: pd.DataFrame, table: str):
        """
        Загрузка DataFrame объекта в БД

        :param df: DataFrame объект, где столбцы = столбцы в таблице table
        :param table: Название таблицы в БД
        :return: При успешной вставке значений - возвращает количество вставленных строк. Иначе - текст ошибки
        """
        # Если значение не существует, заменяем значение nan на понятное для БД - None
        df.replace({np.nan: None}, inplace=True)

        data_rows = tuple([tuple(row) for row in df.to_numpy()])
        cols = ','.join(list(df.columns))

        query = "INSERT INTO %s (%s) VALUES %%s" % (table, cols)

        with (self.conn.cursor() as cur):
            try:
                extras.execute_values(cur, query, data_rows)
                result = cur.rowcount
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s" % error)
                self.conn.rollback()
                result = str(error)

        return result
