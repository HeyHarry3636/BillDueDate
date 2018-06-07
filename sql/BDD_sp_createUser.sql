USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_createUser;

DELIMITER $$
CREATE PROCEDURE sp_createUser
(
	IN p_email VARCHAR(60),
	IN p_password BINARY(60)
)