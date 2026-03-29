-- ============================================================
-- VRMS - Vehicle Rental Management System
-- Seed File: Creates all tables and inserts sample data
-- ============================================================

CREATE DATABASE IF NOT EXISTS vrms;
USE vrms;

-- ---------------------------------------------------------------
-- DROP TABLES (in reverse dependency order for clean re-runs)
-- ---------------------------------------------------------------
DROP TABLE IF EXISTS MaintenanceRecord;
DROP TABLE IF EXISTS RentalAgreement;
DROP TABLE IF EXISTS MaintenanceStaff;
DROP TABLE IF EXISTS Vehicle;
DROP TABLE IF EXISTS VehicleType;
DROP TABLE IF EXISTS RentalBranch;
DROP TABLE IF EXISTS Customer;

-- ---------------------------------------------------------------
-- TABLE: Customer
-- ---------------------------------------------------------------
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    DriversLicenseNumber VARCHAR(50) UNIQUE NOT NULL,
    DriversLicenseExpiryDate DATE NOT NULL
);

-- ---------------------------------------------------------------
-- TABLE: RentalBranch
-- ---------------------------------------------------------------
CREATE TABLE RentalBranch (
    BranchID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL
);

-- ---------------------------------------------------------------
-- TABLE: VehicleType
-- ---------------------------------------------------------------
CREATE TABLE VehicleType (
    TypeID INT PRIMARY KEY AUTO_INCREMENT,
    TypeName VARCHAR(20) UNIQUE NOT NULL
);

-- ---------------------------------------------------------------
-- TABLE: Vehicle
-- ---------------------------------------------------------------
CREATE TABLE Vehicle (
    VehicleID INT PRIMARY KEY AUTO_INCREMENT,
    LicensePlate VARCHAR(20) UNIQUE NOT NULL,
    Make VARCHAR(50) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    Color VARCHAR(30),
    DailyRentalRate DECIMAL(10, 2) NOT NULL,
    CurrentMileage INT NOT NULL DEFAULT 0,
    TypeID INT NOT NULL,
    BranchID INT NOT NULL,
    FOREIGN KEY (BranchID) REFERENCES RentalBranch(BranchID),
    FOREIGN KEY (TypeID) REFERENCES VehicleType(TypeID)
);

-- ---------------------------------------------------------------
-- TABLE: MaintenanceStaff
-- ---------------------------------------------------------------
CREATE TABLE MaintenanceStaff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    OfficeNumber VARCHAR(20),
    PhoneNumber VARCHAR(20) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    BranchID INT NOT NULL,
    FOREIGN KEY (BranchID) REFERENCES RentalBranch(BranchID)
);

-- ---------------------------------------------------------------
-- TABLE: RentalAgreement
-- ---------------------------------------------------------------
CREATE TABLE RentalAgreement (
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
    Status VARCHAR(20) NOT NULL DEFAULT 'Booked',
    CHECK (Status IN ('Booked', 'Active', 'Completed', 'Cancelled')),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID),
    FOREIGN KEY (PickupBranchID) REFERENCES RentalBranch(BranchID),
    FOREIGN KEY (ReturnBranchID) REFERENCES RentalBranch(BranchID)
);

-- ---------------------------------------------------------------
-- TABLE: MaintenanceRecord
-- ---------------------------------------------------------------
CREATE TABLE MaintenanceRecord (
    RecordID INT PRIMARY KEY AUTO_INCREMENT,
    DateTimeReported DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    VehicleID INT NOT NULL,
    ReportingCustomerID INT,
    AssignedMaintenanceStaffID INT,
    IssueType VARCHAR(20) NOT NULL,
    Description TEXT NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Reported',
    DateTimeResolved DATETIME,
    Notes TEXT,
    CHECK (IssueType IN ('Routine', 'Urgent')),
    CHECK (Status IN ('Reported', 'In-progress', 'Complete', 'Awaiting Parts')),
    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID),
    FOREIGN KEY (ReportingCustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (AssignedMaintenanceStaffID) REFERENCES MaintenanceStaff(StaffID)
);

-- ---------------------------------------------------------------
-- INDEX: RentalAgreement on CustomerID (required by Part 2)
-- ---------------------------------------------------------------
CREATE INDEX idx_agreement_customer ON RentalAgreement(CustomerID);

-- ---------------------------------------------------------------
-- SAMPLE DATA
-- ---------------------------------------------------------------

INSERT INTO RentalBranch (Name, Address, PhoneNumber) VALUES
('Downtown Branch',    '123 Main St, Miami, FL 33101',       '305-100-1001'),
('Airport Branch',     '456 Airport Rd, Miami, FL 33142',    '305-100-1002'),
('Westside Branch',    '789 West Ave, Miami, FL 33125',      '305-100-1003'),
('Northside Branch',  '321 North Blvd, Miami, FL 33127',    '305-100-1004');

INSERT INTO VehicleType (TypeName) VALUES
('Sedan'), ('SUV'), ('Van'), ('Truck'), ('Convertible');

INSERT INTO Customer (FirstName, LastName, Address, PhoneNumber, Email, DriversLicenseNumber, DriversLicenseExpiryDate) VALUES
('James',    'Carter',   '10 Palm Ave, Miami, FL',       '305-201-1111', 'james.carter@email.com',   'DL-FL-10001', '2027-06-15'),
('Sofia',    'Rivera',   '22 Ocean Dr, Miami Beach, FL', '305-202-2222', 'sofia.rivera@email.com',   'DL-FL-10002', '2026-09-30'),
('Michael',  'Thompson', '5 Coral Way, Coral Gables, FL','305-203-3333', 'michael.t@email.com',      'DL-FL-10003', '2028-01-20'),
('Aisha',    'Patel',    '88 Brickell Ave, Miami, FL',   '305-204-4444', 'aisha.patel@email.com',    'DL-FL-10004', '2026-11-05'),
('Carlos',   'Mendez',   '15 SW 8th St, Miami, FL',      '305-205-5555', 'carlos.m@email.com',       'DL-FL-10005', '2027-03-18');

