from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from ThreatWatch import db
from ThreatWatch.models import Incident
from ThreatWatch.incidents.forms import IncidentForm
from ThreatWatch.enums import AccountStatus, Role
from ThreatWatch.decorators import account_status_required

# Create a Blueprint named 'incidents'
incidents = Blueprint('incidents', __name__)

# Route for creating a new incident (GET and POST requests are accepted)
@incidents.post('/incident/new')
@incidents.get('/incident/new')
@login_required
@account_status_required(AccountStatus.CONFIRMED)
def new_incident():
    # Create a new IncidentForm instance
    form = IncidentForm()
    force_add = request.form.get('force_add', type=bool, default=False)
    if form.validate_on_submit():
        if not force_add:
            # Check for similar incidents first
            title_words = set(form.title.data.split())
            similar_incidents = Incident.query.filter_by(year=form.year.data, industry_type=form.industry_type.data, incident_type=form.incident_type.data).all()
            for inc in similar_incidents:
                if len(title_words.intersection(set(inc.title.split()))) / len(title_words) >= 0.5:
                    return jsonify(status='similar')
        # Create a new Incident instance and populate its attributes from the form data
        incident = Incident(
            title = form.title.data,
            year = form.year.data,
            industry_type = form.industry_type.data,
            reliability = form.reliability.data,
            description = form.description.data,
            incident_type = form.incident_type.data,
            impact = form.impact.data,
            actions_taken = form.actions_taken.data,
            created_date = datetime.utcnow(),
            last_modified_date = datetime.utcnow(),
            author = current_user
        )
        db.session.add(incident)
        db.session.commit()
        flash('Your incident has been created.', 'success')
        return jsonify(status='added')
    # Render the template for creating a new incident
    return render_template('create_incident.html', title='New Incident', form = form, legend='New Incident')

# Route for viewing a specific incident
@incidents.route('/incident/<int:incident_id>')
def incident(incident_id):
    # Retrieve the incident with the specified ID or return a 404 error if not found
    incident = Incident.query.get_or_404(incident_id)
    # Render the template for displaying the incident details
    return render_template('incident.html', title=incident.title, incident=incident)

# Route for updating an existing incident (GET and POST requests are accepted)
@incidents.post('/incident/<int:incident_id>/update')
@incidents.get('/incident/<int:incident_id>/update')
@login_required
@account_status_required(AccountStatus.CONFIRMED)
def update_incident(incident_id):
    # Retrieve the incident with the specified ID or return a 404 error if not found
    incident = Incident.query.get_or_404(incident_id)
    if incident.author != current_user and (incident.author.account_status == AccountStatus.CONFIRMED and current_user.role == Role.ADMIN):
        abort(403)  # If user does not have permission, return a 403 error
    # Create a new IncidentForm instance
    form = IncidentForm()
    form.submit.label.text = 'Update incident'
    if form.validate_on_submit():
        # Update the attributes of the incident with the form data
        incident.title = form.title.data
        incident.year = form.year.data
        incident.industry_type = form.industry_type.data
        incident.reliability = form.reliability.data
        incident.description = form.description.data
        incident.impact = form.impact.data
        incident.actions_taken = form.actions_taken.data
        incident.last_modified_date = datetime.utcnow()
        db.session.commit()
        flash('Your incident has been updated.', 'success')
        return redirect(url_for('incidents.incident', incident_id=incident.id))
    elif request.method == 'GET':
        # Pre-populate the form with the incident's current data
        form.title.data = incident.title
        form.year.data = incident.year
        form.industry_type.data = incident.industry_type
        form.reliability.data = incident.reliability
        form.description.data = incident.description
        form.industry_type.data = incident.industry_type
        form.impact.data = incident.impact
        form.actions_taken.data = incident.actions_taken
    # Render the template for updating the incident
    return render_template('create_incident.html', title='Update Incident', form = form, legend='Update Incident')

# Route for deleting an incident (GET and POST requests are accepted)
@incidents.post('/incident/<int:incident_id>/delete')
@incidents.get('/incident/<int:incident_id>/delete')
@login_required
@account_status_required(AccountStatus.CONFIRMED)
def delete_incident(incident_id):
    # Retrieve the incident with the specified ID or return a 404 error if not found
    incident = Incident.query.get_or_404(incident_id)
    if current_user.account_status == AccountStatus.DISABLED:
        abort(405)  # If user's account is disabled, return a 405 error
    if incident.author != current_user and current_user.role != Role.ADMIN:
        abort(405)  # If user does not have permission, return a 405 error
    # Delete the incident from the database
    db.session.delete(incident)
    db.session.commit()
    flash('Your incident has been deleted.', 'success')
    return redirect(url_for('main.home'))
