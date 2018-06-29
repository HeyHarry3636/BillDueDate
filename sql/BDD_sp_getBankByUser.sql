USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_getBankByUser;

DELIMITER $$
CREATE PROCEDURE sp_getBankByUser
(
	IN p_user_id BIGINT
)
BEGIN
	SELECT * FROM tbl_bank WHERE user_id = p_user_id;
END;
$$
DELIMITER ;
