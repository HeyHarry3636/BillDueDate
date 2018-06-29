USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_getBankByBankID;

DELIMITER $$
CREATE PROCEDURE sp_getBankByBankID
(
	IN p_bank_id BIGINT
)
BEGIN
	SELECT * FROM tbl_bank WHERE bank_id = p_bank_id;
END;
$$
DELIMITER ;
