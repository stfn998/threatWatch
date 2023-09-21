import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from ThreatWatch import mail

def save_picture(form_picture):
    """Save profile picture and return the filename."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_fn)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_email(subject, recipient, body):
    """Send an email with the specified subject, recipient, and body."""
    try:
        msg = Message(subject, sender='info.threatwatch@gmail.com', recipients=[recipient])
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {e}")
        return False

def send_reset_email(user):
    """Send a password reset email to the user."""
    token = user.get_reset_token()
    body = f'''Hi {user.email},

We received your request for password reset.
To reset your password, visit the following link: {url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.

Thanks,
ThreatWatch team
'''
    return send_email('Password Reset Request', user.email, body)

def send_confirmation_email(user):
    """Send an account confirmation email to the user."""
    token = user.get_confirmation_token()
    if token is not None:
        body = f'''Hi {user.email},

Thank you for registering with ThreatWatch! To confirm your account, please visit the following link: {url_for('users.confirm_email', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.

Thanks,
ThreatWatch team
'''
        return send_email('Account Confirmation', user.email, body)
    else:
        current_app.logger.error("Failed to generate confirmation token.")
        return False
