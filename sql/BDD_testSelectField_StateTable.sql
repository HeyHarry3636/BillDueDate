USE BillDueDate;

-- Credentials for Test USER
-- U: test
-- P: Test1234!

-- DROP all tables from previous uses
DROP TABLE IF EXISTS City;

-- Create the Cities table
CREATE TABLE City (
	id BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	state VARCHAR(2) NOT NULL,
	name VARCHAR(50) NOT NULL,
	PRIMARY KEY (id)
);

INSERT INTO city(id, state, name)
	VALUES(1, "NV", "Las Vegas");
INSERT INTO city(id, state, name)
	VALUES(2, "NV", "Reno");
INSERT INTO city(id, state, name)
  VALUES(3, "CA", "Los Angeles");
INSERT INTO city(id, state, name)
	VALUES(4, "CA", "San Diego");
