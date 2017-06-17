from flask import Flask, jsonify, request, url_for, abort
from models import User, Request, Proposal, MealDate, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///meet-n-eat.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Meet\'n\'eat!'


@app.route('/api/v1/users', methods=['POST'])
def new_user():
    email = request.json.get('email')
    password = request.json.get('password')
    picture = request.json.get('picture')
    if email is None or password is None:
        abort(400)  # missing arguments
    if session.query(User).filter_by(email=email).first() is not None:
        abort(400)  # existing user
    user = User(email=email, picture=picture)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify(user.serialize), 201, {'Location': url_for('get_user', id=user.id, _external=True)}


@app.route('/api/v1/users', methods=['GET'])
def list_users():
    users = session.query(User).all()
    return jsonify(allUsers = [i.serialize for i in users])


@app.route('/api/v1/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify(user.serialize)


if __name__ == '__main__':
    # Fixtures
    user = User(picture="pic", email="john.doe@example.com")
    session.add(user)
    session.commit()

    app.debug = True
    app.run(port=5000)
