import config

''' Decorator function to handle cors on requests '''
def enable_cors(func):
    def func_wrapper(self, request):
        res = func(self, request);
        ip = request.headers['Remote-Addr'] #.split(":")[0] #TODO cross check with db
        res.headers['Access-Control-Allow-Origin'] = config.cor_origins
        res.headers['Access-Control-Allow-Methods'] = config.cor_methods
        res.headers['Access-Control-Allow-Headers'] = config.cor_headers
        res.headers['Access-Control-Allow-Max-Age'] = config.cor_max_age
        res.headers['Access-Control-Allow-Credentials'] = config.cor_creds
        return res
    return func_wrapper

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = config.cor_origins
    response.headers['Access-Control-Allow-Methods'] = config.cor_methods
    response.headers['Access-Control-Allow-Headers'] = config.cor_headers
    response.headers['Access-Control-Allow-Max-Age'] = config.cor_max_age
    response.headers['Access-Control-Allow-Credentials'] = config.cor_creds
    return response
