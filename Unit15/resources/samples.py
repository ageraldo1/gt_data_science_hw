from flask_restful import Resource
from models.samples import SamplesModel

class Samples(Resource):
    def get(self, sampleid=None, limit=None):

        if limit:
             return {'result': SamplesModel.get_samples(sampleid, limit)}, 200

        elif sampleid:
            return {'result': SamplesModel.get_samples(sampleid, 10)}, 200
            
        else:
            return {'result': SamplesModel.get_samples_columns_name()}, 200
