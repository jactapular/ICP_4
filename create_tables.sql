DROP TABLE IF EXISTS UnitType;
CREATE TABLE UnitType (
    typeID CHAR(3),
    atributes CHAR(200),
    PRIMARY KEY (typeID)
);

DROP TABLE IF EXISTS Unit;
CREATE TABLE Unit (
   unitID CHAR(3),
   typeID CHAR(3),
   PRIMARY KEY (unitID),
   FOREIGN KEY (typeID) REFERENCES UnitType(typeID)
);

DROP TABLE IF EXISTS Cust;
CREATE TABLE Cust (
    custID CHAR(3),
    name CHAR(50) NOT NULL,
    email CHAR(50) NOT NULL,
    PRIMARY KEY (custID)
);

DROP TABLE IF EXISTS Proj;
CREATE TABLE Proj (
    custID CHAR(3),
    projID CHAR(3),
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
    unitID CHAR(3),
    dt CHAR(3),
    projID CHAR(3),
    PRIMARY KEY (unitID,dt),
    FOREIGN KEY (projID) REFERENCES Proj(projID),
    FOREIGN KEY (unitID) REFERENCES Unit(unitID)
);

DROP TABLE IF EXISTS ValOne;
CREATE TABLE ValOne (
    unitID CHAR(3),
    dt CHAR(3),
    val DECIMAL(3,2) NOT NULL,
    PRIMARY KEY (unitID,dt),
    FOREIGN KEY (unitID) REFERENCES Unit(unitID),
    FOREIGN KEY (dt) REFERENCES Reading(dt)     
);