USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_deleteBillByBillID;

DELIMITER $$
CREATE PROCEDURE sp_deleteBillByBillID
(
	IN p_bill_id BIGINT
)
BEGIN
	DELETE FROM tbl_bill WHERE bill_id = p_bill_id;
END;
$$
DELIMITER ;
