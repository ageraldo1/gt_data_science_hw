from db import db

class MetadataModel(db.Model):
    __table__ = db.Model.metadata.tables['sample_metadata']

    @classmethod
    def get_metadata(cls, sample_id):
        result = MetadataModel.query.filter(MetadataModel.sample == sample_id).first()

        return {
            'sample'    : result.sample,
            'ethnicity' : result.ETHNICITY,
            'gender'    : result.GENDER,
            'age'       : result.AGE,
            'location'  : result.LOCATION,
            'bbtype'    : result.BBTYPE,
            'wfreq'     : result.WFREQ
        }
