CREATE TABLE INTEREST_RATE_DATA (
    ID INT IDENTITY(1,1) PRIMARY KEY,         -- 自動遞增的唯一識別碼
    REPORT_DATE DATE NOT NULL,                -- 報告日期
    FEDFUNDS DECIMAL(10, 4) NOT NULL          -- 聯邦基準利率（FEDFUNDS）
);
