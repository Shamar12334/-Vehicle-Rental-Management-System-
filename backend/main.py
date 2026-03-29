from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# ----------------------------
# DB connection
# ----------------------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ----------------------------
# Create database + tables
# ----------------------------
def create_database():
    # connect without database first
    config = DB_CONFIG.copy()
    config.pop("database", None)

    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS vrms")
    conn.commit()
    cur.close()
    conn.close()

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS RentalBranch (
        BranchID INT PRIMARY KEY AUTO_INCREMENT,
        Name VARCHAR(100) NOT NULL,
        Address VARCHAR(255) NOT NULL,
        PhoneNumber VARCHAR(20) NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS VehicleType (
        TypeID INT PRIMARY KEY AUTO_INCREMENT,
        TypeName VARCHAR(20) UNIQUE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INT PRIMARY KEY AUTO_INCREMENT,
        FirstName VARCHAR(50) NOT NULL,
        LastName VARCHAR(50) NOT NULL,
        Address VARCHAR(255) NOT NULL,
        PhoneNumber VARCHAR(20) NOT NULL,
        Email VARCHAR(100) UNIQUE NOT NULL,
        DriversLicenseNumber VARCHAR(50) UNIQUE NOT NULL,
        DriversLicenseExpiryDate DATE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS MaintenanceStaff (
        StaffID INT PRIMARY KEY AUTO_INCREMENT,
        Name VARCHAR(100) NOT NULL,
        OfficeNumber VARCHAR(20),
        PhoneNumber VARCHAR(20) NOT NULL,
        Email VARCHAR(100) UNIQUE,
        BranchID INT NOT NULL,
        FOREIGN KEY (BranchID) REFERENCES RentalBranch(BranchID)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Vehicle (
        VehicleID INT PRIMARY KEY,
        LicensePlate VARCHAR(20) UNIQUE NOT NULL,
        Make VARCHAR(50) NOT NULL,
        Model VARCHAR(50) NOT NULL,
        `Year` INT NOT NULL,
        Color VARCHAR(30),
        DailyRentalRate DECIMAL(10, 2) NOT NULL,
        CurrentMileage INT NOT NULL,
        TypeID INT NOT NULL,
        BranchID INT NOT NULL,
        FOREIGN KEY (BranchID) REFERENCES RentalBranch(BranchID),
        FOREIGN KEY (TypeID) REFERENCES VehicleType(TypeID)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS RentalAgreement (
        AgreementID INT PRIMARY KEY AUTO_INCREMENT,
        CustomerID INT NOT NULL,
        VehicleID INT NOT NULL,
        PickupBranchID INT NOT NULL,
        ReturnBranchID INT NOT NULL,
        ScheduledPickupDateTime DATETIME NOT NULL,
        ScheduledReturnDateTime DATETIME NOT NULL,
        ActualPickupDateTime DATETIME,
        ActualReturnDateTime DATETIME,
        EstimatedCost DECIMAL(10, 2) NOT NULL,
        ActualCost DECIMAL(10, 2),
        Status VARCHAR(20) NOT NULL,
        CHECK (Status IN ('Booked', 'Active', 'Completed', 'Cancelled')),
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID),
        FOREIGN KEY (PickupBranchID) REFERENCES RentalBranch(BranchID),
        FOREIGN KEY (ReturnBranchID) REFERENCES RentalBranch(BranchID)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS MaintenanceRecord (
        RecordID INT PRIMARY KEY AUTO_INCREMENT,
        DateTimeReported DATETIME NOT NULL,
        VehicleID INT NOT NULL,
        ReportingCustomerID INT,
        AssignedMaintenanceStaffID INT,
        IssueType VARCHAR(20) NOT NULL,
        Description TEXT NOT NULL,
        Status VARCHAR(20) NOT NULL,
        DateTimeResolved DATETIME,
        Notes TEXT,
        CHECK (IssueType IN ('Routine', 'Urgent')),
        CHECK (Status IN ('Reported', 'In-progress', 'Complete', 'Awaiting Parts')),
        FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID),
        FOREIGN KEY (ReportingCustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (AssignedMaintenanceStaffID) REFERENCES MaintenanceStaff(StaffID)
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# ----------------------------
# Pydantic models
# ----------------------------
class CustomerCreate(BaseModel):
    FirstName: str
    LastName: str
    Address: str
    PhoneNumber: str
    Email: EmailStr
    DriversLicenseNumber: str
    DriversLicenseExpiryDate: date

class CustomerOut(CustomerCreate):
    CustomerID: int

# ----------------------------
# Routes
# ----------------------------
@app.get("/")
def root():
    return {"message": "VRMS API is running with MySQL"}

@app.post("/customers")
def create_customer(customer: CustomerCreate):
    if customer.DriversLicenseExpiryDate <= date.today():
        raise HTTPException(
            status_code=400,
            detail="DriversLicenseExpiryDate must be in the future"
        )

    sql = """
    INSERT INTO Customer
    (FirstName, LastName, Address, PhoneNumber, Email,
     DriversLicenseNumber, DriversLicenseExpiryDate)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    vals = (
        customer.FirstName,
        customer.LastName,
        customer.Address,
        customer.PhoneNumber,
        customer.Email,
        customer.DriversLicenseNumber,
        customer.DriversLicenseExpiryDate
    )

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql, vals)
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()

        return {"message": "Customer created successfully", "CustomerID": new_id}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers")
def list_customers():
    sql = """
    SELECT CustomerID, FirstName, LastName, Address, PhoneNumber, Email,
           DriversLicenseNumber, DriversLicenseExpiryDate
    FROM Customer
    ORDER BY CustomerID DESC
    """

    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
