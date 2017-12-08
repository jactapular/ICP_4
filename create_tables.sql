DROP TABLE IF EXISTS UnitType;
CREATE TABLE UnitType (
    typeID CHAR(3),
    atributes CHAR(200),
    PRIMARY KEY (typeID)
);

DROP TABLE IF EXISTS Unit;
CREATE TABLE Unit (
   unitID CHAR(3)
   typeID CHAR(3),
   PRIMARY KEY (unitID),
   FOREIGN KEY (typeID) REFERENCES UnitType(typeID)
);

DROP TABLE IF EXISTS Proj;
CREATE TABLE Proj (
    projID CHAR(3),
    PRIMARY KEY (projID),
    FOREIGN KEY (custID) REFERENCES Cust(custID)
);

DROP TABLE IF EXISTS Cust;
CREATE TABLE Cust (
    custID CHAR(3),
    name CHAR(50) NOT NULL,
    email CHAR(50) NOT NULL,
    PRIMARY KEY (custID)
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

DROP TABLE IF EXISTS Read;
CREATE TABLE Read(
    unitID CHAR(3),
    dt DATETIME,
    projID CHAR(3),
    PRIMARY KEY (unitID,dt),
    FOREIGN KEY (projID) REFERENCES Proj(projID),
    FOREIGN KEY (unitID) REFERENCES Unit(unitID)
);

DROP TABLE IF EXISTS ValOne;
CREATE TABLE ValOne (
    unitID CHAR(3),
    dt DATETIME,
    val DECIMAL(3,2) NOT NULL,
    PRIMAY KEY (unitID,dt),
    FOREIGN KEY (unitID, dt) REFERENCES Unit(unitID, dt),

);