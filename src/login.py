from SmartApi import SmartConnect
import pyotp
from logzero import logger
import helpers

def login(config_path):
    config_data = helpers.load_config(config_path)
    api_key = config_data['api_keys']['your_api_key']
    userID = config_data['api_keys']['userID']
    pwd = config_data['api_keys']['pwd']
    totp_key = config_data['api_keys']['totp_key']

    obj = SmartConnect(api_key)

    try:
        token = totp_key
        totp = pyotp.TOTP(token).now()
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    data = obj.generateSession(userID, pwd, totp)
    if data['status'] == False:
        logger.error(data)
    else:
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']
        feedToken = obj.getfeedToken()
        res = obj.getProfile(refreshToken)
        print(res)
        obj.generateToken(refreshToken)

    return obj, authToken, refreshToken, feedToken, res

if __name__ == "__main__":
    config_path = "/Users/shashi/Documents/quantala_projects/algo_trade/config/config.yml"
    login(config_path)
