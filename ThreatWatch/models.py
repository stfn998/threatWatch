# Import necessary modules
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedSerializer as Serializer
from datetime import datetime
from ThreatWatch import db, login_manager
from .enums import AccountStatus, Role

# Define a function to load a user by ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the User class
class User(db.Model, UserMixin):
    # Define User class attributes
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(60), nullable=True)
    last_name = db.Column(db.String(60), nullable=True)
    country = db.Column(db.String(60), nullable=True)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.USER)
    profile_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    account_status = db.Column(db.Enum(AccountStatus), nullable=False, default=AccountStatus.PENDING)
    incidents = db.relationship('Incident', backref='author', lazy=True)

    # Define a method to generate a reset token for password reset
    def get_reset_token(self):
        s = Serializer(current_app.secret_key)
        return s.dumps({'user_id': self.id})

    # Define a method to generate a confirmation token for email confirmation
    def get_confirmation_token(self):
        s = Serializer(current_app.secret_key)
        return s.dumps({'email': self.email}, salt='email-confirm')

    # Define a static method to verify the confirmation token
    @staticmethod
    def verify_confirmation_token(token):
        s = Serializer(current_app.secret_key)
        try:
            data = s.loads(token, salt='email-confirm', max_age=43200)
            email = data.get('email')
            print(email)
        except:
            return None
        return User.query.filter(User.email == email).first()

    # Define a static method to verify the reset token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.secret_key)
        try:
            user_id = s.loads(token, max_age=43200)['user_id']
            print(user_id)
        except:
            return None
        return User.query.get(user_id)

    # Define how the User class will be represented when printed
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.profile_picture}')"

# Define the Incident class
class Incident(db.Model):
    # Define Incident class attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    industry_type = db.Column(db.String(100), nullable=False)
    reliability = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_type = db.Column(db.String(100), nullable=False)
    impact = db.Column(db.Text, nullable=False)
    actions_taken = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Define additional table arguments (constraints)
    __table_args__ = (
        db.CheckConstraint(year >= 1900, name='year_min_constraint'),
        db.CheckConstraint(year <= datetime.now().year, name='year_max_constraint'),
    )

    # Define how the Incident class will be represented when printed
    def __repr__(self):
        return f"Incident('{self.title}','{self.created_date}')"

# Define the AuditLog class
class AuditLog(db.Model):
    # Define AuditLog class attributes
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(80), nullable=False)
    history = db.Column(db.Text(), nullable=True)
    model_name = db.Column(db.String(80), nullable=False)
    original_id = db.Column(db.Integer)
    db_event_name = db.Column(db.String(80), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    user_ip_address = db.Column(db.String(15), nullable=True)
    username = db.Column(db.String(20), nullable=True)
