CREATE TABLE programs (
        Id integer primary key,
        Program Text default "",
        Station Text default "",
        StationFrequency Text default "",
        Modulation Text default "",
        Bandwidth Text default "",
        Modem Text default "",
        CenterFrequency Text default "",
        Active Text default "Y",
        Notes Text default ""
 );
INSERT INTO programs VALUES(1,'TIAMS_THU_0200_WRMI','WRMI','5850000','AM','3600','MFSK32','1500','Yes','This is a Music Show runs on Thursday at 0200UTC on WRMI at 5850 kHz.');
INSERT INTO programs VALUES(2,'SWRG_FRI_0030_WINB','WINB','9265000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(3,'SWRG_FRI_1300_WRMI','WRMI','15770000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(4,'SWRG_FRI_1500_WINB','WINB','13655000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(5,'SWRG_SAT_0330_WINB','WINB','9265000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(6,'SWRG_SAT_1330_WRMI','WRMI','15770000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(7,'SWRG_SUN_0800_WRMI','WRMI','5850000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(8,'SWRG_SUN_0800_WRMI','WRMI','7730000','AM','3600','MFSK32','1500','No','');
INSERT INTO programs VALUES(9,'SWRG_SUN_2330_WRMI','WRMI','7780000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(10,'SWRG_SAT_0100_WRMI','WRMI','9955000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(11,'TIAMS_THU_0200_WRMI','WRMI','5850000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(12,'RNEI_THU_0100_WRMI','WRMI','5850000','AM','3600','MFSK32','1500','Yes','');
INSERT INTO programs VALUES(13,'KBC_SUN_0000_KBC','KBC','5960000','AM','3600','MFSK32','1500','Yes','');

create table programs_new as select Id, Program, Station, StationFrequency, Modulation, Bandwidth, Modem, CenterFrequency, Active, Notes from programs;
