from flask_restplus import Resource, reqparse
from models.measurement import MeasurementModel

class Tobs(Resource):
    #
    # query for the dates and temperature observations from a year from the last data point.
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    #
    # TA's : I wasn't sure regarding the statement "the last data point". The last data point can be the max id of the measurement table or max date. So I decided to include in JSON response both assumptions.
    # last_observation             : last record of the measurement table
    # observations_last_data_point : all records from the last date
    # observations_previous_year   : all records from the last date - 12 months
    def get(self):           
        return { 'last_observation' : MeasurementModel.get_last_data_point().to_json(),
                 'observations_last_data_point' : [item.to_json(['date', 'tobs']) for item in MeasurementModel.get_last_data_points()],
                 'observations_previous_year' : [item.to_json(['date', 'tobs']) for item in MeasurementModel.get_previous_year_data_points()]
               }, 200
        
