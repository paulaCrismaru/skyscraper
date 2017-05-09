from skyscraper.models import base
import sys

base.delete_indexes(sys.argv[1:])
for item in base.select_all_flights():
    print item

