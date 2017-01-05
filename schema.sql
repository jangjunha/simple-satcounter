CREATE TABLE comments (
        id INTEGER PRIMARY KEY,
        writer TEXT NOT NULL,
        content TEXT NOT NULL,
	created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

