from FlaskAPP import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Doctor.query.get(int(user_id))


class Doctor(db.Model, UserMixin):
    __tablename__ = 'Doctor'
    DoctorID = db.Column(db.Integer, primary_key=True)
    DoctorName = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=False)
    password_ = db.Column(db.String(15))

    def get_id(self):
        try:
            return self.DoctorID
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')
