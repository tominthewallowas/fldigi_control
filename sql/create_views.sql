drop view programs_vw;

CREATE VIEW IF NOT EXISTS programs_vw
AS
select
 a.id as id,
 a.program as program,
 f.station as station,
 e.frequency as radiofrequency,
 d.mode as mode,
 c.modem as modem,
 b.frequency as centerfreq,
 g.bandwidth as bandwidth,
 a.active as active,
 a.notes as notes
from
 programs a,
 center_data_frequencies b,
 modems c,
 modes d,
 radio_frequencies e,
 radio_stations f,
 bandwidths g
where
 a.center_data_frequency_id=b.id and
 a.modem_id=c.id and
 a.mode_id=d.id and
 a.radio_frequency_id=e.id and
 a.radio_station_id=f.id and
 a.bandwidth_id=g.id
;
