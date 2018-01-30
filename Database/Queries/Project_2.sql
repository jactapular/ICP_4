SELECT 
	unitID 'Unit ID', 
    dt AS 'Date Time', 
    ProjID AS 'Proj ID', 
    valOne AS 'Temperature', 
    valTwo AS 'Light' 
FROM Reading 
WHERE projID = 2;
