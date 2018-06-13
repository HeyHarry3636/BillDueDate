USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_addBill;

DELIMITER $$
CREATE PROCEDURE sp_addBill
(
	IN p_user_id BIGINT,
	IN p_bill_name VARCHAR(45),
	IN p_bill_description VARCHAR(200),
	IN p_bill_amount DECIMAL(7,2),
	IN p_bill_autoWithdrawal CHAR(1),
	IN p_bill_date DATE,
	IN p_recur_id BIGINT
)
BEGIN
	INSERT INTO tbl_bill
	(
		user_id,
		bill_name,
		bill_description,
		bill_amount,
		bill_autoWithdrawal,
		bill_date,
		recur_id,
		bill_createdDate,
		bill_paid
	)
	VALUES
	(
		p_user_id,
		p_bill_name,
		p_bill_description,
		p_bill_amount,
		p_bill_autoWithdrawal,
		p_bill_date,
		p_recur_id,
		NOW(),
		'N'
	);
END;
$$
DELIMITER ;