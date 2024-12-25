from modules.shared_params.param_config import DatabaseConnection,mssql_login_info

def save_cpi_data_to_mssql(data, db_connection):
    """
    將 CPI 數據存入 MSSQL 的 CPI_HISTORICAL_DATA 資料表。

    Args:
        data (pd.DataFrame): 包含 CPI 數據的 DataFrame。
        db_connection (DatabaseConnection): MSSQL 資料庫連線物件。
    """
    try:
        cursor = db_connection.get_cursor()

        create_table_query = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CPI_HISTORICAL_DATA' AND xtype='U')
        CREATE TABLE CPI_HISTORICAL_DATA (
            ID INT IDENTITY(1,1) PRIMARY KEY,
            REPORT_DATE DATE NOT NULL,
            CPIAUCSL DECIMAL(10, 2) NOT NULL,
            MONTHLY_INFLATION_RATE DECIMAL(10, 4) NULL
        )
        """
        cursor.execute(create_table_query)
        db_connection.conn.commit()
        
        # 自動生成 ID 欄位
        data['ID'] = range(1, len(data) + 1)

        # 確保數據格式正確
        data['REPORT_DATE'] = pd.to_datetime(data['REPORT_DATE'])
        data['CPIAUCSL'] = pd.to_numeric(data['CPIAUCSL'], errors='coerce')
        data['MONTHLY_INFLATION_RATE'] = pd.to_numeric(data['MONTHLY_INFLATION_RATE'], errors='coerce')

        placeholders = "?, ?, ?"
        insert_query = "INSERT INTO CPI_HISTORICAL_DATA (REPORT_DATE, CPIAUCSL, MONTHLY_INFLATION_RATE) VALUES (" + placeholders + ")"
        data_tuples = [tuple(row) for row in data.itertuples(index=False, name=None)]

        cursor.executemany(insert_query, data_tuples)
        db_connection.conn.commit()

        print("CPI 數據已成功存入 CPI_HISTORICAL_DATA 資料表！")

    except Exception as e:
        print(f"儲存 CPI 數據到 MSSQL 時發生錯誤: {e}")
        raise
    finally:
        db_connection.close()

def save_interest_rate_data_to_mssql(data, db_connection):
    """
    將利率數據存入 MSSQL 的 INTEREST_RATE_DATA 資料表。

    Args:
        data (pd.DataFrame): 包含利率數據的 DataFrame。
        db_connection (DatabaseConnection): MSSQL 資料庫連線物件。
    """
    try:
        cursor = db_connection.get_cursor()

        create_table_query = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='INTEREST_RATE_DATA' AND xtype='U')
        CREATE TABLE INTEREST_RATE_DATA (
            ID INT IDENTITY(1,1) PRIMARY KEY,
            REPORT_DATE DATE NOT NULL,
            UPPER_TARGET_RATE DECIMAL(10, 4) NOT NULL,
            LOWER_TARGET_RATE DECIMAL(10, 4) NOT NULL,
            POLICY_RATE DECIMAL(10, 4) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        db_connection.conn.commit()
        
        # 自動生成 ID 欄位
        data['ID'] = range(1, len(data) + 1)

        # 確保數據格式正確
        data['REPORT_DATE'] = pd.to_datetime(data['REPORT_DATE'])
        data['UPPER_TARGET_RATE'] = pd.to_numeric(data['UPPER_TARGET_RATE'], errors='coerce')
        data['LOWER_TARGET_RATE'] = pd.to_numeric(data['LOWER_TARGET_RATE'], errors='coerce')
        data['POLICY_RATE'] = pd.to_numeric(data['POLICY_RATE'], errors='coerce')

        placeholders = "?, ?, ?, ?"
        insert_query = "INSERT INTO INTEREST_RATE_DATA (REPORT_DATE, UPPER_TARGET_RATE, LOWER_TARGET_RATE, POLICY_RATE) VALUES (" + placeholders + ")"
        data_tuples = [tuple(row) for row in data.itertuples(index=False, name=None)]

        cursor.executemany(insert_query, data_tuples)
        db_connection.conn.commit()

        print("利率數據已成功存入 INTEREST_RATE_DATA 資料表！")

    except Exception as e:
        print(f"儲存利率數據到 MSSQL 時發生錯誤: {e}")
        raise
    finally:
        db_connection.close()

def save_stock_data_to_mssql(data, db_connection):
    """
    將股票數據存入 MSSQL 的 STOCK_HISTORICAL_DATA 資料表。

    Args:
        data (pd.DataFrame): 包含股票數據的 DataFrame。
        db_connection (DatabaseConnection): MSSQL 資料庫連線物件。
    """
    try:
        cursor = db_connection.get_cursor()

        create_table_query = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='STOCK_HISTORICAL_DATA' AND xtype='U')
        CREATE TABLE STOCK_HISTORICAL_DATA (
            ID INT IDENTITY(1,1) PRIMARY KEY,
            STOCK_CODE NVARCHAR(50) NOT NULL,
            TRADE_DATE DATE NOT NULL,
            OPEN_PRICE DECIMAL(18, 2) NULL,
            HIGH_PRICE DECIMAL(18, 2) NULL,
            LOW_PRICE DECIMAL(18, 2) NULL,
            CLOSE_PRICE DECIMAL(18, 2) NULL,
            ADJ_CLOSE_PRICE DECIMAL(18, 2) NULL,
            VOLUME BIGINT NULL
        )
        """
        cursor.execute(create_table_query)
        db_connection.conn.commit()
        
          # 自動生成 ID 欄位
        data['ID'] = range(1, len(data) + 1)

        # 確保數據格式正確
        data['TRADE_DATE'] = pd.to_datetime(data['TRADE_DATE'])
        data['OPEN_PRICE'] = pd.to_numeric(data['OPEN_PRICE'], errors='coerce')
        data['HIGH_PRICE'] = pd.to_numeric(data['HIGH_PRICE'], errors='coerce')
        data['LOW_PRICE'] = pd.to_numeric(data['LOW_PRICE'], errors='coerce')
        data['CLOSE_PRICE'] = pd.to_numeric(data['CLOSE_PRICE'], errors='coerce')
        data['ADJ_CLOSE_PRICE'] = pd.to_numeric(data['ADJ_CLOSE_PRICE'], errors='coerce')
        data['VOLUME'] = pd.to_numeric(data['VOLUME'], errors='coerce')

        placeholders = "?, ?, ?, ?, ?, ?, ?, ?"
        insert_query = "INSERT INTO STOCK_HISTORICAL_DATA (STOCK_CODE, TRADE_DATE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE, ADJ_CLOSE_PRICE, VOLUME) VALUES (" + placeholders + ")"
        data_tuples = [tuple(row) for row in data.itertuples(index=False, name=None)]

        cursor.executemany(insert_query, data_tuples)
        db_connection.conn.commit()

        print("股票數據已成功存入 STOCK_HISTORICAL_DATA 資料表！")

    except Exception as e:
        print(f"儲存股票數據到 MSSQL 時發生錯誤: {e}")
        raise
    finally:
        db_connection.close()
