CREATE TABLE Vehicle ( 
    VehicleID INT PRIMARY KEY, 
    LicensePlate VARCHAR(20) UNIQUE NOT NULL, 
    Make VARCHAR(50) NOT NULL, 
    Model VARCHAR(50) NOT NULL, 
    Year INT NOT NULL, 
    Color VARCHAR(30), 
    DailyRentalRate DECIMAL(10, 2) NOT NULL, 
    CurrentMileage INT NOT NULL, 
    TypeID INT NOT NULL, 
    BranchID INT NOT NULL, 
    FOREIGN KEY (BranchID) REFERENCES RentalBranch(BranchID), 
    FOREIGN KEY (TypeID) REFERENCES VehicleType(TypeID) 
);
