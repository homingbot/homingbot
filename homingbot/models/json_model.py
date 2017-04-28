from cassandra.cqlengine import models

class Model(models.Model):
    ''' Base Model Class '''
    __ignore__ = True
    __abstract__ = True

class JsonModel(Model):
    __abstract__ = True
    __ignore__ = True

    def toJson(self):
        keys = self.__dict__['_values'].keys()
        hidden = getattr(self, '__json_hide__', [])
        result = {}
        for key in keys:
            if key[0] != '_' and key not in hidden:
                result[key] = getattr(self, key, None)
        return result

    def __repr__(self):
        return toJson()
