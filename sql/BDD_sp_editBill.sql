USE BillDueDate;

DROP PROCEDURE IF EXISTS sp_editBill;

DELIMITER $$
CREATE PROCEDURE sp_editBill
(
  IN p_bill_id BIGINT,
	IN p_user_id BIGINT,
	IN p_bill_name VARCHAR(45),
	IN p_bill_description VARCHAR(200),
	IN p_bill_amount DECIMAL(7,2),
	IN p_bill_autoWithdrawal CHAR(1),
	IN p_bill_date DATE,
	IN p_recur_id BIGINT
)
BEGIN
	UPDATE tbl_bill
  SET
		user_id = p_user_id,
		bill_name = p_bill_name,
		bill_description = p_bill_description,
		bill_amount = p_bill_amount,
		bill_autoWithdrawal = p_bill_autoWithdrawal,
		bill_date = p_bill_date,
		recur_id = p_recur_id
  WHERE bill_id = p_bill_id;
END;
$$
DELIMITER ;
