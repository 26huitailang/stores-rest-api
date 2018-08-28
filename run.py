from app import create_app
from db import db

app = create_app()
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
