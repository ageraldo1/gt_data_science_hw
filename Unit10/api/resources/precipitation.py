from flask_restplus import Resource, reqparse
from models.measurement import MeasurementModel

class Precipitation(Resource):

    def get(self):
        return { 'measurements' : [item.to_json(['date', 'prcp']) for item in MeasurementModel.get_all_measurements()]}, 200
        
