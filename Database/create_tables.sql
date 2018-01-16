DROP TABLE IF EXISTS UnitType;
CREATE TABLE UnitType (
    typeID      INT(4),
    attributes   CHAR(200),
    PRIMARY KEY (typeID)
);

DROP TABLE IF EXISTS Unit;
CREATE TABLE Unit (
   unitID VARCHAR(10),
   typeID INT(4),
   PRIMARY KEY (unitID),
   FOREIGN KEY (typeID) REFERENCES UnitType(typeID)
);

DROP TABLE IF EXISTS Cust;
CREATE TABLE Cust (
    custID  INT(4),
    name    CHAR(50) NOT NULL,
    email   CHAR(50) NOT NULL,
    PRIMARY KEY (custID)
);

DROP TABLE IF EXISTS Proj;
CREATE TABLE Proj (
    custID INT(4),
    projID INT(4),
    projName CHAR(200) NOT NULL,
    PRIMARY KEY (projID),
    FOREIGN KEY (custID) REFERENCES Cust(custID)
);

DROP TABLE IF EXISTS Mat;
CREATE TABLE Mat (
    matID       INT(4),
    descr       CHAR(200),
    PRIMARY KEY (matID)
);

DROP TABLE IF EXISTS Loc;
CREATE TABLE Loc (
    locID       INT(4),
    matID       INT(4),
    east        DECIMAL(6,2),
    north       DECIMAL(6,2),
    rl          DECIMAL(4,2),
    treeCover   DECIMAL(2,2),
    comment     CHAR(200),
    PRIMARY KEY (locID),
    FOREIGN KEY (matID) REFERENCES Mat(matID)
);


DROP TABLE IF EXISTS Reading;
CREATE TABLE Reading(
    unitID      VARCHAR(100),
    dt          DATETIME,
    projID      INT(4),
    locID       INT(4),
    valOne      DECIMAL(3,2),
    valTwo      DECIMAL(3,2),
    valThree    DECIMAL(3,2),
    valFour     DECIMAL(3,2),
    valFive     DECIMAL(3,2),
    valSix      DECIMAL(3,2),        
    PRIMARY KEY (unitID,dt),
    FOREIGN KEY (projID) REFERENCES Proj(projID),
    FOREIGN KEY (unitID) REFERENCES Unit(unitID),
    FOREIGN KEY (locID) REFERENCES Loc(locID)
);

-- DROP TABLE IF EXISTS ValOne;
-- CREATE TABLE ValOne (
--     unitID CHAR(3),
--     dt CHAR(3),
--     val DECIMAL(3,2) NOT NULL,
--     PRIMARY KEY (unitID,),
--     FOREIGN KEY (unitID) REFERENCES Unit(unitID),
--     FOREIGN KEY (dt) REFERENCES Reading(dt)     
-- );
