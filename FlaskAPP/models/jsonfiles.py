from FlaskAPP import db


class JSONFiles(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    data = db.Column(db.LargeBinary)
