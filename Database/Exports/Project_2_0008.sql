SELECT 
	unitID 'Unit ID', 
    DATE_SUB(dt, INTERVAL 3 HOUR) AS 'Date Time', 
    ProjID AS 'Proj ID', 
    valOne AS 'Temperature', 
    valTwo AS 'Light' 
FROM Reading 
WHERE projID = 2 
	AND unitID = "0x00540008";
