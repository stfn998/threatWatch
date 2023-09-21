from ThreatWatch import create_app
from flask import g
from uuid import uuid4

app = create_app()

@app.before_request
def before_request_handler():
    g.request_id = str(uuid4())

if __name__ == '__main__':
    app.run(debug=True)
