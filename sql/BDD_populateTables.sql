-- ====================================================================
-- MySQL script to populate BillDueDate tables with test data
-- ====================================================================

-- Populate USER table
INSERT INTO tbl_user(user_id, user_email, user_password, user_createdDate)
	VALUES(1, "Test@Test.com", "Test", NOW());

