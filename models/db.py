import psycopg2


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
            except Exception as e:
                return str(e)
