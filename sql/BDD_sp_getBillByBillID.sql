USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_getBillByBillID;

DELIMITER $$
CREATE PROCEDURE sp_getBillByBillID
(
	IN p_bill_id BIGINT
)
BEGIN
	SELECT * FROM tbl_bill WHERE bill_id = p_user_id;
END;
$$
DELIMITER ;
