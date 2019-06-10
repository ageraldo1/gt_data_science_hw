from flask_restful import Resource
from models.metadata import MetadataModel

class Metadata(Resource):
    def get(self, sampleid):

        return {'result': MetadataModel.get_metadata(sampleid)}, 200
