CREATE TABLE MaintenanceStaff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    office_number VARCHAR(20),
    phone_number VARCHAR(20),
    email VARCHAR(150),
    CONSTRAINT fk_staff_branch
        FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);
