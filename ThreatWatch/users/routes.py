from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc
from ThreatWatch import db, bcrypt
from ThreatWatch.models import User, Incident
from ThreatWatch.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from ThreatWatch.users.utils import save_picture, send_reset_email, send_confirmation_email
from ThreatWatch.enums import AccountStatus, Role
from ThreatWatch.decorators import account_status_required, admin_required

# Create a Blueprint named 'users'
users = Blueprint('users', __name__)
PER_PAGE = 10

# Registration route
@users.post('/register')
@users.get('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        flash('Your account has been created. To activate your account, please check your email for a confirmation link.', 'info')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

# Login route
@users.post('/login')
@users.get('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccesful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout route
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Account management route
@users.post('/account')
@users.get('/account')
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.profile_picture = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.country = form.country.data
        db.session.commit()
        flash('Your account data has been updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.country.data = current_user.country
    image_file = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    return render_template('account.html', title='Account', image_file=image_file, form = form)

# User incidents route
@users.route('/user/<string:username>')
def user_incidents(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    incidents = Incident.query.filter_by(author=user).order_by(desc(Incident.created_date)).paginate(page=page, per_page=5)
    return render_template('user_incidents.html', incidents=incidents, user=user)


# Password reset request route
@users.get('/reset_password')
@users.post('/reset_password')
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

# Password reset token route
@users.get('/reset_password/<token>')
@users.post('/reset_password/<token>')
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated. You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

# Email confirmation route
@users.get('/confirm_email/<token>')
@users.post('/confirm_email/<token>')
def confirm_email(token):
    user = User.verify_confirmation_token(token)
    if user:
        user.account_status = AccountStatus.CONFIRMED
        db.session.commit()
        flash('Your email address has been confirmed.', 'success')
        return redirect(url_for('users.login'))
    else:
        flash('Invalid or expired confirmation link.', 'danger')
        return redirect(url_for('main.home'))

# User accounts management route (admin only)
@users.get('/user_accounts')
@users.post('/user_accounts')
@login_required
@admin_required
def user_accounts():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id).paginate(page=page, per_page=3)
    return render_template('user_accounts.html', users=users)

# Disable user route (admin only)
@users.get('/user/<string:username>/disable')
@users.post('/user/<string:username>/disable')
@login_required
@admin_required
def disable_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.role != Role.ADMIN:
        abort(403)
    user.account_status = AccountStatus.DISABLED
    db.session.commit()
    flash('User has been disabled.', 'success')
    return redirect(url_for('users.user_accounts'))

# Activate user route (admin only)
@users.get('/user/<string:username>/activate')
@users.post('/user/<string:username>/activate')
@login_required
@admin_required
def activate_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.role != Role.ADMIN:
        abort(403)
    user.account_status = AccountStatus.CONFIRMED
    db.session.commit()
    flash('User has been activated.', 'success')
    return redirect(url_for('users.user_accounts'))
