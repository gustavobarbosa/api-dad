PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE appliances(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
name VARCHAR(100) NOT NULL,
description VARCHAR(300) NOT NULL,
photo_url VARCHAR(255) NOT NULL,
voltage VARCHAR(6) NOT NULL,
power_in_use INTEGER NOT NULL,
power_in_standby INTEGER
);
INSERT INTO appliances VALUES(1,'Microondas','Microondas LG Prata','https://www.dasdas.com/example.jpeg','110v',500,100);
INSERT INTO appliances VALUES(2,'Geladeira','Brastemp 200L','https://www.dasdas.com/example.jpeg','110v',500,100);
INSERT INTO appliances VALUES(3,'Cafeteira','Nespresso Inissia Branca','https://www.dasdas.com/example.jpeg','Bivolt',1500,50);
INSERT INTO appliances VALUES(4,'Ar Condicionado','Ar Condicionado Splitter Springer','https://www.dasdas.com/example.jpeg','220v',5000,100);
INSERT INTO appliances VALUES(5,'Monitor 25','Monitor LG Ultrawide','https://www.dasdas.com/example.jpeg','110v',500,100);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('appliances',5);
