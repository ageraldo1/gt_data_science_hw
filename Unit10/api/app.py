from flask import Flask
from flask_restplus import Resource, Api, Namespace

from resources.precipitation import Precipitation
from resources.stations import Stations
from resources.tobs import Tobs
from resources.temperature import Temperature

app = Flask(__name__)
api = Api(app, version='1.0', title='Climate App API',  description='Flask API Climate Application')

app.config.from_object('config')

api.add_resource(Precipitation, '/api/v1.0/precipitation')
api.add_resource(Stations, '/api/v1.0/stations')
api.add_resource(Tobs, '/api/v1.0/tobs')
api.add_resource(Temperature, '/api/v1.0/stats/<string:startdate>', '/api/v1.0/stats/<string:startdate>/<string:enddate>')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    db.reflect(app=app)

    app.run(port=5000, debug=True)