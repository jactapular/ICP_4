DROP TABLE IF EXISTS UnitType;
CREATE TABLE UnitType (
    typeID      INT(4),
    atributes   CHAR(200),
    PRIMARY KEY (typeID)
);

DROP TABLE IF EXISTS Unit;
CREATE TABLE Unit (
   unitID INT(4),
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
    PRIMARY KEY (projID),
    FOREIGN KEY (custID) REFERENCES Cust(custID)
);

-- DROP TABLE IF EXISTS Loc;
-- CREATE TABLE Loc (
--     locID
--     east
--     north
--     rl
--     treeCover
--     grouCover
--     matType
-- )


DROP TABLE IF EXISTS Reading;
CREATE TABLE Reading(
    unitID      INT(4),
    dt          DATETIME,
    projID      INT(4),
    valOne      DECIMAL(3,2),
    valTwo      DECIMAL(3,2),
    valThree    DECIMAL(3,2),
    valFour     DECIMAL(3,2),
    valFive     DECIMAL(3,2),
    valSix      DECIMAL(3,2),        
    PRIMARY KEY (unitID,dt),
    FOREIGN KEY (projID) REFERENCES Proj(projID),
    FOREIGN KEY (unitID) REFERENCES Unit(unitID)
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