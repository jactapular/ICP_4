DROP PROCEDURE IF EXISTS addCust;
DELIMITER $$
CREATE PROCEDURE addCust(
    n CHAR(50),
    e CHAR(50)
    )
    COMMENT 'Get next Cust ID and add new customer'
    BEGIN
        DECLARE c INT(5);
        SET c = (SELECT COUNT(*) FROM Cust);
        IF (c > 0 && c < 10000) THEN 
            SET @id = (SELECT (MAX(custID)+1) FROM Cust);
            INSERT INTO Cust (custID, name, email)
            VALUES (@id, n, e);
        ELSE IF (c == 0)
            INSERT INTO Cust (custID, name, email) VALUES (0001, n, e); 
        ELSE 
            SELECT 'customer table exceeds limit of 9999 entries'
        END IF;
    END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS test;
DELIMITER $$
CREATE PROCEDURE test()
    COMMENT 'Test a single line select statement proc'
    BEGIN
        SELECT 'test';
    END $$
DELIMITER ;

