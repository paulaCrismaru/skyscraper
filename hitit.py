from skyscraper import config
from skyscraper.scraper import wizzair
from skyscraper.models import base as database
from datetime import datetime

CONF = config.CONF


if __name__ == '__main__':

    departure_airport = CONF.wizzair.departure_airport
    destination_airports = CONF.wizzair.destination_airports.split(',')

    database.create_tables(database.database)
    scraper = wizzair.WizzScrapper()

    for destination in destination_airports:
        today = datetime.strftime(datetime.now(), '%Y-%m-%d')
        fligths = scraper.get_fligths(
            departure=departure_airport, destination=destination,
            date=today)
        for flight in fligths:
            date = datetime.strptime(flight.get('date'), '%Y-%m-%d')
            flight.update({
                'departure': departure_airport,
                'destination': destination,
                'days_before': (date - datetime.now()).days,
                'date': flight.get('date')
            })
            database.insert_data(**flight)
            print("Found flight from %s to %s on %s" %
                  (departure_airport, destination, flight.get('date')))
