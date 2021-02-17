#!/usr/bin/python3 -u

# Crypto Trading Bot - Add or remove assets from the bot's portfolio
# Version: 1.0

from classes.asset import asset
from os import path
import pandas as pd
import pickle
import sys

orders = {}
data = pd.DataFrame()

# Load assets and data
if path.exists( 'pickle/orders.pickle' ):
    with open( 'pickle/orders.pickle', 'rb' ) as f:
        orders = pickle.load( f )

if path.exists( 'pickle/dataframe.pickle' ):
    data = pd.read_pickle( 'pickle/dataframe.pickle' )

if len( sys.argv ) > 1:
    if sys.argv[ 1 ] == 'buy':
        try:
            orders[ str( len( orders ) ) ] = asset( sys.argv[ 2 ], sys.argv[ 3 ], sys.argv[ 4 ], str( len( orders ) ) )
        except:
            print( 'Syntax: manage-asset.py buy ticker quantity price' )
            exit()

    elif sys.argv[ 1 ] == 'sell':
        try:
            orders[ sys.argv[ 2 ] ].status = 'S'
        except:
            print( 'Error: asset not found' )
            exit()

        try:
            if float( sys.argv[ 3 ] ) > 0:
                orders[ sys.argv[ 2 ] ].profit = round( (  orders[ sys.argv[ 2 ] ].quantity * float( sys.argv[ 3 ] ) ) - (  orders[ sys.argv[ 2 ] ].quantity *  orders[ sys.argv[ 2 ] ].price ), 3 )
            else:
                orders.pop( sys.argv[ 2 ] )
        except:
            print( 'Syntax: manage-asset.py sell asset_id sale_price' )
            exit()

    # Change the status on an existing order
    elif sys.argv[ 1 ] == 'update_status':
        try:
            orders[ sys.argv[ 2 ] ].status = str( sys.argv[ 3 ] )
        except:
            print( 'Error: asset not found' )
            exit()

    elif sys.argv[ 1 ] == 'csv':
        import csv
        with open( 'orders.csv', 'w', encoding='utf8' ) as csv_file:
            writer = csv.writer( csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL )
            writer.writerow( [ 'Date and Time', 'Order ID', 'Status', 'Ticker', 'Quantity', 'Price', 'Cost', 'Current Value', 'Profit' ] )
            for a_asset in orders.values():
                row = [
                    a_asset.timestamp.strftime( '%Y-%m-%d %H:%M' ),
                    str( a_asset.order_id ),
                    str( a_asset.status ),
                    str( a_asset.ticker ),
                    str( a_asset.quantity ),
                    str( a_asset.price ),
                    str( round( a_asset.price * a_asset.quantity, 3 ) )
                ]

                if a_asset.status == 'B':
                    row.extend( [ str( round( data.iloc[ -1 ][ a_asset.ticker ] * a_asset.quantity, 3 ) ), 0 ] )
                elif a_asset.status == 'S':
                   row.extend( [ 0, str( a_asset.profit ) ] )
                else:
                    row.extend( [ 0, 0 ] )

                writer.writerow( row )

    # List all orders in the log
    if len( orders ) > 0:
        print( 'Asset Log -------------------------------' )
        for a_asset in orders.values():
            if len( sys.argv ) <= 2 or ( len( sys.argv ) > 2 and a_asset.status == sys.argv[ 2 ] ):
                print( "Date and time: {}\nID: {}\nStatus: {}\nTicker: {}\nQuantity: {}\nPrice: $ {}\nCost: $ {}".format(
                    a_asset.timestamp.strftime( '%Y-%m-%d %H:%M' ),
                    str( a_asset.order_id ),
                    str( a_asset.status ),
                    str( a_asset.ticker ),
                    str( a_asset.quantity ),
                    str( a_asset.price ),
                    str( round( a_asset.price * a_asset.quantity, 3 ) )
                ) )

                if a_asset.status == 'B':
                    print( 'Current Value: $ ' + str( round( data.iloc[ -1 ][ a_asset.ticker ] * a_asset.quantity, 3 ) ) )
                elif a_asset.status == 'S':
                    print( 'Profit: $ ' + str( a_asset.profit ) )

                print()
    else:
        print( 'No orders found.' )

else:
    print( 'Syntax: manage-asset.py buy ticker quantity price | sell asset_id sale_price | update_status order_id status | list' )
    exit()

with open( 'pickle/orders.pickle', 'wb' ) as f:
    pickle.dump( orders, f )
