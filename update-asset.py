#!/usr/bin/python3 -u

# Crypto Trading Bot - Add or remove assets from the bot's portfolio
# Version: 1.0

from classes.asset import asset
from os import path
import pickle
import sys

orders = {}

if path.exists( 'pickle/orders.pickle' ):
    # Load assets
    with open( 'pickle/orders.pickle', 'rb' ) as f:
        orders = pickle.load( f )

if ( len( sys.argv ) > 1 ):
    if ( sys.argv[ 1 ] == 'add'  ):
        try:
            orders[ str( len( orders ) ) ] = asset( sys.argv[ 2 ], sys.argv[ 3 ], sys.argv[ 4 ], str( len( orders ) ) )
        except:
            print( 'Syntax: update-asset.py add ticker quantity price' )
            exit()

    elif ( sys.argv[ 1 ] == 'remove' ):
        try:
            orders.pop( sys.argv[ 2 ] )
        except:
            print( 'Error: asset not found' )
            exit()

    elif ( sys.argv[ 1 ] == 'list' ):
        if ( len( orders ) > 0 ):
            print( 'Current Asset List:' )
            for a_asset in orders.values():
                # Print a summary of all our assets
                print( '[' + str( a_asset.order_id ) + '] ' + str( a_asset.ticker ) + ': ' + str( a_asset.quantity ) + ' | Price: $' + str( round( a_asset.price, 3 ) ) + ' | Cost: $' + str( round( a_asset.quantity * a_asset.price, 3 ) ) )
        else:
            print( 'No orders found.' )
        exit()

    else:
        print( 'Syntax: update-asset.py [add|remove|list] [ticker|asset_id] [quantity] [price]' )
        exit()

    print( 'New Asset List:' )
    for a_asset in orders.values():
        # Print a summary of all our assets
        print( '[' + str( a_asset.order_id ) + '] ' + str( a_asset.ticker ) + ': ' + str( a_asset.quantity ) + ' | Price: $' + str( round( a_asset.price, 3 ) ) + ' | Cost: $' + str( round( a_asset.quantity * a_asset.price, 3 ) ) )

    with open( 'pickle/orders.pickle', 'wb' ) as f:
        pickle.dump( orders, f )

else:
    print( 'Syntax: update-asset.py [add|remove|list] [ticker|asset_id] [quantity] [price]' )
