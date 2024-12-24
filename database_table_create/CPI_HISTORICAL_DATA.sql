CREATE TABLE CPI_HISTORICAL_DATA (
    ID INT IDENTITY(1,1) PRIMARY KEY,         -- 自動遞增的唯一識別碼
    REPORT_DATE DATE NOT NULL,                -- 報告日期
    CPIAUCSL DECIMAL(10, 2) NOT NULL          -- 消費者物價指數（CPIAUCSL）
);
