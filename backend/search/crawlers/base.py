import os


def crawler_settings():
    CLIENT_ID = os.getenv('CLIENT_ID', None)
    CLIENT_SECRET = os.getenv('CLIENT_SECRET', None)

    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("ERROR: you need to check a client_id or client_secret")

    return CLIENT_ID, CLIENT_SECRET
