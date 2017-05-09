from skyscraper.models import base

for item in base.select_all_flights():
    print item
