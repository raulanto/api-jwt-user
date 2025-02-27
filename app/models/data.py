from app import db


class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    def to_data_dict(self):
        data_values = [data.value for data in self.data]
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "data_values": data_values
        }



class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    series = db.relationship('Series', backref=db.backref('data', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "series_id": self.series_id,
            "series_name": self.series.name
        }

