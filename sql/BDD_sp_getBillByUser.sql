USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_getBillByUser;

DELIMITER $$
CREATE PROCEDURE sp_getBillByUser
(
	IN p_user_id BIGINT
)
BEGIN
	SELECT * FROM tbl_bill WHERE user_id = p_user_id;
END;
$$
DELIMITER ;