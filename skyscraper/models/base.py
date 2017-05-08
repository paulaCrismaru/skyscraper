import peewee

database = peewee.SqliteDatabase(database="db0")


class BaseModel(peewee.Model):

    class Meta:
        database = database


class Fligths(BaseModel):

    operator = peewee.CharField()
    departure = peewee.CharField(max_length=3)
    destination = peewee.CharField(max_length=3)
    date = peewee.DateField()
    days_before = peewee.IntegerField()
    price = peewee.IntegerField()
    currency = peewee.CharField()

    def insert_data(self, **kwargs):
        print(kwargs)


def create_tables(database):
    database.connect()
    try:
        database.create_tables([Fligths])
    except peewee.OperationalError:
        print("table already exists")


def insert_data(operator=None, departure=None, destination=None,
                date=None, days_before=None, price=None, currency=None):
    data = {
        'operator': operator,
        'departure': departure,
        'destination': destination,
        'date': date,
        'days_before': days_before,
        'price': price,
        'currency': currency
    }
    query = Fligths.insert(data)
    query.execute()


def select_all_flights(model=Fligths):
    data = model.select().dicts()
    return([l for l in data])


def clear_all(model=Fligths):
    query = model.delete()
    query.execute()
