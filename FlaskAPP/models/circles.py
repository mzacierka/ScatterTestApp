from FlaskAPP import db

class Circles(db.Model):
    TestID = db.Column(db.Integer, db.ForeignKey('testframe.TestID'),
        primary_key=True)
    CircleID = db.Column(db.Integer)
    symbol = db.Column(db.String(1))
    begin_circle = db.Column(db.Time)
    end_circle = db.Column(db.Time)
    total_time = db.Column(db.Time)