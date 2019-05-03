from db import db
from datetime import datetime
from dateutil.relativedelta import relativedelta

class MeasurementModel(db.Model):
    __tablename__ = 'measurement'
   
    id = db.Column(db.Integer, primary_key = True)
    station = db.Column(db.Text)
    date = db.Column(db.Text)
    prcp = db.Column(db.Float)
    tobs = db.Column(db.Float)

    def __init__(self, _id, station, _date, prcp, tobs):
        self.id = _id
        self.station = station
        self.date = _date
        self.prcp = prcp
        self.tobs = tobs

    def to_json(self, attrs=None):

        if attrs:
            filter_dict = {}

            if 'id' in attrs: filter_dict['id'] = self.id
            if 'station' in attrs: filter_dict['station'] = self.station
            if 'date' in attrs: filter_dict['date'] = self.date
            if 'prcp' in attrs: filter_dict['prcp'] = self.prcp
            if 'tobs' in attrs: filter_dict['tobs'] = self.tobs

            return filter_dict
        else:
            return {'id' : self.id, 
                    'station': self.station,
                    'date': self.date,
                    'prcp': self.prcp,
                    'tobs': self.tobs
                    }

    @classmethod
    def get_last_data_points(cls):
        last_datapoint  = MeasurementModel.query.with_entities(db.func.max(db.func.Date(MeasurementModel.date))).scalar()

        return MeasurementModel.query.filter(MeasurementModel.date == last_datapoint).all()
    
    @classmethod
    def get_previous_year_data_points(cls):
        last_datapoint = datetime.strptime(MeasurementModel.query.with_entities(db.func.max(db.func.Date(MeasurementModel.date))).scalar(), '%Y-%m-%d')
        previous_year = last_datapoint - relativedelta(months=12) 

        return MeasurementModel.query.filter(MeasurementModel.date > previous_year).all()

    @classmethod
    def get_all_measurements(cls):
        return MeasurementModel.query.all()

    @classmethod
    def get_min_avg_max(cls, startdate, enddate=None):

        if enddate:            
            return MeasurementModel.query.with_entities(db.func.min(MeasurementModel.tobs), db.func.avg(MeasurementModel.tobs), db.func.max(MeasurementModel.tobs)).filter(db.func.Date(MeasurementModel.date) >= startdate).filter(db.func.Date(MeasurementModel.date) <= enddate).all()

        else:
            return MeasurementModel.query.with_entities(db.func.min(MeasurementModel.tobs), db.func.avg(MeasurementModel.tobs), db.func.max(MeasurementModel.tobs)).filter(db.func.Date(MeasurementModel.date) >= startdate).all()
                    

    


