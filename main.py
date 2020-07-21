"""docstring"""
import sys

import db
import weather


def main(city):
    con = db.connect()
    db.create_table(con)
    response = weather.get_weather(city)
    record = weather.format_response(response)
    db.insert_record(con, record)
    con.close()


if __name__ == "__main__":
    main(sys.argv[1])
