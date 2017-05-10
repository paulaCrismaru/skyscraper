import abc
import json
import requests

from skyscraper import exception
from skyscraper.utils import log

LOG = log.Logger(__file__)


class BaseScrapper(object):

    def __init__(self, url):
        self.url = url

    def _send_post(self, payload):
        if type(payload) is str:
            payload = json.loads(payload)
        request_response = requests.post(self.url, json=payload)
        if request_response.status_code == 503:
            raise exception.SkyscraperException(
                "Request failed: Service unavailable! Check API version!")
        return json.loads(request_response.content.decode('utf8'))

    @abc.abstractmethod
    def _get_schema(self):
        pass

    def get_flights(self, date, departure, destination):
        template = self._get_schema()
        request_string = template.format(departureStation=departure,
                                         arrivalStation=destination,
                                         date=date)
        try:
            response = self._send_post(request_string)
        except exception.SkyscraperException as ex:
            LOG.error(ex.message)
            return None
        return self._get_valid_fligths(response)

    @abc.abstractmethod
    def _is_valid_flight(self, flight):
        pass

    @abc.abstractmethod
    def _get_date(self, flight):
        pass

    @abc.abstractmethod
    def _get_price(self, flight):
        pass

    @abc.abstractmethod
    def get_currency(self, flight):
        pass

    def _get_valid_fligths(self, response):
        flights = self._get_flights(response)
        valid_flights = []
        for flight in flights:
            if self._is_valid_flight(flight):
                f = {
                    'operator': self.operator,
                    'date': self._get_date(flight),
                    'price': self._get_price(flight),
                    'currency': self._get_currency(flight)
                }
                valid_flights.append(f)
        return valid_flights
