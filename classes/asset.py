class asset:
    ticker = ''
    quantity = 0.0
    price = 0.0
    order_id = ''

    def __init__( self, ticker = '', quantity = 0.0, price = 0.0, order_id = '' ):
        self.ticker = ticker
        self.quantity = float( quantity )
        self.price = float( price )
        self.order_id = order_id