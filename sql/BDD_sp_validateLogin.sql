USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_validateLogin;

DELIMITER $$
CREATE PROCEDURE sp_validateLogin
(
	IN p_email VARCHAR(60)
)
BEGIN
	SELECT * FROM tbl_user WHERE user_email = p_email;
END;
$$
DELIMITER ;