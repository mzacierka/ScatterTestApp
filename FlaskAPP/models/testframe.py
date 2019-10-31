from FlaskAPP import db

class TestFrame(db.Model):
    __tablename__ = "testframe"
    TestID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, primary_key=True)
    DoctorID = db.Column(db.Integer, db.ForeignKey('Doctor.DoctorID'), 
        nullable=False, primary_key=True)
    DateTaken = db.Column(db.DateTime)
    TestName = db.Column(db.String(50), db.ForeignKey('json_files.name'))
    TestLength = db.Column(db.Time)

