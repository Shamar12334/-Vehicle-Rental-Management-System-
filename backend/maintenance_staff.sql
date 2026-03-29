CREATE TABLE MaintenanceStaff ( 
    StaffID INT PRIMARY KEY, 
    Name VARCHAR(100) NOT NULL, 
    OfficeNumber VARCHAR(20), 
    PhoneNumber VARCHAR(20) NOT NULL, 
    Email VARCHAR(100) UNIQUE, 
    BranchID INT NOT NULL, 
    FOREIGN KEY (BranchID) REFERENCES RentalBranch(BranchID) 
);

