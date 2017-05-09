import re
from skyscraper.scraper import base
from skyscraper import config

CONF = config.CONF


class WizzScrapper(base.BaseScrapper):

    URL = CONF.wizzair.url
    operator = 'wizzair'

    def __init__(self):
        super(WizzScrapper, self).__init__(self.URL)

    def _get_schema(self):
        '''
        date: 2017-05-03
        '''
        template = '{{' \
            '"adultCount": 1, ' \
            '"childCount": 0, ' \
            '"dayInterval": 10, ' \
            '"flightList": ' \
               '[{{ '\
                    '"departureStation": "{departureStation}", '\
                    '"arrivalStation": "{arrivalStation}", '\
                    '"date": "{date}" ' \
               '}}], '\
            '"isRescueFare": "false", '\
            '"wdc": "false" '\
            '}}'
        return template

    def _get_date(self, fligth):
        return re.match('(\d+-\d+-\d+)', fligth.get('date')).group(0)

    def _get_price(self, fligth):
        return fligth.get('price').get('amount')

    def _get_currency(self, fligth):
        return fligth.get('price').get('currencyCode')

    def _get_flights(self, response):
        return response.get('outboundFlights')

    def _is_valid_flight(self, flight):
        return flight.get('price')
