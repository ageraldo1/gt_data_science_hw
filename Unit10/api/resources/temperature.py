from flask_restplus import Resource
from models.measurement import MeasurementModel
from datetime import datetime

class Temperature(Resource):

    def get(self, startdate, enddate=None):

        try:
            if enddate:
                d_start = datetime.strptime(startdate, '%Y%m%d')
                d_end = datetime.strptime(enddate, '%Y%m%d')
            else:
                d_start = datetime.strptime(startdate, '%Y%m%d')
                d_end = enddate
        except:
            return {'error' : 'Invalid date format. Please use YYYYMMDD'}, 400               

        measurements = MeasurementModel.get_min_avg_max(d_start, d_end)

        return {'measurements' : { 'min' : measurements[0][0], 'avg' :  measurements[0][1], 'max' : measurements[0][2]}}, 200     
        
