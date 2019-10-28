from FlaskAPP import db

class Answers(db.Model):
    TestID = db.Column(db.Integer, db.ForeignKey('testframe.TestID'),
        primary_key=True)
    QuestionID = db.Column(db.Integer, db.ForeignKey('questions.QuestionID'),
        primary_key=True)
    Answer = db.Column(db.String(250))