# ============================================================
# VRMS - Vehicle Rental Management System
# Backend: FastAPI + MySQL
# AI Disclosure: Portions of this code were generated/assisted
#   by Claude (Anthropic). Developer remains fully responsible.
# ============================================================

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional
import mysql.connector
import os
from datetime import datetime

app = FastAPI(title="VRMS API", version="1.0.0")

# ---------------------------------------------------------------
# CORS — allow React dev server
# ---------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------
# DB Connection helper
# ---------------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="vrms_user",
        password="Vrms_1234_Secure",
        database="vrms",
    )

# ---------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------
class VehicleCreate(BaseModel):
    LicensePlate: str
    Make: str
    Model: str
    Year: int
    Color: Optional[str] = None
    DailyRentalRate: float
    CurrentMileage: int = 0
    TypeID: int
    BranchID: int

    @field_validator("Year")
    @classmethod
    def valid_year(cls, v):
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 1:
            raise ValueError(f"Year must be between 1900 and {current_year + 1}")
        return v

    @field_validator("DailyRentalRate")
    @classmethod
    def positive_rate(cls, v):
        if v <= 0:
            raise ValueError("Daily rental rate must be greater than 0")
        return v

    @field_validator("CurrentMileage")
    @classmethod
    def non_negative_mileage(cls, v):
        if v < 0:
            raise ValueError("Mileage cannot be negative")
        return v

    @field_validator("LicensePlate")
    @classmethod
    def non_empty_plate(cls, v):
        if not v.strip():
            raise ValueError("License plate cannot be empty")
        return v.strip().upper()

# ---------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "VRMS API is running"}

# --- Lookups (for dropdowns) ---
@app.get("/vehicle-types")
def get_vehicle_types():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT TypeID, TypeName FROM VehicleType ORDER BY TypeName")
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

@app.get("/branches")
def get_branches():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT BranchID, Name, Address FROM RentalBranch ORDER BY Name")
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

# --- Vehicles ---
@app.get("/vehicles")
def get_vehicles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            v.VehicleID,
            v.LicensePlate,
            v.Make,
            v.Model,
            v.Year,
            v.Color,
            v.DailyRentalRate,
            v.CurrentMileage,
            vt.TypeName,
            rb.Name AS BranchName
        FROM Vehicle v
        JOIN VehicleType vt ON v.TypeID = vt.TypeID
        JOIN RentalBranch rb ON v.BranchID = rb.BranchID
        ORDER BY v.VehicleID
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    return result

@app.post("/vehicles", status_code=201)
def create_vehicle(vehicle: VehicleCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Check duplicate license plate
    cursor.execute("SELECT VehicleID FROM Vehicle WHERE LicensePlate = %s", (vehicle.LicensePlate,))
    if cursor.fetchone():
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="A vehicle with this license plate already exists.")

    # Check TypeID exists
    cursor.execute("SELECT TypeID FROM VehicleType WHERE TypeID = %s", (vehicle.TypeID,))
    if not cursor.fetchone():
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="Invalid vehicle type ID.")

    # Check BranchID exists
    cursor.execute("SELECT BranchID FROM RentalBranch WHERE BranchID = %s", (vehicle.BranchID,))
    if not cursor.fetchone():
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="Invalid branch ID.")

    cursor.execute("""
        INSERT INTO Vehicle (LicensePlate, Make, Model, Year, Color, DailyRentalRate, CurrentMileage, TypeID, BranchID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        vehicle.LicensePlate, vehicle.Make, vehicle.Model, vehicle.Year,
        vehicle.Color, vehicle.DailyRentalRate, vehicle.CurrentMileage,
        vehicle.TypeID, vehicle.BranchID
    ))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close(); conn.close()
    return {"message": "Vehicle added successfully.", "VehicleID": new_id}

# --- Customers ---
@app.get("/customers")
def get_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT CustomerID, FirstName, LastName, Address, PhoneNumber, Email,
               DriversLicenseNumber, DriversLicenseExpiryDate
        FROM Customer
        ORDER BY LastName, FirstName
    """)
    result = cursor.fetchall()
    cursor.close(); conn.close()
    # Convert date to string for JSON serialization
    for row in result:
        if row.get("DriversLicenseExpiryDate"):
            row["DriversLicenseExpiryDate"] = str(row["DriversLicenseExpiryDate"])
    return result

# --- Rental Agreements by Customer ID ---
@app.get("/rental-agreements")
def get_rental_agreements(customer_id: int = Query(..., description="Customer ID to look up")):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verify customer exists
    cursor.execute("SELECT CustomerID, FirstName, LastName FROM Customer WHERE CustomerID = %s", (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        cursor.close(); conn.close()
        raise HTTPException(status_code=404, detail=f"No customer found with ID {customer_id}.")

    cursor.execute("""
        SELECT
            ra.AgreementID,
            ra.Status,
            ra.ScheduledPickupDateTime,
            ra.ScheduledReturnDateTime,
            ra.ActualPickupDateTime,
            ra.ActualReturnDateTime,
            ra.EstimatedCost,
            ra.ActualCost,
            v.Make,
            v.Model,
            v.Year,
            v.LicensePlate,
            vt.TypeName,
            pb.Name AS PickupBranch,
            rb2.Name AS ReturnBranch
        FROM RentalAgreement ra
        JOIN Vehicle v ON ra.VehicleID = v.VehicleID
        JOIN VehicleType vt ON v.TypeID = vt.TypeID
        JOIN RentalBranch pb ON ra.PickupBranchID = pb.BranchID
        JOIN RentalBranch rb2 ON ra.ReturnBranchID = rb2.BranchID
        WHERE ra.CustomerID = %s
        ORDER BY ra.ScheduledPickupDateTime DESC
    """, (customer_id,))

    agreements = cursor.fetchall()
    cursor.close(); conn.close()

    # Serialize datetimes
    for row in agreements:
        for key in ["ScheduledPickupDateTime", "ScheduledReturnDateTime",
                    "ActualPickupDateTime", "ActualReturnDateTime"]:
            if row.get(key):
                row[key] = str(row[key])

    return {
        "customer": customer,
        "agreements": agreements
    }