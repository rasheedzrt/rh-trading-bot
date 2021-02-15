from datetime import datetime

class asset:
    ticker = ''
    quantity = 0.0
    price = 0.0
    order_id = ''
    timestamp = 0
    status = 'new'
    profit = 0.0

    def __init__( self, ticker = '', quantity = 0.0, price = 0.0, order_id = '', status = 'new', profit = 0.0, timestamp = 0 ):
        self.ticker = ticker
        self.quantity = float( quantity )
        self.price = float( price )
        self.order_id = order_id
        self.timestamp = datetime.now()
        self.status = 'new'
        self.profit = float( profit )