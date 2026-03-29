CREATE TABLE RentalAgreement ( 
    AgreementID INT PRIMARY KEY, 
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
);
