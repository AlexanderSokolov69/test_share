import datetime

from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from .db_init import db
from .users import User

def abort_if_user_not_found(user_id):
    user = db.session.query(User).get(user_id)
    if not user:
        abort(404, message=f"Users {user_id} not found")

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', required=False, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('modified_date', required=True)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        user = db.session.get(User, user_id)
        return jsonify({'users': user.to_dict(
            only=('id', 'name', 'surname', 'email'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        news = db.session.get(User, user_id)
        db.session.delete(news)
        db.session.commit()
        return jsonify({'success': 'OK'})

class UsersListResource(Resource):
    def get(self):
        users = db.session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'surname', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            modified_date=datetime.date.fromisoformat(args['modified_date'])
        )
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id})
