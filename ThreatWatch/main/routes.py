from flask import render_template, request, Blueprint
from datetime import datetime
from ThreatWatch.models import Incident

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    incidents = Incident.query.all()
    if incidents:
        last_updated_date = Incident.query.order_by(Incident.last_modified_date.desc()).first().last_modified_date
    else:
        last_updated_date = datetime.today().date()
    return render_template('home.html', incidents=incidents, last_updated_date=last_updated_date)

@main.route('/about')
def about():
    return render_template('about.html', title='About')
