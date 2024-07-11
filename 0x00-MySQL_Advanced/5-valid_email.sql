-- Create a trigger to reset valid_email when email is changed
-- This trigger ensures email validation status is updated when email changes

DELIMITER //

CREATE TRIGGER email_validation
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END //

DELIMITER ;
