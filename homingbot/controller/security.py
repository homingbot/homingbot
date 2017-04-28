import config
from .cors import add_cors

IGNORE_METHODS = ["OPTIONS"]

class PostSecurity():
    ''' Handles outgoing responses '''
    def __init__(self, app):
        @app.middleware('response')
        async def cors_middleware(request, response):
            if (config.enable_cors):
                add_cors(response)
