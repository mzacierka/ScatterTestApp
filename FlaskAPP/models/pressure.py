from FlaskAPP import db

class Pressure(db.Model):
    TestID = db.Column(db.Integer, db.ForeignKey('testframe.TestID'), 
        primary_key=True)
    CircleID = db.Column(db.Integer, db.ForeignKey('circles.CircleID'), 
        primary_key=True)
    Xcoord = db.Column(db.Double)
    Ycoord = db.Column(db.Double)
    Pressure = db.Column(db.Double)
    