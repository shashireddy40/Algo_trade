from fyers_api import fyersModel
from fyers_api import accessToken
import os
from datetime import datetime

from fyers_api.Websocket import ws

import sqlite3
import time


class credentials:
    client_id='ZYZ5JYOGTX-100'
    secret_key="H5UP4TBCCV"
    redirect_uri="https://www.google.com/"
    response_type="code"
    grant_type="authorization_code"
    session=accessToken.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type,
        grant_type=grant_type,
        )

    def auth_code_func(self,session):
        auth_code = session.generate_authcode()
        return auth_code
    
    def access_token(session,auth_code):
        session.set_token(auth_code)
        response = session.generate_token()
        access_token = response["access_token"]
        return access_token
    