import mysql.connector


def connect(host="localhost", database="weatherdb", user="weather", passwd="weather"):
    db_connection = mysql.connector.connect(
        host=host, database=database, user=user, passwd=passwd
    )
    return db_connection


def create_table(con):
    sql = """
        CREATE TABLE IF NOT EXISTS weatherdb.weather (
            weather_description TEXT NOT NULL,
            temp FLOAT NOT NULL,
            temp_feels_like FLOAT NOT NULL,
            temp_min FLOAT NOT NULL,
            temp_max FLOAT NOT NULL,
            pressure SMALLINT NOT NULL,
            humidity SMALLINT NOT NULL,
            visibility SMALLINT NOT NULL,
            wind_speed FLOAT NOT NULL,
            wind_deg SMALLINT NOT NULL,
            datetime DATETIME NOT NULL,
            timezone INT NOT NULL,
            city_name VARCHAR(32) NOT NULL,
            city_id BIGINT NOT NULL,
            sunrise DATETIME NOT NULL,
            sunset DATETIME NOT NULL,
            PRIMARY KEY (datetime)
        );

        CREATE TABLE IF NOT EXISTS weatherdb.cities (
            city_id BIGINT NOT NULL,
            city_name TEXT NOT NULL,
            lon FLOAT NOT NULL,
            lat FLOAT NOT NULL,
            PRIMARY KEY (city_id)
        );
    """
    cursor = con.cursor()
    results = cursor.execute(sql, multi=True)
    # stupidly using multi=True changes the behaviour, returning a generator you
    # need to iterate over to actually advance the processing to the next sql
    # statement in a multi-statement query
    for cur in results:
        if cur.with_rows:
            cur.fetchall()
    con.commit()
    cursor.close()


def insert_record(con, record):
    """insert record dict into weatherdb.weather"""
    cursor = con.cursor()
    query = """
        INSERT INTO weather (
            weather_description, temp, temp_feels_like, temp_min,
            temp_max, pressure, humidity, visibility, wind_speed, wind_deg,
            datetime, timezone, city_name, city_id, sunrise, sunset
        )
        VALUES (
            %(weather_description)s, %(temp)s,
            %(temp_feels_like)s, %(temp_min)s, %(temp_max)s,
            %(pressure)s, %(humidity)s, %(visibility)s, %(wind_speed)s,
            %(wind_deg)s, from_unixtime(%(datetime)s), %(timezone)s, %(city_name)s,
            %(city_id)s, from_unixtime(%(sunrise)s), from_unixtime(%(sunset)s)
        );

        INSERT INTO cities (
            city_id, city_name, lon, lat
        )
        VALUES (
            %(city_id)s, %(city_name)s, %(lon)s, %(lat)s
        )
        ON DUPLICATE KEY UPDATE city_id=city_id ;
    """
    results = cursor.execute(query, record, multi=True)
    # stupidly using multi=True changes the behaviour, returning a generator you
    # need to iterate over to actually advance the processing to the next sql
    # statement in a multi-statement query
    for cur in results:
        if cur.with_rows:
            cur.fetchall()
    con.commit()
    cursor.close()
