-- Creates a table users with constraints on the email column

CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY_KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	);
