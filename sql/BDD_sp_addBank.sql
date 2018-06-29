USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_addBank;

DELIMITER $$
CREATE PROCEDURE sp_addBank
(
	IN p_user_id BIGINT,
	IN p_bank_currentAmount DECIMAL(8,2),
	IN p_bank_payDayAmount DECIMAL(7,2),
	IN p_recur_id BIGINT
)
BEGIN
	INSERT INTO tbl_bank
	(
		user_id,
		bank_currentAmount,
		bank_payDayAmount,
		recur_id,
		bank_createdDate
	)
	VALUES
	(
		p_user_id,
		p_bank_currentAmount,
		p_bank_payDayAmount,
		p_recur_id,
		NOW()
	);
END;
$$
DELIMITER ;
