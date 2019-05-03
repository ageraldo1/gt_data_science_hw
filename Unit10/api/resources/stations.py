from flask_restplus import Resource, reqparse
from models.stations import StationsModel

class Stations(Resource):

    def get(self):
        return { 'stations' : [station.to_json() for station in StationsModel.get_all_stations()]}, 200
        
