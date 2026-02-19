CREATE TABLE records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    time DATETIME,
    vehicle INT,
    reporting_customer INT,
    issue_type ENUM('routine', 'urgent'),
    description TEXT,
    status VARCHAR(50),
    resolved_date DATE,
    resolved_time DATETIME,
    staff_assigned INT,
    notes TEXT
);
