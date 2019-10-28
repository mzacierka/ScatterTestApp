from FlaskAPP import db

class TestFrame(db.Model):
    TestID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.DoctorID'), 
        nullable=False, primary_key=True)
    DateTaken = db.Column(db.DateTime)
    TestName = db.Column(db.String(50), db.ForeignKey('json_files.name'))
    TestLength = db.Column(db.Time)

