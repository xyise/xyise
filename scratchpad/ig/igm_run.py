from trading_ig import IGService

if __name__ == '__main__':

    ig_service = IGService('yligdemo', r'zxASqw!2', r'30efa7f594b1712fd8e6c40c5b5259427a9a2c0c', acc_type='demo')
    ig = ig_service.create_session()
    
    ig_service.search_markets('Bitcoin')

    pass