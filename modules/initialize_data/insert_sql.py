from modules.shared_params.param_config import DatabaseConnection
        
def save_stock_data_to_mssql(data, table_name, db_connection):
    """
    將 DataFrame 存入 MSSQL 資料庫，使用 SQL Server 驗證。

    Args:
        data (pd.DataFrame): 要存入的數據。
        table_name (str): 資料表名稱。
        server (str): MSSQL 伺服器名稱或 IP。
        database (str): 資料庫名稱。
        username (str): SQL Server 帳號。
        password (str): SQL Server 密碼。
    """
    
    try:
        cursor = db_connection.get_cursor()
        
        # 創建資料表（如果不存在）
        cursor.execute(f"""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
        CREATE TABLE {table_name} (
            [Trading_Date] DATE,
            [Open_Price] FLOAT,
            [High_Price] FLOAT,
            [Low_Price] FLOAT,
            [Close_Price] FLOAT,
            [Trading_Volume] BIGINT,
            [Stock_Code] VARCHAR(50)
        )
        """)

        for index, row_data in data.iterrows():
            try:
                cursor.execute(
                    "INSERT INTO " + table_name +
                    " ([Trading_Date],[Open_Price],[High_Price],[Low_Price],[Close_Price],[Trading_Volume],[Stock_Code]) " +
                    "VALUES (?,?,?,?,?,?,?)",
                    (
                        row_data['Date'].date(),
                        float(row_data['Open']),
                        float(row_data['High']),
                        float(row_data['Low']),
                        float(row_data['Close']),
                        int(row_data['Volume']),
                        str(row_data['Stock_Code'])
                    )
                )
            except Exception as e:
                print(f"插入數據時發生錯誤: {str(e)}")
                print(f"錯誤數據: {row_data}")
                continue

        db_connection.conn.commit()
        print(f"成功將數據存入資料表 {table_name}！")

    except Exception as e:
        print(f"儲存數據到 MSSQL 時發生錯誤: {str(e)}")
        raise
    finally:
        # 確保關閉資料庫連線
        db_connection.close()
        
def save_data_to_mssql(data, table_name, db_connection):
    """
    通用函式：將 DataFrame 存入 MSSQL 資料庫。
    支援中文表名和列名。

    Args:
        data (pd.DataFrame): 要存入的數據。
        table_name (str): 資料表名稱。
        db_connection (DatabaseConnection): MSSQL 資料庫連線物件。
    """
    try:
        cursor = db_connection.get_cursor()

        # 動態生成表結構（處理中文列名）
        column_definitions = ", ".join([
            f"[{col}] FLOAT" if dtype in ['float64', 'int64'] else f"[{col}] NVARCHAR(MAX)"
            for col, dtype in zip(data.columns, data.dtypes)
        ])
        create_table_query = f"""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
        CREATE TABLE {table_name} ({column_definitions})
        """
        cursor.execute(create_table_query)
        db_connection.conn.commit()

        # 準備批量插入（處理中文列名）
        placeholders = ", ".join(["?" for _ in data.columns])
        column_names = ", ".join([f"[{col}]" for col in data.columns])
        insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

        # 將數據轉換為元組列表
        data_tuples = [tuple(row) for row in data.itertuples(index=False, name=None)]

        # 批量插入
        cursor.executemany(insert_query, data_tuples)
        db_connection.conn.commit()

        print(f"數據已成功存入資料表: {table_name}！")

    except Exception as e:
        print(f"儲存數據到 MSSQL 時發生錯誤: {e}")
        raise
    finally:
        db_connection.close()
        