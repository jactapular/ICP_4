SELECT 
	unitID 'Unit ID', 
    DATE_SUB(dt, INTERVAL 3 HOUR) AS 'Date Time',  
    TIMEDIFF(NOW(), DATE_SUB(dt, INTERVAL 3 HOUR)) AS 'Age',
    ProjID AS 'Proj ID',    
    valOne AS 'Temperature', 
    valTwo AS 'Light' 
FROM Reading 
WHERE projID = 2 
    AND TIMEDIFF(NOW(), DATE_SUB(dt, INTERVAL 3 HOUR)) < '00:05:00'
ORDER BY dt;