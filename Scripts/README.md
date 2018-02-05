Script to listen for new packets from sensors on LoRaWAN gateway and forward to mysql database.

*Files*
-config.ini: config file for DB access
-python_mysql_dbconfig.py: helper script to access DB
-transfer.py: transfers appropriate packets to DB

*requires:*
  sudo apt-get install python-configparser
  python3

-pip install mysql-connector-python
http://www.mysqltutorial.org/python-connecting-mysql-databases/
-http://www.mysqltutorial.org/python-mysql-insert/

* LoRaWan Gateway example:*
https://l.messenger.com/l.php?u=http%3A%2F%2Fcpham.perso.univ-pau.fr%2FLORA%2FRPIgateway.html&h=ATMsiQTd0bXfXnC9xiGh-MpGxlnFjFiDBbRdVQSWXfkMTuJnFwdEhj_R5yaoMMClouN3ePBRpRfe1t9OPQVvtfnPKP7nIIa0GlhvvzxYwQbOOlpntY2ot70TFS_Qgf-uv4M