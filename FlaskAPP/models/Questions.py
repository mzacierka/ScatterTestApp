from FlaskAPP import db


class Questions(db.Model):
    QuestionID = db.Column(db.Integer, primary_key=True)
    QuestionType = db.Column(db.Integer)
    PossibleAnswers = db.Column(db.String)
    Question = db.Column(db.String)