INSERT INTO MaintenanceStaff (Name, OfficeNumber, PhoneNumber, Email, BranchID) VALUES
('Tony Harris',   'Office-101', '305-300-0001', 'tony.harris@driveeasy.com',   1),
('Linda Brooks',  'Office-102', '305-300-0002', 'linda.brooks@driveeasy.com',  1),
('Ray Nguyen',    'Office-201', '305-300-0003', 'ray.nguyen@driveeasy.com',    2),
('Fatima Diallo', 'Office-301', '305-300-0004', 'fatima.diallo@driveeasy.com', 3),
('Greg Santos',   'Office-401', '305-300-0005', 'greg.santos@driveeasy.com',   4);

INSERT INTO Vehicle (LicensePlate, Make, Model, Year, Color, DailyRentalRate, CurrentMileage, TypeID, BranchID) VALUES
('FL-AAA-001', 'Toyota',  'Camry',      2022, 'Silver',  55.00,  23000, 1, 1),
('FL-AAA-002', 'Honda',   'CR-V',       2023, 'White',   70.00,  15000, 2, 1),
('FL-AAA-003', 'Ford',    'Transit',    2021, 'White',   95.00,  40000, 3, 2),
('FL-AAA-004', 'Chevy',   'Silverado',  2022, 'Black',  110.00,  32000, 4, 2),
('FL-AAA-005', 'BMW',     '3 Series',   2023, 'Blue',    85.00,   8000, 1, 3),
('FL-AAA-006', 'Tesla',   'Model Y',    2024, 'Red',    120.00,   3000, 2, 3),
('FL-AAA-007', 'Nissan',  'Altima',     2021, 'Gray',    50.00,  28000, 1, 4),
('FL-AAA-008', 'Jeep',    'Wrangler',   2022, 'Green',   90.00,  19000, 2, 4),
('FL-AAA-009', 'Dodge',   'Grand Caravan', 2020, 'Silver', 80.00, 55000, 3, 1),
('FL-AAA-010', 'Ford',    'Mustang',    2023, 'Yellow', 130.00,   5000, 5, 2);

INSERT INTO RentalAgreement (CustomerID, VehicleID, PickupBranchID, ReturnBranchID, ScheduledPickupDateTime, ScheduledReturnDateTime, ActualPickupDateTime, ActualReturnDateTime, EstimatedCost, ActualCost, Status) VALUES
(1, 1, 1, 1, '2025-01-10 09:00:00', '2025-01-15 09:00:00', '2025-01-10 09:30:00', '2025-01-15 10:00:00', 275.00, 275.00, 'Completed'),
(1, 5, 3, 1, '2025-03-01 10:00:00', '2025-03-05 10:00:00', '2025-03-01 10:15:00', '2025-03-05 09:45:00', 340.00, 340.00, 'Completed'),
(2, 2, 1, 2, '2025-02-14 08:00:00', '2025-02-18 08:00:00', '2025-02-14 08:30:00', '2025-02-18 08:10:00', 280.00, 280.00, 'Completed'),
(2, 6, 3, 3, '2025-04-10 12:00:00', '2025-04-14 12:00:00', NULL, NULL, 480.00, NULL, 'Booked'),
(3, 3, 2, 2, '2025-03-20 07:00:00', '2025-03-25 07:00:00', '2025-03-20 07:00:00', NULL, 475.00, NULL, 'Active'),
(4, 7, 4, 4, '2025-01-05 11:00:00', '2025-01-08 11:00:00', '2025-01-05 11:20:00', '2025-01-08 11:00:00', 150.00, 150.00, 'Completed'),
(4, 8, 4, 1, '2025-04-20 09:00:00', '2025-04-25 09:00:00', NULL, NULL, 450.00, NULL, 'Booked'),
(5, 4, 2, 3, '2025-02-28 13:00:00', '2025-03-03 13:00:00', '2025-02-28 13:10:00', '2025-03-03 13:30:00', 330.00, 345.00, 'Completed'),
(5, 10, 2, 2, '2025-04-01 08:00:00', '2025-04-03 08:00:00', '2025-04-01 08:00:00', NULL, 260.00, NULL, 'Active'),
(3, 9, 1, 4, '2025-04-15 10:00:00', '2025-04-18 10:00:00', NULL, NULL, 240.00, NULL, 'Cancelled');

INSERT INTO MaintenanceRecord (DateTimeReported, VehicleID, ReportingCustomerID, AssignedMaintenanceStaffID, IssueType, Description, Status, DateTimeResolved, Notes) VALUES
('2025-01-16 10:00:00', 1, 1, 1, 'Routine', 'Oil change after rental return.', 'Complete', '2025-01-17 12:00:00', 'Completed without issues.'),
('2025-02-20 15:30:00', 3, NULL, 3, 'Urgent', 'Engine warning light on during rental.', 'Complete', '2025-02-22 09:00:00', 'Replaced faulty sensor.'),
('2025-03-10 09:00:00', 6, NULL, 4, 'Routine', 'Tire rotation and brake inspection.', 'In-progress', NULL, 'Scheduled for next available slot.'),
('2025-03-25 14:00:00', 8, 4, 2, 'Urgent', 'Customer reported brake noise.', 'Awaiting Parts', NULL, 'Brake pads ordered.'),
('2025-04-02 11:00:00', 10, 5, 5, 'Routine', 'Windshield wiper replacement.', 'Complete', '2025-04-02 13:00:00', 'Replaced both wipers.');