-- ====================================================================
-- MySQL script to populate BillDueDate tables with test data
-- ====================================================================

-- Populate USER table
INSERT INTO tbl_user(user_id, user_email, user_password, user_createdDate)
	VALUES(1, "Test@Test.com", "Test", NOW());

-- Populate RECUR table
INSERT INTO tbl_recur(recur_id, recur_interval, recur_value)
	VALUES(1, "Monthly", 30);

-- Populate BANK table
INSERT INTO tbl_bank(bank_id, user_id, bank_currentAmount, bank_payDayAmount, recur_id)
	VALUES(1, 1, 1234.56, 1000.00, 1);

-- Populate BILL table
INSERT INTO tbl_bill(bill_id, user_id, bill_name, bill_description, bill_amount, bill_date, recur_id, bill_createdDate, bill_paid)
	VALUES(1, 1, "Fed Loans", "Income-Based", 199.70, 06/01/2018, 1, NOW(), 1);
INSERT INTO tbl_bill(bill_id, user_id, bill_name, bill_description, bill_amount, bill_date, recur_id, bill_createdDate, bill_paid)
	VALUES(1, 1, "Public Storage", NULL, 118.00, 06/01/2018, 1, NOW(), 1);
INSERT INTO tbl_bill(bill_id, user_id, bill_name, bill_description, bill_amount, bill_date, recur_id, bill_createdDate, bill_paid)
	VALUES(1, 1, "Private Loans", NULL, 484.09, 06/23/2018, 1, NOW(), 0);
