DROP PROCEDURE IF EXISTS aaddCust;

DELIMITER $$

CREATE PROCEDURE assignProj (
    n CHAR(50),
    e CHAR(50)
    )
    COMMENT 'Get next Cust ID and add new customer'
    BEGIN
        IF EXISTS (SELECT custID FROM Cust) THEN
            @id = SELECT MAX(custID)+1 FROM Cust;
            INSERT INTO Cust (custID, name, email)
            VALUES (@id, n, e);
        ELSE 
            INSERT INTO Cust (custID, name, email)
            VALUES (@id, n, e);
            ;
    END $$
DELIMITER ;