from datetime import datetime
from flaskblog import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50),nullable=False)
    Address = db.Column(db.String(100),nullable=True)
    PhoneNumber = db.Column(db.String(13), unique=True, nullable=False)
    PlotNumber  = db.Column(db.String(10), unique=True,  nullable=False)
    FlatNumber = db.Column(db.String(10), nullable=True)
    PaymentStatus = db.Column(db.String(10), nullable=False,default="False")
    Role =         db.Column(db.String(10), nullable=False, default="User")
    Date_created = db.Column(db.DateTime, nullable=False, default=datetime.today())
    payment = db.relationship('Payment', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.Username}', '{self.PhoneNumber}', '{self.PlotNumber}','{self.PaymentStatus}','{self.Role}','{self.Date_created}')"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    PhoneNumber = db.Column(db.String(13))
    ReceiptNo = db.Column(db.String(10), nullable=False)
    Amount    =  db.Column(db.String(10), nullable=False)
    StartDate = db.Column(db.DateTime, nullable=False, default=datetime.today())
    EndDate   = db.Column(db.DateTime, nullable=False, default=datetime.today())
    TotalMonth = db.Column(db.Integer, nullable=False, default=0)
    Donation  = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Payment('{self.ReceiptNo}', '{self.Amount}','{self.StartDate}','{self.EndDate}','{self.PhoneNumber}', '{self.TotalMonth}')"
