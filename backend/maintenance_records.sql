CREATE TABLE MaintenanceRecord ( 
    RecordID INT PRIMARY KEY, 
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
);

