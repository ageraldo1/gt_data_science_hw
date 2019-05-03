from flask_restplus import Resource, reqparse
from models.measurement import MeasurementModel

class Tobs(Resource):

    def get(self):           
        return { 'observations_last_data_point' : [item.to_json(['date', 'tobs']) for item in MeasurementModel.get_last_data_points()],
                 'observations_previous_year' : [item.to_json(['date', 'tobs']) for item in MeasurementModel.get_previous_year_data_points()]
               }, 200
        
