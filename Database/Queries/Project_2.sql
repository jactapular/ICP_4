SELECT 
	unitID 'UnitID', 
    dt AS 'Time', 
    valOne AS 'Temp', 
    valTwo AS 'Light' 
FROM Reading 
WHERE projID = 2;
