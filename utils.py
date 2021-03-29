from psycopg2 import sql


def get_or_create_city(cur, city_name) -> int:
    """
    :param cur: psycopg2 cursor
    :param city_name: City name
    :type city_name: str
    """
    created = False
    get_one = sql.SQL("SELECT * FROM cities WHERE name = {city};").format(
        city=sql.Literal(city_name),
    )
    cur.execute(get_one)
    if cur.fetchone() is None:
        insert = sql.SQL("INSERT INTO cities (name) values ({city});").format(
            city=sql.Literal(city_name)
        )
        cur.execute(insert)
        created = True
    cur.execute(get_one)
    return created, cur.fetchone()[0]


def get_or_create_metro_line(cur, line, color) -> int:
    """
    :param cur: psycopg2 cursor
    :param line: Line name
    :param color: Line hex color
    :type line: str
    :type color: str
    """
    created = False
    get_one = sql.SQL("SELECT * FROM metro_lines WHERE name = {line_name};").format(
        line_name=sql.Literal(line),
    )
    cur.execute(get_one)
    if cur.fetchone() is None:
        insert = sql.SQL("INSERT INTO metro_lines (name, hex_color) values ({line_name}, {line_hex_color});").format(
            line_name=sql.Literal(line),
            line_hex_color=sql.Literal(color)
        )
        cur.execute(insert)
        created = True
    cur.execute(get_one)
    return created, cur.fetchone()[0]


def get_or_create_subway_station(cur, station, city_id, line_id) -> int:
    """
    :param cur: psycopg2 cursor
    :param station: Station data dict
    :param city_id: City id
    :param line_id: Line id
    :type station: dict
    :type city_id: int
    :type line_id: int
    """
    created = False
    get_one = sql.SQL("SELECT * FROM metro_stations WHERE name = {line_name} AND city = {city};").format(
        line_name=sql.Literal(station['name']),
        city=sql.Literal(city_id),
    )
    cur.execute(get_one)
    if cur.fetchone() is None:
        insert = sql.SQL("INSERT INTO metro_stations (name, lat, lon, location, city, line, station_order) "
                         "values ({station_name}, {lat}, {lon}, 'POINT( {lat} {lon})', "
                         "{city_id}, {line_id}, {station_order});").format(
            station_name=sql.Literal(station['name']),
            lat=sql.Literal(station['lat']),
            lon=sql.Literal(station['lng']),
            city_id=sql.Literal(city_id),
            line_id=sql.Literal(line_id),
            station_order=sql.Literal(station['order'])
        )
        cur.execute(insert)
        created = True
    cur.execute(get_one)
    return created, cur.fetchone()[0]
