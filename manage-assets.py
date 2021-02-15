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

if ( path.exists( 'pickle/dataframe.pickle' ) ):
    data = pd.read_pickle( 'pickle/dataframe.pickle' )

if ( len( sys.argv ) > 1 ):
    if ( sys.argv[ 1 ] == 'buy'  ):
        try:
            orders[ str( len( orders ) ) ] = asset( sys.argv[ 2 ], sys.argv[ 3 ], sys.argv[ 4 ], str( len( orders ) ) )
        except:
            print( 'Syntax: manage-asset.py buy ticker quantity price' )
            exit()

    elif ( sys.argv[ 1 ] == 'sell' ):
        try:
            orders[ sys.argv[ 2 ] ].status = 'sold'
        except:
            print( 'Error: asset not found' )
            exit()

        try:
            if ( float( sys.argv[ 3 ] ) > 0 ):
                orders[ sys.argv[ 2 ] ].profit = round( (  orders[ sys.argv[ 2 ] ].quantity * float( sys.argv[ 3 ] ) ) - (  orders[ sys.argv[ 2 ] ].quantity *  orders[ sys.argv[ 2 ] ].price ), 3 )
            else:
                orders.pop( sys.argv[ 2 ] )
        except:
            print( 'Syntax: manage-asset.py sell asset_id sale_price' )
            exit()

    # Change the status on an existing order
    elif ( sys.argv[ 1 ] == 'update_status' ):
        try:
            orders[ sys.argv[ 2 ] ].status = str( sys.argv[ 3 ] )
        except:
            print( 'Error: asset not found' )
            exit()

    # List all orders in the log
    elif ( sys.argv[ 1 ] == 'list' ):
        if ( len( orders ) > 0 ):
            print( 'Asset Log -------------------------------' )
            print( "{:<10}  {:<16}  {:<6}  {:<12}  {:<12}  {:<12}  {:<12}  {:<25}".format( 'Status', 'Date/Time', 'Ticker', 'Quantity', 'Price', 'Cost', 'Value', 'ID' ) )
            for a_asset in orders.values():
                print( "{:<10}  {:<16}  {:<6}  {:<12}  {:<12}  {:<12}  {:<12}  {:<25}".format( str( a_asset.status ), a_asset.timestamp.strftime( '%Y-%m-%d %H:%M' ), str( a_asset.ticker ), str( a_asset.quantity ), str( a_asset.price ), str( round( a_asset.price * a_asset.quantity, 3 ) ), str( round( data.iloc[ -1 ][ a_asset.ticker ] * a_asset.quantity, 3 ) ), str( a_asset.order_id ) ) )
        else:
            print( 'No orders found.' )
        exit()

    else:
        print( 'Syntax: manage-asset.py buy ticker quantity price | sell asset_id sale_price | update_status order_id status | list' )
        exit()

    print( 'New Asset Log ---------------------------' )
    print( "{:<10}  {:<16}  {:<6}  {:<12}  {:<12}  {:<12}  {:<12}  {:<25}".format( 'Status', 'Date/Time', 'Ticker', 'Quantity', 'Price', 'Cost', 'Value', 'ID' ) )
    for a_asset in orders.values():
        print( "{:<10}  {:<16}  {:<6}  {:<12}  {:<12}  {:<12}  {:<12}  {:<25}".format( str( a_asset.status ), a_asset.timestamp.strftime( '%Y-%m-%d %H:%M' ), str( a_asset.ticker ), str( a_asset.quantity ), str( a_asset.price ), str( round( a_asset.price * a_asset.quantity, 3 ) ), str( round( data.iloc[ -1 ][ a_asset.ticker ] * a_asset.quantity, 3 ) ), str( a_asset.order_id ) ) )

    with open( 'pickle/orders.pickle', 'wb' ) as f:
        pickle.dump( orders, f )

else:
    print( 'Syntax: manage-asset.py buy ticker quantity price | sell asset_id sale_price | update_status order_id status | list' )
