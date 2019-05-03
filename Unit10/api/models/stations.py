from db import db

class StationsModel(db.Model):
    __tablename__ = 'station'
    id = db.Column(db.Integer, primary_key = True)
    station = db.Column(db.Text)
    name = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    elevation = db.Column(db.Float)

    def __init__(self, _id, station, name, latitude, longitude, elevation):
        self.id = _id
        self.station = station
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def to_json(self):
        return {'station' : self.station, 
                'name': self.name,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'elevation': self.elevation
                }

    @classmethod
    def get_all_stations(cls):
        return StationsModel.query.all()

    


