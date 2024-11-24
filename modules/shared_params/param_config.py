import pyodbc

def mssql_login_info():
    """返回 MSSQL 登入資訊"""
    server = 'localhost'
    database = 'Finance_data'
    username = 'tony'
    password = '12345678'
    return server, database, username, password

class DatabaseConnection:
    def __init__(self, login_info_func):
        """
        初始化資料庫連線物件
        :param login_info_func: 函式，用於提供資料庫連線資訊
        """
        self.server, self.database, self.username, self.password = login_info_func()
        self.conn = None

    def connect(self):
        """建立與資料庫的連線"""
        if not self.conn:  # 確保只建立一次連線
            self.conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password}'
            )
        return self.conn

    def get_cursor(self):
        """取得游標物件"""
        if not self.conn:
            self.connect()
        return self.conn.cursor()

    def close(self):
        """關閉資料庫連線"""
        if self.conn:
            self.conn.close()
            self.conn = None
