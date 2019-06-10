from db import db
from sqlalchemy import desc


class SamplesModel(db.Model):
    __table__ = db.Model.metadata.tables['samples']

    @classmethod
    def get_samples(cls, sample_id, limit_size):
        result = []

        for item in SamplesModel.query.filter(getattr(SamplesModel, sample_id) > 1).order_by(desc(getattr(SamplesModel, sample_id))).limit(limit_size):
            data = {
                'otu_id' : item.otu_id,
                'otu_label' : item.otu_label,
                'sample_value' : item.__getattribute__(sample_id)
            }

            result.append(data)

        return result

    @classmethod
    def get_samples_columns_name(cls):
        return [column for column in db.Model.metadata.tables['samples'].columns.keys() if column.isnumeric()]