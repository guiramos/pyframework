import datetime
import logging
import os
import traceback

import jwt
from google.oauth2 import id_token

from pyframework.logging import rolling_file_handler, console_handler

from google.auth.transport import requests

JWT_ALGO = "HS256"

logger = logging.getLogger('jwt_util')
logger.setLevel(logging.DEBUG)

logger.addHandler(rolling_file_handler)
logger.addHandler(console_handler)


class InvalidTokenException(Exception):
    def __init__(self, message="Invalid token"):
        self.message = message
        super().__init__(self.message)


def fix_padding(base64_string):
    # Add padding if necessary (Base64 requires '=' padding)
    return base64_string + '=' * (-len(base64_string) % 4)


def add_padding(token: str) -> str:
    """Add padding to a JWT token if necessary."""
    # Base64 encoding requires padding to be divisible by 4
    padding_needed = len(token) % 4
    if padding_needed:
        token += '=' * (4 - padding_needed)
    return token


def decode_google_id_token(token):
    try:
        # Add padding to token before decoding
        padded_token = add_padding(token)
        client_ids = os.getenv("GOOGLE_CLIENT_ID").split(',')

        for client_id in client_ids:
            try:
                return id_token.verify_oauth2_token(padded_token, requests.Request(), client_id)
            except ValueError:
                continue

        # If none of the client IDs work, raise an exception
        raise InvalidTokenException("Invalid Google token")
    except ValueError as e:
        logger.error("Invalid Google token", exc_info=True)
        # Invalid token
        raise InvalidTokenException("Invalid Google token") from e

class JwtUtil:
    def __init__(self, secret_string: str):
        self.secret_key = secret_string.encode('utf-8')

    def decode_jwt_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[JWT_ALGO])

            # Check if the "exp" field is present and not expired
            if "exp" in payload:
                exp = datetime.datetime.fromtimestamp(payload["exp"])
                if exp < datetime.datetime.now():
                    raise InvalidTokenException("Token has expired")

            return payload
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("Token has expired")
        except jwt.InvalidTokenError:
            traceback.print_exc()
            raise InvalidTokenException("Invalid token")

    def decode_auth_token(self, token: str, custom_jwt: bool) -> dict:
        return self.decode_jwt_token(token) if custom_jwt else decode_google_id_token(token)

    def generate_token(self, jwt_payload: dict, hours=24 * 365) -> str:
        # Calculate the expiration time
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
        exp_timestamp = int(expiration_time.timestamp())

        jwt_payload["exp"] = exp_timestamp
        return jwt.encode(jwt_payload, self.secret_key, algorithm=JWT_ALGO)
