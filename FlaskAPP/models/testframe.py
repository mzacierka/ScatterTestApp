from FlaskAPP import db


class Testframe(db.Model):
    __tablename__ = 'TestFrame'
    TestID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, primary_key=True)
    DateTaken = db.Column(db.DateTime)
    DoctorID = db.Column(db.Integer, primary_key=True)
    TestName = db.Column(db.String(50))
    TestLength = db.Column(db.Float)

