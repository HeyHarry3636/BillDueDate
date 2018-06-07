USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_createUser;

DELIMITER $$
CREATE PROCEDURE sp_createUser
(
	IN p_email VARCHAR(60),
	IN p_password BINARY(60)
)
BEGIN
	IF (SELECT EXISTS (SELECT 1 FROM tbl_user WHERE user_email = p_email)) THEN
		SELECT 'Email has already been registered!';
	ELSE
		INSERT INTO tbl_user
		(
			user_email,
			user_password,
			user_createdDate
		)
		VALUES
		(
			p_email,
			p_password,
			NOW()
		);
	END IF;
END;
$$
DELIMITER ;