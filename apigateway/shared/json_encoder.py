from flask.json import JSONEncoder
from bson import ObjectId


class ImprovedJSONEncoder(JSONEncoder):
    """ ObjectIds are not encoded by default so we must extend flask's JSONEncoder. """

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return JSONEncoder.default(self, obj)
