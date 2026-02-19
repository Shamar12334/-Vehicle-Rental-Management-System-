CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    time DATETIME,
    vehicle INTEGER,
    reporting_customer INTEGER,
    issue_type TEXT CHECK(issue_type IN ('routine', 'urgent')),
    description TEXT,
    status TEXT,
    resolved_date DATE,
    resolved_time DATETIME,
    staff_assigned TEXT,
    notes TEXT
);
