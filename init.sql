DROP TABLE IF EXISTS metro_stations;
DROP TABLE IF EXISTS metro_lines;
DROP TABLE IF EXISTS cities;

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    UNIQUE (name)
);

CREATE TABLE metro_lines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    hex_color VARCHAR(7),
    UNIQUE (name)
);

CREATE TABLE metro_stations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    lat VARCHAR(20),
    lon VARCHAR(20),
    location GEOGRAPHY(POINT,4326),
    city INTEGER REFERENCES cities (id),
    line INTEGER REFERENCES metro_lines (id),
    station_order INTEGER
  );
