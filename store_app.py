from app import create_app
from database import db

application = create_app()


@application.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    application.run(port=5000, debug=True)
