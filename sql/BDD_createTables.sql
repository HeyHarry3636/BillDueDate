-- ====================================================================
-- MySQL script to create BillDueDate tables
-- ====================================================================

USE BillDueDate

-- Credentials for Test USER
-- U: test
-- P: Test1234!

-- DROP all tables from previous uses
DROP TABLE IF EXISTS tbl_bill;
DROP TABLE IF EXISTS tbl_bank;
DROP TABLE IF EXISTS tbl_recur;
DROP TABLE IF EXISTS tbl_user;

-- Create the USER table
CREATE TABLE tbl_user (
	user_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	user_email VARCHAR(60) NOT NULL,
	user_password BINARY(60) NOT NULL,
	user_createdDate DATETIME DEFAULT NULL,
	PRIMARY KEY (user_id)
);

-- Create the RECUR table
CREATE TABLE tbl_recur (
	recur_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	recur_interval VARCHAR(45) NULL,
	recur_value BIGINT NULL,
	PRIMARY KEY (recur_id)
);

-- Create the BANK table
CREATE TABLE tbl_bank (
	bank_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	user_id BIGINT NOT NULL,
	bank_currentAmount DECIMAL(8,2) NULL,
	bank_payDayAmount DECIMAL(7,2) NULL,
	recur_id BIGINT NOT NULL,
	PRIMARY KEY (bank_id),
	FOREIGN KEY (user_id) REFERENCES tbl_user(user_id),
	FOREIGN KEY (recur_id) REFERENCES tbl_recur(recur_id)
);

-- Create the BILL table
CREATE TABLE tbl_bill (
	bill_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	user_id BIGINT NOT NULL,
	bill_name VARCHAR(45) NULL,
	bill_description VARCHAR(200) NULL,
	bill_amount DECIMAL(7,2) NULL,
	bill_autoWithdrawal CHAR(1) NULL,
	bill_date DATE DEFAULT NULL,
	recur_id BIGINT NOT NULL,
	bill_createdDate DATETIME DEFAULT NULL,
	bill_paid CHAR(1) NULL,
	PRIMARY KEY (bill_id),
	FOREIGN KEY (user_id) REFERENCES tbl_user(user_id),
	FOREIGN KEY (recur_id) REFERENCES tbl_recur(recur_id)
);