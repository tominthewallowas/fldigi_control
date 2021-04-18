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
