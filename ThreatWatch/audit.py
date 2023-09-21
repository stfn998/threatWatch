from flask import g, request
from flask_login import current_user
from sqlalchemy import event
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.attributes import get_history
from datetime import datetime
import json
from .models import User, AuditLog, Incident
from enum import Enum

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

# Event listener for after_flush
@event.listens_for(Session, 'after_flush')
def db_after_flush(session, flush_context):
    # Loop through new instances in the session
    for instance in session.new:
        if isinstance(instance, AuditLog):
            continue  # Skip if instance is an AuditLog
        model_name = instance.__class__.__name__.lower()  # Get the model name
        user = current_user if current_user.is_authenticated else None  # Get current user
        if user:
            # Create AuditLog entry for creation event
            al = AuditLog(request_id=str(g.request_id), model_name=model_name, original_id=instance.id, db_event_name="create", date_time=datetime.now(), user_ip_address=request.remote_addr, username=user.username)
        else:
            al = AuditLog(request_id=str(g.request_id), model_name=model_name, original_id=instance.id, db_event_name="create", date_time=datetime.now(), user_ip_address=request.remote_addr)
        session.add(al)  # Add AuditLog entry to session

# Event listener for before_flush
@event.listens_for(Session, 'before_flush')
def db_before_flush(session, flush_context, instances):
    # Loop through dirty instances in the session
    for instance in session.dirty:
        if isinstance(instance, AuditLog):
            continue  # Skip if instance is an AuditLog

        model_name = instance.__class__.__name__.lower()  # Get the model name

        if isinstance(instance, User):
            history = {}
            # Loop through specified attributes of User model
            for attr in ['username', 'email', 'password', 'first_name', 'last_name', 'country', 'role', 'profile_picture', 'account_status']:
                if get_history(instance, attr).has_changes():
                    # If attribute has changed, record old and new values
                    history[attr] = {
                        'old': get_history(instance, attr).deleted[0] if get_history(instance, attr).deleted else None,
                        'new': get_history(instance, attr).added[0] if get_history(instance, attr).added else None
                    }
            if history:
                user = current_user if current_user.is_authenticated else None  # Get current user
                if user:
                    # If there are changes, create AuditLog entry for edit event
                    al = AuditLog(request_id=str(g.request_id), model_name=model_name, original_id=instance.id, db_event_name="edit", date_time=datetime.now(), user_ip_address=request.remote_addr, username=user.username, history=json.dumps(history, cls=CustomJSONEncoder))
                else:
                    al = AuditLog(request_id=str(g.request_id), model_name=model_name, original_id=instance.id, db_event_name="edit", date_time=datetime.now(), user_ip_address=request.remote_addr, history=json.dumps(history, cls=CustomJSONEncoder))
                session.add(al)  # Add AuditLog entry to session

        elif isinstance(instance, Incident):
            history = {}
            # Loop through specified attributes of Incident model
            for attr in ['title', 'year', 'industry_type', 'reliability', 'description', 'incident_type', 'impact', 'actions_taken']:
                if get_history(instance, attr).has_changes():
                    # If attribute has changed, record old and new values
                    history[attr] = {
                        'old': get_history(instance, attr).deleted[0] if get_history(instance, attr).deleted else None,
                        'new': get_history(instance, attr).added[0] if get_history(instance, attr).added else None
                    }
            if history:
                user = current_user if current_user.is_authenticated else None  # Get current user
                if user:
                    # If there are changes, create AuditLog entry for edit event
                    al = AuditLog(request_id=str(g.request_id), model_name=model_name, original_id=instance.id, db_event_name="edit", date_time=datetime.now(), user_ip_address=request.remote_addr, username=user.username, history=json.dumps(history, cls=CustomJSONEncoder))
                else:
                    al = AuditLog(request_id=str(g.request_id), model_name=model_name, original_id=instance.id, db_event_name="edit", date_time=datetime.now(), user_ip_address=request.remote_addr, history=json.dumps(history, cls=CustomJSONEncoder))
                session.add(al)  # Add AuditLog entry to session

    # Loop through deleted instances in the session
    for instance in session.deleted:
        if isinstance(instance, AuditLog):
            continue  # Skip if instance is an AuditLog
        if isinstance(instance, User):
            history = {
                'id': get_history(instance, 'id').deleted[0] if get_history(instance, 'id').deleted else None,
                'username': get_history(instance, 'username').deleted[0] if get_history(instance, 'username').deleted else None,
                'email': get_history(instance, 'email').deleted[0] if get_history(instance, 'email').deleted else None,
                'password': get_history(instance, 'password').deleted[0] if get_history(instance, 'password').deleted else None,
                'first_name': get_history(instance, 'first_name').deleted[0] if get_history(instance, 'first_name').deleted else None,
                'last_name': get_history(instance, 'last_name').deleted[0] if get_history(instance, 'last_name').deleted else None,
                'country': get_history(instance, 'country').deleted[0] if get_history(instance, 'country').deleted else None,
                'role': get_history(instance, 'role').deleted[0] if get_history(instance, 'role').deleted else None,
                'profile_picture': get_history(instance, 'profile_picture').deleted[0] if get_history(instance, 'profile_picture').deleted else None,
                'account_status': get_history(instance, 'account_status').deleted[0] if get_history(instance, 'account_status').deleted else None,
            }
            model_name = "user"
            # Create AuditLog entry for delete event
            al = AuditLog(request_id=str(g.request_id), model_name=model_name, original_id=instance.id, db_event_name="delete", date_time=datetime.now(), user_ip_address=request.remote_addr, username=current_user.username, history=json.dumps(history, cls=CustomJSONEncoder))
            session.add(al)  # Add AuditLog entry to session

        elif isinstance(instance, Incident):
            history = {
                'id': get_history(instance, 'id').deleted[0] if get_history(instance, 'id').deleted else None,
                'title': get_history(instance, 'title').deleted[0] if get_history(instance, 'title').deleted else None,
                'year': get_history(instance, 'year').deleted[0] if get_history(instance, 'year').deleted else None,
                'industry_type': get_history(instance, 'industry_type').deleted[0] if get_history(instance, 'industry_type').deleted else None,
                'reliability': get_history(instance, 'reliability').deleted[0] if get_history(instance, 'reliability').deleted else None,
                'description': get_history(instance, 'description').deleted[0] if get_history(instance, 'description').deleted else None,
                'incident_type': get_history(instance, 'incident_type').deleted[0] if get_history(instance, 'incident_type').deleted else None,
                'impact': get_history(instance, 'impact').deleted[0] if get_history(instance, 'impact').deleted else None,
                'actions_taken': get_history(instance, 'actions_taken').deleted[0] if get_history(instance, 'actions_taken').deleted else None,
            }
            model_name = "incident"
            # Create AuditLog entry for delete event
            al = AuditLog(request_id=str(g.request_id), model_name=model_name, original_id=instance.id, db_event_name="delete", date_time=datetime.now(), user_ip_address=request.remote_addr, username=current_user.username, history=json.dumps(history, cls=CustomJSONEncoder))
            session.add(al)  # Add AuditLog entry to session
