PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE programs_new(
  Id INT,
  Program TEXT,
  Station TEXT,
  StationFrequency TEXT,
  Modulation TEXT,
  Bandwidth TEXT,
  Modem TEXT,
  CenterFrequency TEXT,
  Active TEXT,
  Notes TEXT
, Day text, Time text);
INSERT INTO programs_new VALUES(2,'Shortwave Radiogram','WINB','9265000','AM','3600','MFSK32','1500','Yes','','Fri','0030');
INSERT INTO programs_new VALUES(3,'Shortwave Radiogram','WRMI','15770000','AM','3600','MFSK32','1500','Yes','','Fri','1300');
INSERT INTO programs_new VALUES(4,'Shortwave Radiogram','WINB','13655000','AM','3600','MFSK32','1500','Yes','','Fri','1500');
INSERT INTO programs_new VALUES(5,'Shortwave Radiogram','WINB','9265000','AM','3600','MFSK32','1500','Yes','','Sat','0330');
INSERT INTO programs_new VALUES(6,'Shortwave Radiogram','WRMI','15770000','AM','3600','MFSK32','1500','Yes','','Sat','1330');
INSERT INTO programs_new VALUES(7,'Shortwave Radiogram','WRMI','5850000','AM','3600','MFSK32','1500','Yes','','Sun','0800');
INSERT INTO programs_new VALUES(8,'Shortwave Radiogram','WRMI','7730000','AM','3600','MFSK32','1500','No','','Sun','0800');
INSERT INTO programs_new VALUES(9,'Shortwave Radiogram','WRMI','7780000','AM','3600','MFSK32','1500','Yes','','Sun','2330');
INSERT INTO programs_new VALUES(10,'Shortwave Radiogram','WRMI','9955000','AM','3600','MFSK32','1500','Yes','','Sat','0100');
INSERT INTO programs_new VALUES(11,'This Is a Music Show','WRMI','5850000','AM','3600','MFSK32','1500','Yes','','Thu','0200');
INSERT INTO programs_new VALUES(12,'Radio Northern Europe International','WRMI','5850000','AM','3600','MFSK32','1500','Yes','','Thu','0100');
INSERT INTO programs_new VALUES(13,'The Mighty KBC','KBC','5960000','AM','3600','MFSK32','1500','Yes','','Sun','0000');
COMMIT;
