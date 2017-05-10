import abc
import json
import requests

from skyscraper import exception
from skyscraper.utils import log

LOG = log.Logger(__file__)


class BaseScrapper(object):

    def __init__(self, url):
        self.url = url

    def _send_post(self, headers, payload):
        request_response = requests.post(
            self.url, headers=headers, json=payload)
        if request_response.status_code == 503:
            raise exception.SkyscraperException(
                "Request failed: Service unavailable! Check API version!")
        return json.loads(request_response.content.decode('utf8'))

    @abc.abstractmethod
    def _get_schema(self):
        pass

    def get_flights(self, date, departure, destination):
        template = self._get_schema()
        string_schema = template.format(departureStation=departure,
                                        arrivalStation=destination,
                                        date=date)
        json_schema = json.loads(string_schema)
        request_headers = self.get_user_agent()
        request_headers['content-length'] = str(len(string_schema))
        try:
            response = self._send_post(request_headers, json_schema)
        except exception.SkyscraperException as ex:
            LOG.error(str(ex))
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

    def get_user_agent(self):
        return {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en - US, en;q=0.8",
            "content-length": None,
            "content-type": "application/json",
            "origin": self._get_origin(),
            "referer": self._get_referer(),
            "user-agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) "
                          "AppleWebKit / 537.36(KHTML, like Gecko) "
                          "Chrome / 58.0.3029.96 "
                          "Safari / 537.36"
        }

    @abc.abstractmethod
    def _get_origin(self):
        pass

    @abc.abstractmethod
    def _get_referer(self):
        pass
