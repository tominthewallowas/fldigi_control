create table if not exists center_data_frequencies (
  id integer primary key,
  frequency text unique not null
);

create table if not exists modems (
  id integer primary key,
  modem text unique not null
);

create table if not exists modes (
  id integer primary key,
  mode text unique not null
);

create table if not exists radio_frequencies (
  id integer primary key,
  frequency text unique not null
);

create table if not exists radio_stations (
  id integer primary key,
  station text unique not null
);

create table if not exists bandwidths (
  id integer primary key,
  bandwidth text unique not null
);

create table if not exists programs (
id integer primary key,
program text unique,
center_data_frequency_id integer,
modem_id integer,
mode_id integer,
radio_frequency_id integer,
radio_station_id integer,
bandwidth_id integer,
active text default "Yes",
notes text,
foreign key (center_data_frequency_id) references center_data_frequencies(id)
foreign key (modem_id) references modems (id)
foreign key (mode_id) references modes (id)
foreign key (radio_frequency_id) references radio_frequencies (id)
foreign key (radio_station_id) references radio_stations (id),
foreign key (bandwidth_id) references bandwidths (id)
);

