CREATE TABLE Customer ( 
    CustomerID INT PRIMARY KEY, 
    FirstName VARCHAR(50) NOT NULL, 
    LastName VARCHAR(50) NOT NULL, 
    Address VARCHAR(255) NOT NULL, 
    PhoneNumber VARCHAR(20) NOT NULL, 
    Email VARCHAR(100) UNIQUE NOT NULL, 
    DriversLicenseNumber VARCHAR(50) UNIQUE NOT NULL, 
    DriversLicenseExpiryDate DATE NOT NULL, 
    CHECK (DriversLicenseExpiryDate > CURRENT_DATE) 
);
