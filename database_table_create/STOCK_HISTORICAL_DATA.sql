CREATE TABLE STOCK_HISTORICAL_DATA (
    ID INT IDENTITY(1,1) PRIMARY KEY,         -- 自動遞增的唯一識別碼
    STOCK_CODE NVARCHAR(50) NOT NULL,         -- 股票代號
    TRADE_DATE DATE NOT NULL,                 -- 交易日期
    OPEN_PRICE DECIMAL(18, 2) NULL,           -- 開盤價
    HIGH_PRICE DECIMAL(18, 2) NULL,           -- 最高價
    LOW_PRICE DECIMAL(18, 2) NULL,            -- 最低價
    CLOSE_PRICE DECIMAL(18, 2) NULL,          -- 收盤價
    ADJ_CLOSE_PRICE DECIMAL(18, 2) NULL,      -- 調整後收盤價
    VOLUME BIGINT NULL                        -- 交易量
);
