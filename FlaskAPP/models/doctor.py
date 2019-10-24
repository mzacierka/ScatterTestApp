from FlaskAPP import db

class Doctor(db.Model):
    DoctorID = db.Column(db.Integer, primary_key=True)
    DoctorName = db.Column(db.String(50))
    email = db.Column(db.String(50), primary_key=True)
    password_ = db.Column(db.String(15))