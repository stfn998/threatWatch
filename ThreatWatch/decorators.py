# Import necessary modules
from functools import wraps
from flask import render_template
from flask_login import current_user
from .enums import AccountStatus, Role

# Define a decorator function to check the account status of the user
def account_status_required(required_status):
    # Define a decorator function that takes another function (func) as an argument
    def decorator(func):
        # Use the wraps decorator to preserve the original function's metadata
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check the account status of the current user
            if current_user.account_status == AccountStatus.DISABLED:
                # If the account is disabled, render a 403 (Forbidden) error page
                return render_template('errors/403.html', description="Your account is temporarily disabled, please contact the administrator."), 403
            elif current_user.account_status == AccountStatus.PENDING:
                # If the account status is pending, render a 403 (Forbidden) error page
                return render_template('errors/403.html', description="Please check your email account, confirm registration and try again."), 403
            elif current_user.account_status != required_status:
                # If the account status does not match the required status, render a 403 (Forbidden) error page
                return render_template('errors/403.html', description="You don't have permission to do that."), 403
            # If all checks pass, execute the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Define a decorator function to check if the user has admin privileges
def admin_required(func):
    # Use the wraps decorator to preserve the original function's metadata
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if the current user has the role of ADMIN
        if current_user.role != Role.ADMIN:
            # If not, render a 403 (Forbidden) error page
            return render_template('errors/403.html', description="You don't have permission to do that."), 403
        # If the user has admin privileges, execute the original function
        return func(*args, **kwargs)
    return wrapper
