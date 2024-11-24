class DatabaseConnection:
    def __init__(self, login_info_func):
        """
        初始化資料庫連線物件
        :param login_info_func: 函式，用於提供資料庫連線資訊
        """
        self.server, self.database, self.username, self.password = login_info_func()
        self.conn = None
