from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI()
DB_FILE = "database.db"

# -------- DB connection --------
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# -------- Table creation --------
def create_tables():
    conn = sqlite3.connect(DB_FILE)
    #----------Customer table-------
    conn.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        CustomerID INTEGER PRIMARY KEY,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Address TEXT NOT NULL,
        PhoneNumber TEXT NOT NULL,
        Email TEXT UNIQUE NOT NULL,
        DriversLicenseNumber TEXT UNIQUE NOT NULL,
        DriversLicenseExpiryDate TEXT NOT NULL
    )
    """)
    #------------VehicleType-------------
    conn.execute("""
    CREATE TABLE VehicleType (
        TypeID INTEGER PRIMARY KEY AUTO_INCREMENT,
        TypeName TEXT UNIQUE NOT NULL
    )

    """)
    #-------------Vehicle----------------
    conn.execute("""
    CREATE TABLE Vehicle(
        VehicleID INTEGER PRIMARY KEY,
        LicensePlate TEXT UNIQUE NOT NULL,
        Make TEXT NOT NULL,
        Model TEXT NOT NULL,
        Year INTEGER NOT NULL,
        Color TEXT,
        DailyRentalRate DECIMAL(10, 2) NOT NULL,
        CurrentMileage INTEGER NOT NULL,
        TypeID INTEGER NOT NULL,
        BranchID INTEGER NOT NULL,
        FOREIGN KEY (BranchID) REFERENCES RentalBranch(BranchID),
        FOREIGN KEY (TypeID) REFERENCES VehicleType(TypeID)
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# -------- Pydantic schema --------
#-------customer schema------------
class Customer(BaseModel):
    FirstName: str
    LastName: str
    Address: str
    PhoneNumber: str
    Email: str
    DriversLicenseNumber: str
    DriversLicenseExpiryDate: str  # format "YYYY-MM-DD"

# -------- Route with expiry check --------
