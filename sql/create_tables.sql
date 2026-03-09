-- Brussels Mobility Quantum Analytics
-- SQL Server Data Warehouse Schema
-- Author: Salwa
-- Date: March 2026

-- ============================================
-- STAGING TABLES (Real-Time Ingestion)
-- ============================================

CREATE TABLE STG_Villo_Realtime (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Station VARCHAR(100),
    Bikes_Available INT,
    Capacity INT,
    Latitude DECIMAL(9,6),
    Longitude DECIMAL(9,6),
    Status VARCHAR(50),
    Insertion_Timestamp DATETIME DEFAULT GETDATE()
);

CREATE TABLE STG_STIB_Realtime (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Station VARCHAR(100),
    Line_ID VARCHAR(20),
    GPS_Latitude DECIMAL(9,6),
    GPS_Longitude DECIMAL(9,6),
    Insertion_Timestamp DATETIME DEFAULT GETDATE()
);

-- ============================================
-- DIMENSION TABLES
-- ============================================

CREATE TABLE DIM_Quartiers (
    Quartier_ID INT PRIMARY KEY,
    Nom VARCHAR(100),
    Code_Postal VARCHAR(10),
    Population INT,
    Surface_KM2 DECIMAL(5,2)
);

-- ============================================
-- FACT TABLE
-- ============================================

CREATE TABLE FAIT_Performance_Mobilite (
    Performance_ID INT IDENTITY(1,1) PRIMARY KEY,
    Quartier_ID INT FOREIGN KEY REFERENCES DIM_Quartiers(Quartier_ID),
    Date DATE,
    Score_Mobilite DECIMAL(5,2),
    Velos_Disponibles_Avg INT,
    Temp_Max_Celsius DECIMAL(4,1),
    Pluie_mm DECIMAL(5,2)
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX IX_STG_Villo_Timestamp ON STG_Villo_Realtime(Insertion_Timestamp);
CREATE INDEX IX_FAIT_Date ON FAIT_Performance_Mobilite(Date);
