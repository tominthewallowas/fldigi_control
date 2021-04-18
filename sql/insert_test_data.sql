#center_data_frequencies
insert into center_data_frequencies (frequency) values
('1000'),
('1500'),
('2000')
;

#modems
insert into modems (modem) values
('MFSK32'),
('MSFK64'),
('THOR')
;

#modes
insert into modes (mode) values
('AM'),
('LSB'),
('USB')
;

#radio_frequencies
insert into radio_frequencies (
  id,
  frequency
) values
(25,'9265'),
(48,'15770'),
(3,'5850')
;

#radio_stations
insert into radio_stations (station) values
('WINB'),
('WRMI'),
('KBC')
;

#bandwidths
insert into bandwidths (bandwidth) values
('4000'),
('2000'),
('800')
;

#programs
insert into programs (
  program,
  center_data_frequency_id,
  modem_id,
  mode_id,
  radio_frequency_id,
  radio_station_id,
  bandwidth_id,
  notes
) values
('program 1', 1, 1, 1, 25, 1, 1, 'Note 1'),
('program 2', 2, 2, 2, 48, 2, 2, 'Note 2'),
('program 3', 3, 3, 3, 3, 3, 3, 'Note 3');
