select
 a.program as "Program Name",
 b.frequency as "Center Freq",
 c.modem as "Modem",
 d.mode as "Mode",
 e.frequency as "Radio Frequency",
 f.station as "Station",
 a.active as "Active",
 a.notes as "Notes"
from
 programs a,
 center_data_frequencies b,
 modems c,
 modes d,
 radio_frequencies e,
 radio_stations f
where
 a.center_data_frequency_id=b.id and
 a.modem_id=c.id and
 a.mode_id=d.id and
 a.radio_frequency_id=e.id and
 a.radio_station_id=f.id
;