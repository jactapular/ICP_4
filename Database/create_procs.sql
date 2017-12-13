##PROCEDURES TO HANDLE SAFE DATABASE MANIPULATION - to be called by front end

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
        IF NOT EXISTS (SELECT email FROM Cust WHERE email = e) THEN
            IF (c > 0 && c < 10000) THEN 
                SET @id = (SELECT (MAX(custID)+1) FROM Cust);
                INSERT INTO Cust (custID, name, email)
                VALUES (@id, n, e);
            ELSEIF (c = 0) THEN
                INSERT INTO Cust (custID, name, email) VALUES (0001, n, e); 
            ELSEIF (c > 9999) THEN
                SELECT 'customer table exceeds limit of 9999 entries';
            END IF;
        ELSE
            SELECT 'customer email already exists' AS Error, e AS Email;
        END IF;
    END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS addProj;
DELIMITER $$
CREATE PROCEDURE addProj(
    n CHAR(50),
    i CHAR(50)
    )
    COMMENT 'Get next Proj ID and add new proj'
    BEGIN
        DECLARE c INT(5);
        IF EXISTS (SELECT custID FROM Cust WHERE custID = i) THEN
            SET c = (SELECT COUNT(*) FROM Proj);
            IF (c > 0 && c < 10000) THEN 
                SET @id = (SELECT (MAX(projID)+1) FROM Proj);
                INSERT INTO Proj (custID, projID, projName) 
                VALUES (i, @id, n);
            ELSEIF (c = 0) THEN
                INSERT INTO Proj (custID, projID, projName) 
                VALUES (i, 0001, n); 
            ELSE 
                SELECT 'project table exceeds limit of 9999 entries';
            END IF;
        END IF;
    END $$
DELIMITER ;
/*
DROP PROCEDURE IF EXISTS addUnit;
DELIMITER $$
CREATE PROCEDURE addUnit(
    n CHAR(50),
    i CHAR(50)
    )
    COMMENT 'Get next Proj ID and add new proj'
    BEGIN
        DECLARE c INT(5);
        IF EXISTS (SELECT custID FROM Cust WHERE custID = i) THEN
            SET c = (SELECT COUNT(*) FROM Proj);
            IF (c > 0 && c < 10000) THEN 
                SET @id = (SELECT (MAX(projID)+1) FROM Proj);
                INSERT INTO Proj (custID, projID, projName) 
                VALUES (i, @id, n);
            ELSEIF (c = 0) THEN
                INSERT INTO Proj (custID, projID, projName) 
                VALUES (i, 0001, n); 
            ELSE 
                SELECT 'project table exceeds limit of 9999 entries';
            END IF;
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
*/
