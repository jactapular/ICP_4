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
            IF (c > 0 && c < 9999) THEN 
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
#TODO: if name exists deny
        IF EXISTS (SELECT custID FROM Cust WHERE custID = i) THEN
            SET c = (SELECT COUNT(*) FROM Proj);
            IF (c > 0 && c < 9999) THEN 
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

DROP PROCEDURE IF EXISTS addUnitType;
DELIMITER $$
CREATE PROCEDURE addUnitType(
    a CHAR(200)
    )
    COMMENT 'Get next UnitTypeID and add new unitType'
    BEGIN
        DECLARE c INT(5);
        SET c = (SELECT COUNT(*) FROM UnitType);
        IF (c > 0 && c < 9999) THEN 
            SET @id = (SELECT (MAX(typeID)+1) FROM UnitType);
            INSERT INTO UnitType(typeID, attributes) 
            VALUES (@id, a);
        ELSEIF (c = 0) THEN
            INSERT INTO UnitType(typeID, attributes) 
            VALUES (0001, a); 
        ELSE
            SELECT 'UnitType table exceeds limit of 9999 entries';
        END IF;
    END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS addUnit;
DELIMITER $$
CREATE PROCEDURE addUnit(
    t INT(4),
    i CHAR(10)
    )
    COMMENT 'Get next UnitID and add new unit'
    BEGIN
        DECLARE c INT(5);
        IF EXISTS (SELECT typeID FROM UnitType WHERE typeID = t) THEN
            INSERT INTO Unit(unitID, typeID) 
            VALUES (i, t); 
        ELSE
            SELECT 'unit type does not exist' AS Error, t AS typeID;
        END IF;
    END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS addLoc;
DELIMITER $$
CREATE PROCEDURE addLoc(
    m INT(4)
    )
    COMMENT 'create new location ID, other vals are NULL'
    BEGIN
        DECLARE c INT(5);
        IF EXISTS (SELECT matID FROM Mat WHERE matID = m) THEN
            SET c = (SELECT COUNT(*) FROM Loc);
            IF (c > 0 && c < 9999) THEN 
                SET @id = (SELECT (MAX(locID)+1) FROM Loc);
                INSERT INTO Loc (locID) 
                VALUES (@id);
            ELSEIF (c = 0) THEN
                INSERT INTO Loc (locID) 
                VALUES (0001); 
            ELSE 
                SELECT 'project table exceeds limit of 9999 entries';
            END IF;
        END IF;
    END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS addMat;
DELIMITER $$
CREATE PROCEDURE addMat(
    d CHAR(200)
    )
    COMMENT 'create new Material ID, details recorded in comment'
    BEGIN
        DECLARE c INT(5);
        SET c = (SELECT COUNT(*) FROM Mat);
        IF (c > 0 && c < 9999) THEN 
            SET @id = (SELECT (MAX(matID)+1) FROM Mat);
            INSERT INTO Mat(matID, descr) 
            VALUES (@id, d);
        ELSEIF (c = 0) THEN
            INSERT INTO Mat(matID, descr) 
            VALUES (0001, d); 
        ELSE
            SELECT 'Unit table exceeds limit of 9999 entries';
        END IF;
    END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS addRead;
DELIMITER $$
CREATE PROCEDURE addRead(
    u VARCHAR(100),       #unit ID
    dt DATETIME,    #timestamp of recording time
    p INT(4),       #project ID
    l INT(4),        #location ID
    a FLOAT, #sensor 1 value....
    b FLOAT,
    c FLOAT,
    d FLOAT,
    e FLOAT,
    f FLOAT
    ) #...sensor 6 value
    COMMENT 'add a new reading to the Reading table, comes from LoRa Server'
    BEGIN 
        IF EXISTS (SELECT unitID FROM Unit WHERE unitID = u) &&
        EXISTS (SELECT projID FROM Proj WHERE projID = p) &&
        EXISTS (SELECT locID FROM Loc WHERE locID = l) THEN
            INSERT INTO Reading VALUES(u, dt, p, l, a, b, c, d, e, f);
        ELSE
            SELECT 'ID does not exist, review table entries and try again';
        END IF;
    END$$
DELIMITER ;

